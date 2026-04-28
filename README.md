# ML-Driven OS Performance Optimization

A comprehensive machine learning system that optimizes operating system performance through intelligent analysis of system metrics, database-driven storage, and algorithmic optimization techniques with a modern web interface.

## 🚀 Features Overview

### 🌐 Web Dashboard
- **Interactive Real-time Dashboard**: Modern responsive web interface
- **Live Performance Charts**: Dynamic visualizations with Plotly.js
- **ML Predictions Display**: Visual prediction graphs with confidence indicators
- **System Health Scoring**: Real-time health assessment with risk indicators
- **Anomaly Highlighting**: Visual alerts for detected anomalies
- **Optimization Suggestions Panel**: Intelligent recommendations with priority levels

### 🗄️ Database Integration
- **MySQL Database**: Persistent storage for all system metrics
- **Automated Data Collection**: Stores metrics every 5 seconds automatically
- **Historical Analysis**: Query and analyze performance trends over time
- **Data Retention**: Configurable retention policies for long

-term analysis

### 🤖 Machine Learning Engine
- **Linear Regression Models**: Separate models for CPU and Memory prediction
- **5-minute Predictions**: Forecast next 5 minutes of resource usage
- **Model Accuracy Tracking**: R² scores and RMSE metrics for model performance
- **Automatic Retraining**: Models retrain automatically with new data
- **Feature Engineering**: Advanced time-based and lag features for better predictions

### 🔍 Anomaly Detection
- **Moving Average Algorithm**: Detects sudden spikes using statistical thresholds
- **Multi-metric Analysis**: Monitors CPU, Memory, Disk, and Network simultaneously
- **Severity Classification**: Low, Medium, High severity levels
- **Real-time Alerts**: Immediate notification of anomalous behavior
- **Historical Anomaly Tracking**: Store and analyze anomaly patterns

### 🔧 Optimization Engine
- **System Health Score**: Weighted formula: `100 - (0.4×CPU + 0.3×Memory + 0.2×Disk + 0.1×Network)`
- **Intelligent Alerts**: Configurable thresholds for different metrics
- **Optimization Suggestions**: Context-aware recommendations based on system state
- **Impact Analysis**: Estimate potential improvements from suggestions
- **Risk Assessment**: Low/Medium/High risk classification

### 📊 Advanced Analytics
- **Moving Average Smoothing**: Reduce noise in performance data
- **Trend Analysis**: Identify performance patterns over time
- **Correlation Analysis**: Understand relationships between metrics
- **Performance Forecasting**: Predict future resource requirements

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Web Dashboard  │───▶│  Flask API   │───▶│  MySQL Database │
│  (Enhanced UI)  │    │  (REST API)  │    │  (Persistence)  │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                       │                    │
         ▼                       ▼                    ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Real-time      │    │  ML Engine   │    │  Optimization   │
│  Monitoring     │    │  (Sklearn)   │    │  Engine         │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
ml-os-performance-optimization/
├── 📄 README.md                     # Project documentation
├── 📄 requirements.txt              # Python dependencies
├── 📄 config.py                     # Configuration management
├── 📄 setup_ml_system.py           # Automated setup script
├── 📄 ml_performance_server.py     # Main application server
├── 📄 enhanced_dashboard.html      # Modern web dashboard
├── 📄 API_DOCUMENTATION.md         # Complete API documentation
├── 🗂️ database/                    # Database management
│   ├── __init__.py
│   └── mysql_manager.py            # MySQL operations
├── 🗂️ routes/                      # API routes
│   ├── __init__.py
│   └── api_routes.py               # REST API endpoints
├── 🗂️ ml/                          # Machine learning modules
│   ├── __init__.py
│   ├── predictor.py                # ML prediction models
│   └── anomaly_detector.py         # Anomaly detection
├── 🗂️ services/                    # Business logic
│   ├── __init__.py
│   └── optimization_engine.py      # Optimization algorithms
├── 🗂️ models/                      # Trained ML models
├── 🗂️ data/                        # Data storage
└── 🗂️ logs/                        # Application logs
```

## Getting Started

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize the system
python setup.py
```

### 2. Web Dashboard (Recommended)
```bash
# Start the web dashboard
python web_server.py

# Or use the batch file on Windows
start_dashboard.bat

# Or specify a custom port
python web_server.py --port 8081
```

The web dashboard provides:
- **Real-time monitoring** at http://localhost:8080
- **Interactive charts** with Plotly.js
- **Live system metrics** (CPU, Memory, Disk, Network)
- **Auto-refresh capability**
- **Responsive design** for mobile devices
- **No additional dependencies** (uses built-in Python libraries)

### 3. Quick Demo
```bash
# Run a 2-minute demonstration
python demo.py --mode quick

# Or run a comprehensive 5-minute demo
python demo.py --mode full
```

### 4. Command Line Usage
```bash
# Continuous monitoring (recommended)
python main.py --mode monitor

# Generate performance report
python main.py --mode report

# Train ML models manually
python main.py --mode train

# Comprehensive analysis with visualizations
python analyze.py --hours 24
```

## Usage Examples

### Continuous Monitoring
```bash
# Start continuous monitoring with ML optimization
python main.py --mode monitor

# Monitor for specific duration (1 hour)
python main.py --mode monitor --duration 3600
```

### Performance Analysis
```bash
# Analyze last 24 hours with charts
python analyze.py --hours 24

# Quick analysis without ML training
python analyze.py --hours 12 --no-ml

# Analysis without visualizations
python analyze.py --hours 6 --no-charts

# Save results to file
python analyze.py --hours 24 --output results.json
```

### Custom Demo
```bash
# 10-minute demo with 30-second intervals
python demo.py --duration 10 --interval 30
```

## Key Features

### 🌐 Web Dashboard
- **Interactive Streamlit Dashboard**: Real-time performance monitoring
- **REST API**: Full programmatic access to all system data
- **Live Charts**: Dynamic visualizations with Plotly
- **ML Controls**: Train models and view predictions through web UI
- **Mobile Responsive**: Access from any device

### 🔍 System Monitoring
- Real-time CPU, memory, disk, and network metrics
- Process-level performance tracking
- Configurable collection intervals
- Persistent data storage

### 🤖 Machine Learning
- **Performance Prediction**: Forecast resource usage trends
- **Anomaly Detection**: Identify unusual system behavior
- **Pattern Analysis**: Cluster performance states
- **Optimization**: Generate actionable recommendations

### 📊 Visualization
- Resource usage timelines
- Performance distribution analysis
- Correlation matrices
- Trend analysis with moving averages

### 🎯 Optimization
- Automated performance recommendations
- Resource allocation suggestions
- Bottleneck identification
- Proactive system tuning

## Technologies

- **Database**: SQLite with SQLAlchemy ORM
- **ML Framework**: scikit-learn, pandas, numpy
- **System Monitoring**: psutil for cross-platform metrics
- **Visualization**: matplotlib, seaborn
- **Scheduling**: schedule for automated tasks