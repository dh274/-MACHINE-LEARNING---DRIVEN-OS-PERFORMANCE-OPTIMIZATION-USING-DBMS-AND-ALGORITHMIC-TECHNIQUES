"""
Startup script for the web-based performance monitoring system.
Launches both the Flask API server and Streamlit dashboard.
"""

import subprocess
import sys
import time
import webbrowser
from threading import Thread

def run_flask_api():
    """Run the Flask API server."""
    print("🚀 Starting Flask API server...")
    subprocess.run([sys.executable, "web_api.py"])

def run_streamlit_dashboard():
    """Run the Streamlit dashboard."""
    print("📊 Starting Streamlit dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port=8501"])

def main():
    """Main startup function."""
    print("🌐 ML-Driven OS Performance Monitor - Web Interface")
    print("=" * 60)
    print("Starting web services...")
    
    # Start Flask API in a separate thread
    api_thread = Thread(target=run_flask_api, daemon=True)
    api_thread.start()
    
    # Wait a moment for API to start
    print("⏳ Waiting for API server to start...")
    time.sleep(3)
    
    # Start Streamlit dashboard
    print("🎯 Opening dashboard...")
    
    # Open browser automatically
    webbrowser.open("http://localhost:8501")
    
    # Run Streamlit (this will block)
    run_streamlit_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down web services...")
        sys.exit(0)