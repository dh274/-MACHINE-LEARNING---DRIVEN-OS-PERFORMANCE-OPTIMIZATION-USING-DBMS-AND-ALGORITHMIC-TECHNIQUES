"""
Anomaly Detection Module for OS Performance Optimization
Detects performance anomalies using moving averages and statistical thresholds.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
from collections import deque

class AnomalyDetector:
    """
    Anomaly detector using moving averages and statistical thresholds.
    Detects sudden spikes in system metrics.
    """
    
    def __init__(self, window_size: int = 10, threshold_multiplier: float = 2.0):
        """
        Initialize anomaly detector.
        
        Args:
            window_size: Size of moving average window
            threshold_multiplier: Multiplier for standard deviation threshold
        """
        self.window_size = window_size
        self.threshold_multiplier = threshold_multiplier
        
        # Historical data buffers for real-time detection
        self.cpu_history = deque(maxlen=window_size)
        self.memory_history = deque(maxlen=window_size)
        self.disk_history = deque(maxlen=window_size)
        self.network_history = deque(maxlen=window_size)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"🔍 Anomaly detector initialized (window={window_size}, threshold={threshold_multiplier})")
    
    def update_history(self, cpu: float, memory: float, disk: float, network: float):
        """
        Update historical data buffers.
        
        Args:
            cpu: CPU usage percentage
            memory: Memory usage percentage
            disk: Disk usage percentage
            network: Network usage in MB
        """
        self.cpu_history.append(cpu)
        self.memory_history.append(memory)
        self.disk_history.append(disk)
        self.network_history.append(network)
    
    def detect_anomalies(self, current_metrics: Dict) -> Dict:
        """
        Detect anomalies in current metrics using moving average method.
        
        Args:
            current_metrics: Current system metrics
            
        Returns:
            Dict: Anomaly detection results
        """
        cpu = current_metrics.get('cpu', 0)
        memory = current_metrics.get('memory', 0)
        disk = current_metrics.get('disk', 0)
        network = current_metrics.get('network', 0)
        
        # Update history
        self.update_history(cpu, memory, disk, network)
        
        anomalies = []
        
        # Check each metric for anomalies
        metrics_to_check = [
            ('cpu', cpu, self.cpu_history),
            ('memory', memory, self.memory_history),
            ('disk', disk, self.disk_history),
            ('network', network, self.network_history)
        ]
        
        for metric_name, current_value, history in metrics_to_check:
            if len(history) >= 3:  # Need at least 3 points for meaningful detection
                anomaly_result = self._detect_single_metric_anomaly(
                    metric_name, current_value, list(history)
                )
                if anomaly_result['is_anomaly']:
                    anomalies.append(anomaly_result)
        
        # Determine overall anomaly status
        is_anomaly = len(anomalies) > 0
        severity = self._calculate_overall_severity(anomalies) if is_anomaly else 'normal'
        
        result = {
            'is_anomaly': is_anomaly,
            'severity': severity,
            'anomalies': anomalies,
            'timestamp': datetime.now().isoformat(),
            'detection_method': 'moving_average_threshold'
        }
        
        if is_anomaly:
            self.logger.warning(f"⚠️ Anomaly detected: {severity} severity, {len(anomalies)} metrics affected")
        
        return result
    
    def _detect_single_metric_anomaly(self, metric_name: str, current_value: float, 
                                    history: List[float]) -> Dict:
        """
        Detect anomaly for a single metric.
        
        Args:
            metric_name: Name of the metric
            current_value: Current metric value
            history: Historical values
            
        Returns:
            Dict: Anomaly detection result for single metric
        """
        if len(history) < 3:
            return {'is_anomaly': False, 'metric': metric_name}
        
        # Calculate moving average (excluding current value)
        historical_values = history[:-1]  # Exclude current value
        moving_average = np.mean(historical_values)
        std_dev = np.std(historical_values)
        
        # Calculate threshold
        threshold = moving_average + (self.threshold_multiplier * std_dev)
        
        # Check for anomaly
        is_anomaly = current_value > threshold
        
        # Calculate severity based on how much the threshold is exceeded
        if is_anomaly:
            excess_ratio = (current_value - threshold) / threshold if threshold > 0 else 1
            if excess_ratio > 0.5:
                severity = 'high'
            elif excess_ratio > 0.2:
                severity = 'medium'
            else:
                severity = 'low'
        else:
            severity = 'normal'
        
        return {
            'is_anomaly': is_anomaly,
            'metric': metric_name,
            'current_value': current_value,
            'moving_average': moving_average,
            'threshold': threshold,
            'severity': severity,
            'excess_ratio': (current_value - threshold) / threshold if is_anomaly and threshold > 0 else 0
        }
    
    def _calculate_overall_severity(self, anomalies: List[Dict]) -> str:
        """
        Calculate overall severity from individual anomalies.
        
        Args:
            anomalies: List of individual anomaly results
            
        Returns:
            str: Overall severity level
        """
        if not anomalies:
            return 'normal'
        
        severity_scores = {'low': 1, 'medium': 2, 'high': 3}
        max_severity = max(severity_scores.get(a['severity'], 0) for a in anomalies)
        
        for severity, score in severity_scores.items():
            if score == max_severity:
                return severity
        
        return 'low'
    
    def detect_batch_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in a batch of historical data.
        
        Args:
            df: DataFrame with historical metrics
            
        Returns:
            pd.DataFrame: DataFrame with anomaly flags
        """
        if df.empty or len(df) < self.window_size:
            self.logger.warning("Insufficient data for batch anomaly detection")
            return df
        
        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Initialize anomaly columns
        df['cpu_anomaly'] = False
        df['memory_anomaly'] = False
        df['disk_anomaly'] = False
        df['network_anomaly'] = False
        df['overall_anomaly'] = False
        df['anomaly_severity'] = 'normal'
        
        # Detect anomalies for each row
        for i in range(self.window_size, len(df)):
            # Get window of historical data
            window_start = max(0, i - self.window_size)
            window_data = df.iloc[window_start:i]
            
            current_row = df.iloc[i]
            current_metrics = {
                'cpu': current_row['cpu'],
                'memory': current_row['memory'],
                'disk': current_row['disk'],
                'network': current_row['network']
            }
            
            # Detect anomalies
            anomaly_result = self._detect_anomalies_from_window(current_metrics, window_data)
            
            # Update DataFrame
            df.loc[i, 'cpu_anomaly'] = anomaly_result.get('cpu_anomaly', False)
            df.loc[i, 'memory_anomaly'] = anomaly_result.get('memory_anomaly', False)
            df.loc[i, 'disk_anomaly'] = anomaly_result.get('disk_anomaly', False)
            df.loc[i, 'network_anomaly'] = anomaly_result.get('network_anomaly', False)
            df.loc[i, 'overall_anomaly'] = anomaly_result.get('overall_anomaly', False)
            df.loc[i, 'anomaly_severity'] = anomaly_result.get('severity', 'normal')
        
        anomaly_count = df['overall_anomaly'].sum()
        self.logger.info(f"🔍 Batch anomaly detection complete: {anomaly_count} anomalies found in {len(df)} records")
        
        return df
    
    def _detect_anomalies_from_window(self, current_metrics: Dict, window_data: pd.DataFrame) -> Dict:
        """
        Detect anomalies using a specific window of historical data.
        
        Args:
            current_metrics: Current metric values
            window_data: Historical data window
            
        Returns:
            Dict: Anomaly detection results
        """
        results = {}
        anomalies = []
        
        for metric in ['cpu', 'memory', 'disk', 'network']:
            if metric in window_data.columns:
                historical_values = window_data[metric].values
                current_value = current_metrics.get(metric, 0)
                
                if len(historical_values) > 0:
                    moving_average = np.mean(historical_values)
                    std_dev = np.std(historical_values)
                    threshold = moving_average + (self.threshold_multiplier * std_dev)
                    
                    is_anomaly = current_value > threshold
                    results[f'{metric}_anomaly'] = is_anomaly
                    
                    if is_anomaly:
                        excess_ratio = (current_value - threshold) / threshold if threshold > 0 else 1
                        if excess_ratio > 0.5:
                            severity = 'high'
                        elif excess_ratio > 0.2:
                            severity = 'medium'
                        else:
                            severity = 'low'
                        
                        anomalies.append({
                            'metric': metric,
                            'severity': severity,
                            'current_value': current_value,
                            'threshold': threshold
                        })
        
        # Overall anomaly status
        results['overall_anomaly'] = len(anomalies) > 0
        results['severity'] = self._calculate_overall_severity(anomalies) if anomalies else 'normal'
        results['anomaly_count'] = len(anomalies)
        
        return results
    
    def get_anomaly_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get statistics about anomalies in the dataset.
        
        Args:
            df: DataFrame with anomaly detection results
            
        Returns:
            Dict: Anomaly statistics
        """
        if 'overall_anomaly' not in df.columns:
            return {'error': 'No anomaly detection results found'}
        
        total_records = len(df)
        total_anomalies = df['overall_anomaly'].sum()
        anomaly_rate = (total_anomalies / total_records * 100) if total_records > 0 else 0
        
        # Severity distribution
        severity_counts = df['anomaly_severity'].value_counts().to_dict()
        
        # Metric-specific anomaly counts
        metric_anomalies = {}
        for metric in ['cpu', 'memory', 'disk', 'network']:
            col_name = f'{metric}_anomaly'
            if col_name in df.columns:
                metric_anomalies[metric] = df[col_name].sum()
        
        return {
            'total_records': total_records,
            'total_anomalies': int(total_anomalies),
            'anomaly_rate_percent': round(anomaly_rate, 2),
            'severity_distribution': severity_counts,
            'metric_anomalies': metric_anomalies,
            'detection_window_size': self.window_size,
            'threshold_multiplier': self.threshold_multiplier
        }