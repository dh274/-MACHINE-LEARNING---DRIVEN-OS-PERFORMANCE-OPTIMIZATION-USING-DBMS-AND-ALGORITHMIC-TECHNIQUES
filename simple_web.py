"""
Simple Web Interface for OS Performance Monitoring
Lightweight version without ML dependencies.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psutil
import time
from datetime import datetime
import sqlite3
import os

# Page configuration
st.set_page_config(
    page_title="OS Performance Monitor",
    page_icon="📊",
    layout="wide"
)

def get_current_metrics():
    """Get current system metrics using psutil."""
    return {
        'timestamp': datetime.now(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent,
        'network_sent': psutil.net_io_counters().bytes_sent,
        'network_recv': psutil.net_io_counters().bytes_recv
    }

def init_database():
    """Initialize SQLite database for storing metrics."""
    conn = sqlite3.connect('data/simple_metrics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL,
            network_sent INTEGER,
            network_recv INTEGER
        )
    ''')
    
    conn.commit()
    return conn

def store_metrics(conn, metrics):
    """Store metrics in database."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metrics (timestamp, cpu_percent, memory_percent, disk_percent, network_sent, network_recv)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        metrics['timestamp'].isoformat(),
        metrics['cpu_percent'],
        metrics['memory_percent'],
        metrics['disk_percent'],
        metrics['network_sent'],
        metrics['network_recv']
    ))
    conn.commit()

def get_recent_metrics(conn, hours=24):
    """Get recent metrics from database."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM metrics 
        WHERE datetime(timestamp) > datetime('now', '-{} hours')
        ORDER BY timestamp DESC
    '''.format(hours))
    
    columns = ['id', 'timestamp', 'cpu_percent', 'memory_percent', 'disk_percent', 'network_sent', 'network_recv']
    data = cursor.fetchall()
    
    if data:
        df = pd.DataFrame(data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        return pd.DataFrame()

def main():
    """Main dashboard application."""
    
    # Initialize database
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = init_database()
    
    # Title
    st.title("📊 OS Performance Monitor")
    st.markdown("Real-time system monitoring dashboard")
    
    # Sidebar
    st.sidebar.header("⚙️ Controls")
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto-refresh (10s)", value=False)
    
    # Time range
    time_range = st.sidebar.selectbox(
        "📅 Time Range",
        options=[1, 6, 12, 24],
        index=3,
        format_func=lambda x: f"Last {x} hours"
    )
    
    # Manual refresh
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Store current metrics
    if st.sidebar.button("💾 Store Current Metrics"):
        current_metrics = get_current_metrics()
        store_metrics(conn, current_metrics)
        st.success("Metrics stored!")
    
    # Current Status
    st.header("📊 Current System Status")
    
    current_metrics = get_current_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🖥️ CPU Usage",
            value=f"{current_metrics['cpu_percent']:.1f}%"
        )
        
    with col2:
        st.metric(
            label="💾 Memory Usage", 
            value=f"{current_metrics['memory_percent']:.1f}%"
        )
        
    with col3:
        st.metric(
            label="💿 Disk Usage",
            value=f"{current_metrics['disk_percent']:.1f}%"
        )
        
    with col4:
        network_mb = current_metrics['network_sent'] / 1024 / 1024
        st.metric(
            label="📡 Network Sent",
            value=f"{network_mb:.1f} MB"
        )
    
    # Real-time gauges
    st.header("🎯 Real-time Gauges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_cpu = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_metrics['cpu_percent'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CPU Usage (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_cpu.update_layout(height=300)
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        fig_mem = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_metrics['memory_percent'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Memory Usage (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 85], 'color': "yellow"},
                    {'range': [85, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_mem.update_layout(height=300)
        st.plotly_chart(fig_mem, use_container_width=True)
    
    with col3:
        fig_disk = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_metrics['disk_percent'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Disk Usage (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkorange"},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 90], 'color': "yellow"},
                    {'range': [90, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig_disk.update_layout(height=300)
        st.plotly_chart(fig_disk, use_container_width=True)
    
    # Historical Data
    st.header("📈 Historical Performance")
    
    df = get_recent_metrics(conn, time_range)
    
    if not df.empty:
        # Time series chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Usage (%)', 'Memory Usage (%)', 'Disk Usage (%)', 'Network Activity (MB)'),
        )
        
        # CPU
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['cpu_percent'], 
                      name='CPU %', line=dict(color='#ff6b6b')),
            row=1, col=1
        )
        
        # Memory
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['memory_percent'], 
                      name='Memory %', line=dict(color='#4ecdc4')),
            row=1, col=2
        )
        
        # Disk
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['disk_percent'], 
                      name='Disk %', line=dict(color='#45b7d1')),
            row=2, col=1
        )
        
        # Network
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['network_sent']/1024/1024, 
                      name='Sent (MB)', line=dict(color='#96ceb4')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📋 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg CPU", f"{df['cpu_percent'].mean():.1f}%")
            st.metric("Max CPU", f"{df['cpu_percent'].max():.1f}%")
            
        with col2:
            st.metric("Avg Memory", f"{df['memory_percent'].mean():.1f}%")
            st.metric("Max Memory", f"{df['memory_percent'].max():.1f}%")
            
        with col3:
            st.metric("Avg Disk", f"{df['disk_percent'].mean():.1f}%")
            st.metric("Max Disk", f"{df['disk_percent'].max():.1f}%")
            
        with col4:
            st.metric("Data Points", f"{len(df)}")
            st.metric("Time Span", f"{time_range}h")
    
    else:
        st.info("No historical data available. Click 'Store Current Metrics' to start collecting data.")
    
    # System Information
    st.header("💻 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hardware")
        st.write(f"**CPU Cores:** {psutil.cpu_count()}")
        st.write(f"**CPU Frequency:** {psutil.cpu_freq().current:.0f} MHz")
        
        memory = psutil.virtual_memory()
        st.write(f"**Total Memory:** {memory.total / 1024**3:.1f} GB")
        st.write(f"**Available Memory:** {memory.available / 1024**3:.1f} GB")
    
    with col2:
        st.subheader("Network")
        net_io = psutil.net_io_counters()
        st.write(f"**Bytes Sent:** {net_io.bytes_sent / 1024**2:.1f} MB")
        st.write(f"**Bytes Received:** {net_io.bytes_recv / 1024**2:.1f} MB")
        st.write(f"**Packets Sent:** {net_io.packets_sent:,}")
        st.write(f"**Packets Received:** {net_io.packets_recv:,}")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()
    
    conn.close()

if __name__ == "__main__":
    main()