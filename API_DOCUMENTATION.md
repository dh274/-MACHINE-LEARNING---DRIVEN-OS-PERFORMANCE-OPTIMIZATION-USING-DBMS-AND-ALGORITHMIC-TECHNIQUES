# ML-Driven OS Performance Optimization - API Documentation

## Overview

This API provides comprehensive system performance monitoring, machine learning predictions, anomaly detection, and optimization recommendations for operating systems.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

---

## Endpoints

### Health Check

#### GET /api/health
Check the health status of the system and its components.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "version": "2.0.0",
  "components": {
    "database": true,
    "ml_predictor": false,
    "monitoring": true
  }
}
```

---

### System Metrics

#### GET /api/metrics/current
Get current system performance metrics.

**Response:**
```json
{
  "success": true,
  "data": {
    "cpu": 45.2,
    "memory": 67.8,
    "disk": 23.1,
    "network": 125.4,
    "timestamp": "2024-01-01T12:00:00.000Z",
    "system_info": {
      "cpu_cores": 8,
      "total_memory_gb": 16.0,
      "available_memory_gb": 5.2,
      "total_disk_gb": 500.0,
      "free_disk_gb": 384.5
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### GET /api/metrics/history
Get historical system metrics.

**Parameters:**
- `minutes` (optional): Number of minutes to look back (default: 60)

**Example:** `/api/metrics/history?minutes=120`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "cpu": 45.2,
      "memory": 67.8,
      "disk": 23.1,
      "network": 125.4,
      "timestamp": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 120,
  "minutes": 120
}
```

---

### Machine Learning

#### POST /api/ml/predict
Get ML predictions for system performance.

**Request Body:** None required (uses current metrics)

**Response:**
```json
{
  "success": true,
  "predictions": {
    "predicted_cpu": 48.5,
    "predicted_memory": 71.2,
    "prediction_horizon_minutes": 5,
    "prediction_time": "2024-01-01T12:00:00.000Z",
    "model_accuracy": {
      "cpu_r2": 0.85,
      "cpu_rmse": 3.2,
      "memory_r2": 0.78,
      "memory_rmse": 4.1,
      "training_samples": 500,
      "test_samples": 125
    },
    "confidence": "high"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### POST /api/ml/train
Train ML models using historical data.

**Request Body:**
```json
{
  "hours": 24
}
```

**Response:**
```json
{
  "success": true,
  "training_results": {
    "cpu_r2": 0.85,
    "cpu_rmse": 3.2,
    "memory_r2": 0.78,
    "memory_rmse": 4.1,
    "training_samples": 500,
    "test_samples": 125
  },
  "training_data_points": 625,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

---

### Anomaly Detection

#### POST /api/anomalies/detect
Detect anomalies in current system state.

**Request Body:** None required (uses current metrics)

**Response:**
```json
{
  "success": true,
  "anomaly_detection": {
    "is_anomaly": true,
    "severity": "medium",
    "anomalies": [
      {
        "metric": "cpu",
        "current_value": 95.2,
        "moving_average": 45.0,
        "threshold": 65.0,
        "severity": "high",
        "excess_ratio": 0.46
      }
    ],
    "timestamp": "2024-01-01T12:00:00.000Z",
    "detection_method": "moving_average_threshold"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

---

### Optimization Analysis

#### POST /api/optimization/analyze
Get comprehensive optimization analysis including health score, alerts, and suggestions.

**Request Body:** None required (uses current metrics)

**Response:**
```json
{
  "success": true,
  "optimization_analysis": {
    "timestamp": "2024-01-01T12:00:00.000Z",
    "current_metrics": {
      "cpu": 45.2,
      "memory": 67.8,
      "disk": 23.1,
      "network": 125.4
    },
    "predicted_metrics": {
      "predicted_cpu": 48.5,
      "predicted_memory": 71.2
    },
    "moving_averages": {
      "cpu_ma": 43.8,
      "memory_ma": 65.2,
      "disk_ma": 22.9,
      "network_ma": 120.1,
      "window_size": 5
    },
    "health_assessment": {
      "health_score": 72.5,
      "risk_level": "medium",
      "contributions": {
        "cpu": 18.08,
        "memory": 20.34,
        "disk": 4.62,
        "network": 1.25
      },
      "weights": {
        "cpu": 0.4,
        "memory": 0.3,
        "disk": 0.2,
        "network": 0.1
      },
      "timestamp": "2024-01-01T12:00:00.000Z"
    },
    "alerts": [
      {
        "type": "memory_risk_alert",
        "severity": "medium",
        "message": "Memory Risk: 67.8%",
        "metric": "memory",
        "current_value": 67.8,
        "threshold": 65.0,
        "timestamp": "2024-01-01T12:00:00.000Z"
      }
    ],
    "optimization_suggestions": [
      {
        "category": "memory_optimization",
        "priority": "medium",
        "suggestion": "Clear system cache and close memory-intensive applications",
        "details": "Current memory usage: 67.8%. Consider restarting memory-heavy applications or clearing cache.",
        "action_type": "cache_cleanup",
        "estimated_impact": "High",
        "timestamp": "2024-01-01T12:00:00.000Z"
      }
    ],
    "impact_analysis": {
      "total_suggestions": 1,
      "priority_breakdown": {
        "high": 0,
        "medium": 1,
        "low": 0
      },
      "potential_improvements": {
        "cpu": 5,
        "memory": 20,
        "disk": 0
      },
      "projected_values": {
        "cpu": 40.2,
        "memory": 47.8,
        "disk": 23.1
      },
      "overall_improvement_score": 8.33
    },
    "summary": {
      "health_score": 72.5,
      "risk_level": "medium",
      "alert_count": 1,
      "suggestion_count": 1,
      "high_priority_actions": 0
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

---

### Monitoring Control

#### POST /api/monitoring/start
Start background monitoring (collects metrics every 5 seconds).

**Request Body:** None

**Response:**
```json
{
  "success": true,
  "message": "Background monitoring started",
  "interval_seconds": 5,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### POST /api/monitoring/stop
Stop background monitoring.

**Request Body:** None

**Response:**
```json
{
  "success": true,
  "message": "Background monitoring stopped",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### GET /api/monitoring/status
Get current monitoring status.

**Response:**
```json
{
  "monitoring_active": true,
  "database_connected": true,
  "ml_models_trained": false,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

---

### Dashboard Data

#### GET /api/dashboard/data
Get comprehensive data for dashboard display (combines multiple endpoints).

**Response:**
```json
{
  "success": true,
  "dashboard_data": {
    "current_metrics": { /* Current metrics object */ },
    "predictions": { /* Predictions object */ },
    "anomalies": { /* Anomaly detection object */ },
    "optimization": { /* Optimization analysis object */ },
    "recent_history": [ /* Array of recent metrics */ ],
    "monitoring_status": {
      "active": true,
      "database_connected": true,
      "models_trained": false
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message describing what went wrong",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error
- `503`: Service Unavailable (database not connected)

---

## Data Types

### Metric Values
- **CPU**: Percentage (0-100)
- **Memory**: Percentage (0-100)
- **Disk**: Percentage (0-100)
- **Network**: Megabytes (MB)

### Severity Levels
- `low`: Minor issue or low confidence
- `medium`: Moderate issue requiring attention
- `high`: Critical issue requiring immediate action

### Risk Levels
- `low`: System performing well (health score > 80)
- `medium`: Some performance concerns (health score 60-80)
- `high`: Significant performance issues (health score < 60)

### Priority Levels
- `low`: Nice to have optimization
- `medium`: Recommended optimization
- `high`: Critical optimization needed

---

## Usage Examples

### Basic Monitoring Workflow

1. **Start monitoring:**
   ```bash
   curl -X POST http://localhost:5000/api/monitoring/start
   ```

2. **Check current metrics:**
   ```bash
   curl http://localhost:5000/api/metrics/current
   ```

3. **Train ML models (after collecting data):**
   ```bash
   curl -X POST http://localhost:5000/api/ml/train \
     -H "Content-Type: application/json" \
     -d '{"hours": 24}'
   ```

4. **Get predictions:**
   ```bash
   curl -X POST http://localhost:5000/api/ml/predict
   ```

5. **Get optimization analysis:**
   ```bash
   curl -X POST http://localhost:5000/api/optimization/analyze
   ```

### JavaScript Example

```javascript
// Get dashboard data
async function getDashboardData() {
  try {
    const response = await fetch('/api/dashboard/data');
    const data = await response.json();
    
    if (data.success) {
      console.log('Current CPU:', data.dashboard_data.current_metrics.cpu);
      console.log('Health Score:', data.dashboard_data.optimization.health_assessment.health_score);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Start monitoring
async function startMonitoring() {
  try {
    const response = await fetch('/api/monitoring/start', {
      method: 'POST'
    });
    const result = await response.json();
    console.log(result.message);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. However, it's recommended to:
- Limit monitoring status checks to once per second
- Limit training requests to once per hour
- Use the dashboard data endpoint for comprehensive updates

---

## Database Schema

The system uses the following MySQL tables:

### system_metrics
- `id`: Auto-increment primary key
- `cpu`: CPU usage percentage
- `memory`: Memory usage percentage
- `disk`: Disk usage percentage
- `network`: Network usage in MB
- `timestamp`: Record timestamp

### ml_predictions
- `id`: Auto-increment primary key
- `predicted_cpu`: Predicted CPU usage
- `predicted_memory`: Predicted memory usage
- `prediction_horizon`: Prediction horizon in minutes
- `model_accuracy`: Model accuracy score
- `timestamp`: Prediction timestamp

### optimization_logs
- `id`: Auto-increment primary key
- `optimization_type`: Type of optimization
- `suggestion`: Optimization suggestion text
- `priority`: Priority level (low/medium/high)
- `system_state`: JSON of system state
- `timestamp`: Log timestamp

### anomalies
- `id`: Auto-increment primary key
- `metric_type`: Type of metric (cpu/memory/disk/network)
- `anomaly_value`: Anomalous value
- `threshold_value`: Threshold that was exceeded
- `severity`: Severity level (low/medium/high)
- `timestamp`: Anomaly timestamp

### health_scores
- `id`: Auto-increment primary key
- `health_score`: Calculated health score
- `risk_level`: Risk level (low/medium/high)
- `cpu_contribution`: CPU contribution to score
- `memory_contribution`: Memory contribution to score
- `disk_contribution`: Disk contribution to score
- `network_contribution`: Network contribution to score
- `timestamp`: Score timestamp