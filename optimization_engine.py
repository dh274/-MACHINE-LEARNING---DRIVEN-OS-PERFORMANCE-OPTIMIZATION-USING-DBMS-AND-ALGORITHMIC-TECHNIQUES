"""
Optimization Engine for OS Performance Optimization
Implements algorithmic optimization techniques and intelligent suggestions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
from collections import deque

class OptimizationEngine:
    """
    Algorithmic optimization engine for system performance.
    Implements moving averages, health scoring, and intelligent suggestions.
    """
    
    def __init__(self, ma_window: int = 5):
        """
        Initialize optimization engine.
        
        Args:
            ma_window: Moving average window size
        """
        self.ma_window = ma_window
        
        # Moving average buffers
        self.cpu_ma_buffer = deque(maxlen=ma_window)
        self.memory_ma_buffer = deque(maxlen=ma_window)
        self.disk_ma_buffer = deque(maxlen=ma_window)
        self.network_ma_buffer = deque(maxlen=ma_window)
        
        # Health score weights
        self.health_weights = {
            'cpu': 0.4,
            'memory': 0.3,
            'disk': 0.2,
            'network': 0.1
        }
        
        # Alert thresholds
        self.alert_thresholds = {
            'cpu_high': 80.0,
            'memory_risk': 85.0,
            'disk_critical': 90.0,
            'network_high': 1000.0  # MB
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("🔧 Optimization engine initialized")
    
    def calculate_moving_averages(self, cpu: float, memory: float, 
                                disk: float, network: float) -> Dict:
        """
        Calculate moving averages for system metrics.
        
        Args:
            cpu: Current CPU usage
            memory: Current memory usage
            disk: Current disk usage
            network: Current network usage
            
        Returns:
            Dict: Moving averages for all metrics
        """
        # Update buffers
        self.cpu_ma_buffer.append(cpu)
        self.memory_ma_buffer.append(memory)
        self.disk_ma_buffer.append(disk)
        self.network_ma_buffer.append(network)
        
        # Calculate moving averages
        moving_averages = {
            'cpu_ma': np.mean(list(self.cpu_ma_buffer)),
            'memory_ma': np.mean(list(self.memory_ma_buffer)),
            'disk_ma': np.mean(list(self.disk_ma_buffer)),
            'network_ma': np.mean(list(self.network_ma_buffer)),
            'window_size': len(self.cpu_ma_buffer)
        }
        
        return moving_averages
    
    def calculate_health_score(self, cpu: float, memory: float, 
                             disk: float, network: float) -> Dict:
        """
        Calculate system health score using weighted formula.
        Health Score = 100 - (0.4*CPU + 0.3*Memory + 0.2*Disk + 0.1*Network)
        
        Args:
            cpu: CPU usage percentage
            memory: Memory usage percentage
            disk: Disk usage percentage
            network: Network usage percentage (normalized to 0-100)
            
        Returns:
            Dict: Health score and risk assessment
        """
        # Normalize network usage (assuming max 1000 MB = 100%)
        network_normalized = min(100, (network / 1000.0) * 100)
        
        # Calculate weighted contributions
        cpu_contribution = self.health_weights['cpu'] * cpu
        memory_contribution = self.health_weights['memory'] * memory
        disk_contribution = self.health_weights['disk'] * disk
        network_contribution = self.health_weights['network'] * network_normalized
        
        # Calculate health score
        health_score = 100 - (cpu_contribution + memory_contribution + 
                            disk_contribution + network_contribution)
        
        # Ensure score is within bounds
        health_score = max(0, min(100, health_score))
        
        # Determine risk level
        if health_score >= 80:
            risk_level = 'low'
        elif health_score >= 60:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'health_score': round(health_score, 2),
            'risk_level': risk_level,
            'contributions': {
                'cpu': round(cpu_contribution, 2),
                'memory': round(memory_contribution, 2),
                'disk': round(disk_contribution, 2),
                'network': round(network_contribution, 2)
            },
            'weights': self.health_weights,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_intelligent_alerts(self, current_metrics: Dict, 
                                  predicted_metrics: Dict = None) -> List[Dict]:
        """
        Generate intelligent alerts based on current and predicted metrics.
        
        Args:
            current_metrics: Current system metrics
            predicted_metrics: Predicted metrics (optional)
            
        Returns:
            List[Dict]: List of alerts
        """
        alerts = []
        
        cpu = current_metrics.get('cpu', 0)
        memory = current_metrics.get('memory', 0)
        disk = current_metrics.get('disk', 0)
        network = current_metrics.get('network', 0)
        
        # Current metric alerts
        if cpu > self.alert_thresholds['cpu_high']:
            alerts.append({
                'type': 'high_load_alert',
                'severity': 'high' if cpu > 90 else 'medium',
                'message': f'High CPU Load: {cpu:.1f}%',
                'metric': 'cpu',
                'current_value': cpu,
                'threshold': self.alert_thresholds['cpu_high'],
                'timestamp': datetime.now().isoformat()
            })
        
        if memory > self.alert_thresholds['memory_risk']:
            alerts.append({
                'type': 'memory_risk_alert',
                'severity': 'high' if memory > 95 else 'medium',
                'message': f'Memory Risk: {memory:.1f}%',
                'metric': 'memory',
                'current_value': memory,
                'threshold': self.alert_thresholds['memory_risk'],
                'timestamp': datetime.now().isoformat()
            })
        
        if disk > self.alert_thresholds['disk_critical']:
            alerts.append({
                'type': 'disk_critical_alert',
                'severity': 'high',
                'message': f'Disk Critical: {disk:.1f}%',
                'metric': 'disk',
                'current_value': disk,
                'threshold': self.alert_thresholds['disk_critical'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Predicted metric alerts
        if predicted_metrics:
            pred_cpu = predicted_metrics.get('predicted_cpu', 0)
            pred_memory = predicted_metrics.get('predicted_memory', 0)
            
            if pred_cpu > 85:
                alerts.append({
                    'type': 'predicted_cpu_alert',
                    'severity': 'medium',
                    'message': f'Predicted High CPU: {pred_cpu:.1f}%',
                    'metric': 'predicted_cpu',
                    'predicted_value': pred_cpu,
                    'threshold': 85,
                    'timestamp': datetime.now().isoformat()
                })
            
            if pred_memory > 90:
                alerts.append({
                    'type': 'predicted_memory_alert',
                    'severity': 'high',
                    'message': f'Predicted Memory Critical: {pred_memory:.1f}%',
                    'metric': 'predicted_memory',
                    'predicted_value': pred_memory,
                    'threshold': 90,
                    'timestamp': datetime.now().isoformat()
                })
        
        return alerts
    
    def generate_optimization_suggestions(self, current_metrics: Dict, 
                                        predicted_metrics: Dict = None,
                                        alerts: List[Dict] = None) -> List[Dict]:
        """
        Generate optimization suggestions based on system state.
        
        Args:
            current_metrics: Current system metrics
            predicted_metrics: Predicted metrics (optional)
            alerts: Current alerts (optional)
            
        Returns:
            List[Dict]: List of optimization suggestions
        """
        suggestions = []
        
        cpu = current_metrics.get('cpu', 0)
        memory = current_metrics.get('memory', 0)
        disk = current_metrics.get('disk', 0)
        
        # CPU optimization suggestions
        if cpu > 80:
            suggestions.append({
                'category': 'cpu_optimization',
                'priority': 'high' if cpu > 90 else 'medium',
                'suggestion': 'Reduce process priorities for non-critical applications',
                'details': f'Current CPU usage: {cpu:.1f}%. Consider closing unnecessary applications or reducing background processes.',
                'action_type': 'process_priority_reduction',
                'estimated_impact': 'High',
                'timestamp': datetime.now().isoformat()
            })
        
        if predicted_metrics and predicted_metrics.get('predicted_cpu', 0) > 85:
            suggestions.append({
                'category': 'predictive_cpu_optimization',
                'priority': 'medium',
                'suggestion': 'Proactive process priority reduction recommended',
                'details': f'Predicted CPU usage: {predicted_metrics["predicted_cpu"]:.1f}%. Take preventive action now.',
                'action_type': 'proactive_process_management',
                'estimated_impact': 'Medium',
                'timestamp': datetime.now().isoformat()
            })
        
        # Memory optimization suggestions
        if memory > 85:
            suggestions.append({
                'category': 'memory_optimization',
                'priority': 'high' if memory > 95 else 'medium',
                'suggestion': 'Clear system cache and close memory-intensive applications',
                'details': f'Current memory usage: {memory:.1f}%. Consider restarting memory-heavy applications or clearing cache.',
                'action_type': 'cache_cleanup',
                'estimated_impact': 'High',
                'timestamp': datetime.now().isoformat()
            })
        
        if predicted_metrics and predicted_metrics.get('predicted_memory', 0) > 90:
            suggestions.append({
                'category': 'predictive_memory_optimization',
                'priority': 'high',
                'suggestion': 'Immediate cache cleanup recommended',
                'details': f'Predicted memory usage: {predicted_metrics["predicted_memory"]:.1f}%. Critical action required.',
                'action_type': 'immediate_cache_cleanup',
                'estimated_impact': 'High',
                'timestamp': datetime.now().isoformat()
            })
        
        # Disk optimization suggestions
        if disk > 85:
            suggestions.append({
                'category': 'disk_optimization',
                'priority': 'high' if disk > 95 else 'medium',
                'suggestion': 'Clean temporary files and run disk cleanup',
                'details': f'Current disk usage: {disk:.1f}%. Consider removing temporary files, logs, or unused applications.',
                'action_type': 'disk_cleanup',
                'estimated_impact': 'Medium',
                'timestamp': datetime.now().isoformat()
            })
        
        # General performance suggestions
        if cpu > 70 and memory > 70:
            suggestions.append({
                'category': 'general_optimization',
                'priority': 'medium',
                'suggestion': 'System restart recommended for optimal performance',
                'details': 'Both CPU and memory usage are elevated. A system restart may help clear accumulated processes.',
                'action_type': 'system_restart',
                'estimated_impact': 'High',
                'timestamp': datetime.now().isoformat()
            })
        
        # Performance tuning suggestions
        if len(suggestions) == 0 and (cpu > 50 or memory > 60):
            suggestions.append({
                'category': 'performance_tuning',
                'priority': 'low',
                'suggestion': 'Consider performance monitoring and optimization',
                'details': 'System performance could be improved with regular monitoring and maintenance.',
                'action_type': 'performance_monitoring',
                'estimated_impact': 'Low',
                'timestamp': datetime.now().isoformat()
            })
        
        return suggestions
    
    def calculate_optimization_impact(self, suggestions: List[Dict], 
                                   current_metrics: Dict) -> Dict:
        """
        Calculate potential impact of optimization suggestions.
        
        Args:
            suggestions: List of optimization suggestions
            current_metrics: Current system metrics
            
        Returns:
            Dict: Impact analysis
        """
        if not suggestions:
            return {'total_suggestions': 0, 'potential_improvement': 0}
        
        # Estimate potential improvements based on suggestion types
        impact_estimates = {
            'process_priority_reduction': {'cpu': -15, 'memory': -5},
            'cache_cleanup': {'cpu': -5, 'memory': -20},
            'disk_cleanup': {'disk': -10},
            'system_restart': {'cpu': -25, 'memory': -30, 'disk': -5},
            'performance_monitoring': {'cpu': -5, 'memory': -5}
        }
        
        total_cpu_improvement = 0
        total_memory_improvement = 0
        total_disk_improvement = 0
        
        high_priority_count = 0
        medium_priority_count = 0
        low_priority_count = 0
        
        for suggestion in suggestions:
            action_type = suggestion.get('action_type', '')
            priority = suggestion.get('priority', 'low')
            
            # Count priorities
            if priority == 'high':
                high_priority_count += 1
            elif priority == 'medium':
                medium_priority_count += 1
            else:
                low_priority_count += 1
            
            # Calculate improvements
            if action_type in impact_estimates:
                improvements = impact_estimates[action_type]
                total_cpu_improvement += improvements.get('cpu', 0)
                total_memory_improvement += improvements.get('memory', 0)
                total_disk_improvement += improvements.get('disk', 0)
        
        # Calculate potential new values
        current_cpu = current_metrics.get('cpu', 0)
        current_memory = current_metrics.get('memory', 0)
        current_disk = current_metrics.get('disk', 0)
        
        potential_cpu = max(0, current_cpu + total_cpu_improvement)
        potential_memory = max(0, current_memory + total_memory_improvement)
        potential_disk = max(0, current_disk + total_disk_improvement)
        
        return {
            'total_suggestions': len(suggestions),
            'priority_breakdown': {
                'high': high_priority_count,
                'medium': medium_priority_count,
                'low': low_priority_count
            },
            'potential_improvements': {
                'cpu': abs(total_cpu_improvement),
                'memory': abs(total_memory_improvement),
                'disk': abs(total_disk_improvement)
            },
            'projected_values': {
                'cpu': potential_cpu,
                'memory': potential_memory,
                'disk': potential_disk
            },
            'overall_improvement_score': (abs(total_cpu_improvement) + 
                                        abs(total_memory_improvement) + 
                                        abs(total_disk_improvement)) / 3
        }
    
    def get_optimization_summary(self, current_metrics: Dict, 
                               predicted_metrics: Dict = None) -> Dict:
        """
        Get comprehensive optimization summary.
        
        Args:
            current_metrics: Current system metrics
            predicted_metrics: Predicted metrics (optional)
            
        Returns:
            Dict: Complete optimization analysis
        """
        # Calculate moving averages
        moving_averages = self.calculate_moving_averages(
            current_metrics.get('cpu', 0),
            current_metrics.get('memory', 0),
            current_metrics.get('disk', 0),
            current_metrics.get('network', 0)
        )
        
        # Calculate health score
        health_info = self.calculate_health_score(
            current_metrics.get('cpu', 0),
            current_metrics.get('memory', 0),
            current_metrics.get('disk', 0),
            current_metrics.get('network', 0)
        )
        
        # Generate alerts
        alerts = self.generate_intelligent_alerts(current_metrics, predicted_metrics)
        
        # Generate suggestions
        suggestions = self.generate_optimization_suggestions(
            current_metrics, predicted_metrics, alerts
        )
        
        # Calculate impact
        impact_analysis = self.calculate_optimization_impact(suggestions, current_metrics)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'current_metrics': current_metrics,
            'predicted_metrics': predicted_metrics,
            'moving_averages': moving_averages,
            'health_assessment': health_info,
            'alerts': alerts,
            'optimization_suggestions': suggestions,
            'impact_analysis': impact_analysis,
            'summary': {
                'health_score': health_info['health_score'],
                'risk_level': health_info['risk_level'],
                'alert_count': len(alerts),
                'suggestion_count': len(suggestions),
                'high_priority_actions': impact_analysis['priority_breakdown']['high']
            }
        }