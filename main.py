"""
Main Application for ML-Driven OS Performance Optimization
Orchestrates system monitoring, database storage, and ML-based optimization.
"""

import time
import json
import schedule
from datetime import datetime, timedelta
from typing import Dict, Any
import argparse

from src.system_monitor import SystemMonitor
from src.database_manager import DatabaseManager
from src.ml_optimizer import PerformancePredictor, AnomalyDetector, PerformanceOptimizer


class PerformanceOptimizationSystem:
    """Main system orchestrating all components."""
    
    def __init__(self, db_path: str = "data/performance_metrics.db"):
        """Initialize the performance optimization system."""
        self.monitor = SystemMonitor(collection_interval=30)  # 30-second intervals
        self.db = DatabaseManager(db_path)
        self.predictor = PerformancePredictor()
        self.anomaly_detector = AnomalyDetector()
        self.optimizer = PerformanceOptimizer()
        
        self.is_running = False
        self.models_trained = False
    
    def collect_and_store_metrics(self):
        """Collect current metrics and store in database."""
        try:
            metrics = self.monitor.collect_all_metrics()
            success = self.db.store_metrics(metrics)
            
            if success:
                print(f"✓ Metrics collected and stored at {metrics['timestamp']}")
                
                # Check for anomalies if model is trained
                if self.models_trained:
                    anomaly_result = self.anomaly_detector.detect_anomaly(metrics)
                    if anomaly_result['is_anomaly']:
                        print(f"⚠️  ANOMALY DETECTED: {anomaly_result['severity']} severity "
                              f"(score: {anomaly_result['anomaly_score']:.3f})")
                        
                        # Generate recommendations for anomalous behavior
                        recommendations = self.optimizer.generate_optimization_recommendations(metrics)
                        if recommendations:
                            print("🔧 Optimization Recommendations:")
                            for rec in recommendations:
                                print(f"   - {rec['recommendation']} ({rec['priority']} priority)")
                
                return metrics
            else:
                print("❌ Failed to store metrics")
                return None
                
        except Exception as e:
            print(f"❌ Error in metric collection: {e}")
            return None
    
    def train_ml_models(self, hours_of_data: int = 24):
        """Train ML models using historical data."""
        try:
            print(f"🤖 Training ML models using last {hours_of_data} hours of data...")
            
            # Get training data
            df = self.db.get_recent_metrics(hours_of_data)
            
            if len(df) < 20:
                print(f"⚠️  Insufficient data for training ({len(df)} samples). Need at least 20 samples.")
                return False
            
            # Train performance predictor
            predictor_performance = self.predictor.train_models(df)
            print(f"✓ Performance Predictor trained:")
            print(f"   CPU R²: {predictor_performance['cpu_r2']:.3f}, RMSE: {predictor_performance['cpu_rmse']:.2f}")
            print(f"   Memory R²: {predictor_performance['memory_r2']:.3f}, RMSE: {predictor_performance['memory_rmse']:.2f}")
            
            # Train anomaly detector
            anomaly_summary = self.anomaly_detector.train(df)
            print(f"✓ Anomaly Detector trained:")
            print(f"   Training samples: {anomaly_summary['training_samples']}")
            print(f"   Anomaly rate: {anomaly_summary['anomaly_rate']:.1%}")
            
            # Analyze performance patterns
            patterns = self.optimizer.analyze_performance_patterns(df)
            print(f"✓ Performance patterns analyzed:")
            for cluster_name, cluster_info in patterns.items():
                if isinstance(cluster_info, dict) and 'performance_level' in cluster_info:
                    print(f"   {cluster_name}: {cluster_info['performance_level']} "
                          f"({cluster_info['size']} samples)")
            
            self.models_trained = True
            return True
            
        except Exception as e:
            print(f"❌ Error training ML models: {e}")
            return False
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        try:
            # Get performance summary
            summary = self.db.get_performance_summary(24)
            
            # Get current metrics
            current_metrics = self.monitor.collect_all_metrics()
            
            # Generate predictions if models are trained
            predictions = None
            if self.models_trained:
                try:
                    predictions = self.predictor.predict_resource_usage(current_metrics)
                except Exception as e:
                    print(f"⚠️  Prediction error: {e}")
            
            # Get optimization recommendations
            recommendations = self.optimizer.generate_optimization_recommendations(current_metrics)
            
            # Detect anomalies in recent data
            anomalies = self.db.identify_performance_anomalies()
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'current_metrics': {
                    'cpu_percent': current_metrics.get('cpu', {}).get('cpu_percent', 0),
                    'memory_percent': current_metrics.get('memory', {}).get('virtual_memory', {}).get('percent', 0),
                    'disk_percent': current_metrics.get('disk', {}).get('disk_usage', {}).get('percent', 0)
                },
                'performance_summary': summary,
                'predictions': predictions,
                'recommendations': recommendations,
                'recent_anomalies': len(anomalies),
                'models_trained': self.models_trained
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating performance report: {e}")
            return {'error': str(e)}
    
    def print_performance_report(self):
        """Print formatted performance report."""
        report = self.generate_performance_report()
        
        print("\n" + "="*60)
        print("📊 PERFORMANCE OPTIMIZATION REPORT")
        print("="*60)
        print(f"Generated: {report['timestamp']}")
        
        # Current metrics
        current = report['current_metrics']
        print(f"\n🔍 Current System Status:")
        print(f"   CPU Usage: {current['cpu_percent']:.1f}%")
        print(f"   Memory Usage: {current['memory_percent']:.1f}%")
        print(f"   Disk Usage: {current['disk_percent']:.1f}%")
        
        # Predictions
        if report['predictions']:
            pred = report['predictions']
            print(f"\n🔮 Predictions (next {pred['prediction_horizon_hours']} hour):")
            print(f"   Predicted CPU: {pred['predicted_cpu_percent']:.1f}%")
            print(f"   Predicted Memory: {pred['predicted_memory_percent']:.1f}%")
        
        # Recommendations
        if report['recommendations']:
            print(f"\n🔧 Optimization Recommendations:")
            for rec in report['recommendations']:
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡"
                print(f"   {priority_icon} {rec['recommendation']}")
        else:
            print(f"\n✅ No optimization recommendations - system performing well!")
        
        # Anomalies
        if report['recent_anomalies'] > 0:
            print(f"\n⚠️  Recent anomalies detected: {report['recent_anomalies']}")
        
        print("="*60)
    
    def start_monitoring(self, train_interval_hours: int = 6):
        """Start continuous monitoring with periodic ML training."""
        print("🚀 Starting ML-Driven OS Performance Optimization System")
        print(f"   Monitoring interval: {self.monitor.collection_interval} seconds")
        print(f"   ML training interval: {train_interval_hours} hours")
        
        # Schedule tasks
        schedule.every(self.monitor.collection_interval).seconds.do(self.collect_and_store_metrics)
        schedule.every(train_interval_hours).hours.do(self.train_ml_models)
        schedule.every(1).hours.do(self.print_performance_report)
        
        # Initial training if we have data
        self.train_ml_models()
        
        # Initial report
        self.print_performance_report()
        
        self.is_running = True
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping performance optimization system...")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop the monitoring system."""
        self.is_running = False
        self.db.close()
        print("✅ Performance optimization system stopped")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='ML-Driven OS Performance Optimization')
    parser.add_argument('--mode', choices=['monitor', 'report', 'train'], default='monitor',
                       help='Operation mode: monitor (continuous), report (single), train (ML models)')
    parser.add_argument('--duration', type=int, default=None,
                       help='Monitoring duration in seconds (None for infinite)')
    parser.add_argument('--db-path', default='data/performance_metrics.db',
                       help='Database file path')
    
    args = parser.parse_args()
    
    # Create system instance
    system = PerformanceOptimizationSystem(args.db_path)
    
    if args.mode == 'monitor':
        # Continuous monitoring
        system.start_monitoring()
        
    elif args.mode == 'report':
        # Generate single report
        system.print_performance_report()
        
    elif args.mode == 'train':
        # Train ML models
        success = system.train_ml_models()
        if success:
            print("✅ ML models trained successfully")
        else:
            print("❌ Failed to train ML models")


if __name__ == "__main__":
    main()