"""
Database Management System for OS Performance Metrics
Handles storage, retrieval, and querying of system performance data.
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SystemMetrics(Base):
    """SQLAlchemy model for system metrics."""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    memory_used = Column(Integer)
    memory_available = Column(Integer)
    disk_percent = Column(Float)
    disk_read_bytes = Column(Integer)
    disk_write_bytes = Column(Integer)
    network_bytes_sent = Column(Integer)
    network_bytes_recv = Column(Integer)
    top_processes = Column(Text)  # JSON string
    raw_data = Column(Text)  # Complete metrics as JSON


class DatabaseManager:
    """Manages database operations for system metrics."""
    
    def __init__(self, db_path: str = "data/performance_metrics.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def store_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Store system metrics in database.
        
        Args:
            metrics: Dictionary containing system metrics
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract key metrics for structured storage
            cpu_percent = metrics.get('cpu', {}).get('cpu_percent', 0)
            memory_data = metrics.get('memory', {}).get('virtual_memory', {})
            disk_data = metrics.get('disk', {})
            network_data = metrics.get('network', {})
            
            # Create database record
            record = SystemMetrics(
                timestamp=datetime.fromisoformat(metrics['timestamp']),
                cpu_percent=cpu_percent,
                memory_percent=memory_data.get('percent', 0),
                memory_used=memory_data.get('used', 0),
                memory_available=memory_data.get('available', 0),
                disk_percent=disk_data.get('disk_usage', {}).get('percent', 0),
                disk_read_bytes=disk_data.get('disk_io', {}).get('read_bytes', 0),
                disk_write_bytes=disk_data.get('disk_io', {}).get('write_bytes', 0),
                network_bytes_sent=network_data.get('bytes_sent', 0) if network_data else 0,
                network_bytes_recv=network_data.get('bytes_recv', 0) if network_data else 0,
                top_processes=json.dumps(metrics.get('processes', [])),
                raw_data=json.dumps(metrics, default=str)
            )
            
            self.session.add(record)
            self.session.commit()
            return True
            
        except Exception as e:
            print(f"Error storing metrics: {e}")
            self.session.rollback()
            return False
    
    def get_metrics_range(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Retrieve metrics within a time range.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            
        Returns:
            DataFrame containing metrics
        """
        query = self.session.query(SystemMetrics).filter(
            SystemMetrics.timestamp >= start_time,
            SystemMetrics.timestamp <= end_time
        ).order_by(SystemMetrics.timestamp)
        
        results = query.all()
        
        # Convert to DataFrame
        data = []
        for record in results:
            data.append({
                'timestamp': record.timestamp,
                'cpu_percent': record.cpu_percent,
                'memory_percent': record.memory_percent,
                'memory_used': record.memory_used,
                'memory_available': record.memory_available,
                'disk_percent': record.disk_percent,
                'disk_read_bytes': record.disk_read_bytes,
                'disk_write_bytes': record.disk_write_bytes,
                'network_bytes_sent': record.network_bytes_sent,
                'network_bytes_recv': record.network_bytes_recv
            })
        
        return pd.DataFrame(data)
    
    def get_recent_metrics(self, hours: int = 24) -> pd.DataFrame:
        """
        Get metrics from the last N hours.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            DataFrame containing recent metrics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        return self.get_metrics_range(start_time, end_time)
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get performance summary statistics.
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            Dictionary containing summary statistics
        """
        df = self.get_recent_metrics(hours)
        
        if df.empty:
            return {"error": "No data available"}
        
        summary = {
            'time_range': {
                'start': df['timestamp'].min().isoformat(),
                'end': df['timestamp'].max().isoformat(),
                'duration_hours': hours
            },
            'cpu': {
                'avg': df['cpu_percent'].mean(),
                'max': df['cpu_percent'].max(),
                'min': df['cpu_percent'].min(),
                'std': df['cpu_percent'].std()
            },
            'memory': {
                'avg_percent': df['memory_percent'].mean(),
                'max_percent': df['memory_percent'].max(),
                'avg_used_gb': df['memory_used'].mean() / (1024**3),
                'max_used_gb': df['memory_used'].max() / (1024**3)
            },
            'disk': {
                'avg_percent': df['disk_percent'].mean(),
                'max_percent': df['disk_percent'].max(),
                'total_read_gb': (df['disk_read_bytes'].max() - df['disk_read_bytes'].min()) / (1024**3),
                'total_write_gb': (df['disk_write_bytes'].max() - df['disk_write_bytes'].min()) / (1024**3)
            },
            'network': {
                'total_sent_gb': (df['network_bytes_sent'].max() - df['network_bytes_sent'].min()) / (1024**3),
                'total_recv_gb': (df['network_bytes_recv'].max() - df['network_bytes_recv'].min()) / (1024**3)
            }
        }
        
        return summary
    
    def identify_performance_anomalies(self, threshold_std: float = 2.0) -> List[Dict[str, Any]]:
        """
        Identify performance anomalies using statistical analysis.
        
        Args:
            threshold_std: Standard deviation threshold for anomaly detection
            
        Returns:
            List of detected anomalies
        """
        df = self.get_recent_metrics(24)
        
        if df.empty:
            return []
        
        anomalies = []
        
        # CPU anomalies
        cpu_mean = df['cpu_percent'].mean()
        cpu_std = df['cpu_percent'].std()
        cpu_threshold = cpu_mean + (threshold_std * cpu_std)
        
        cpu_anomalies = df[df['cpu_percent'] > cpu_threshold]
        for _, row in cpu_anomalies.iterrows():
            anomalies.append({
                'type': 'cpu_spike',
                'timestamp': row['timestamp'].isoformat(),
                'value': row['cpu_percent'],
                'threshold': cpu_threshold,
                'severity': 'high' if row['cpu_percent'] > cpu_mean + (3 * cpu_std) else 'medium'
            })
        
        # Memory anomalies
        mem_mean = df['memory_percent'].mean()
        mem_std = df['memory_percent'].std()
        mem_threshold = mem_mean + (threshold_std * mem_std)
        
        mem_anomalies = df[df['memory_percent'] > mem_threshold]
        for _, row in mem_anomalies.iterrows():
            anomalies.append({
                'type': 'memory_spike',
                'timestamp': row['timestamp'].isoformat(),
                'value': row['memory_percent'],
                'threshold': mem_threshold,
                'severity': 'high' if row['memory_percent'] > mem_mean + (3 * mem_std) else 'medium'
            })
        
        return anomalies
    
    def close(self):
        """Close database connection."""
        self.session.close()


if __name__ == "__main__":
    # Test database operations
    db = DatabaseManager()
    
    # Sample metrics for testing
    sample_metrics = {
        'timestamp': datetime.now().isoformat(),
        'uptime': 3600,
        'cpu': {'cpu_percent': 45.2},
        'memory': {'virtual_memory': {'percent': 67.8, 'used': 8589934592, 'available': 4294967296}},
        'disk': {
            'disk_usage': {'percent': 78.5},
            'disk_io': {'read_bytes': 1073741824, 'write_bytes': 536870912}
        },
        'network': {'bytes_sent': 1048576, 'bytes_recv': 2097152},
        'processes': [{'pid': 1234, 'name': 'test_process', 'cpu_percent': 12.5}]
    }
    
    # Store sample metrics
    success = db.store_metrics(sample_metrics)
    print(f"Metrics stored: {success}")
    
    # Get performance summary
    summary = db.get_performance_summary(1)
    print(f"Performance summary: {json.dumps(summary, indent=2, default=str)}")
    
    db.close()