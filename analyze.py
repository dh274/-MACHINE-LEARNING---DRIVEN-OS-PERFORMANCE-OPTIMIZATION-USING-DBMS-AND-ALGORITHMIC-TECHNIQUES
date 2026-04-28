"""
Performance Analysis Script
Comprehensive analysis of system performance using ML and statistical methods.
"""

import argparse
import json
from datetime import datetime, timedelta
from src.database_manager import DatabaseManager
from src.ml_optimizer import PerformancePredictor, AnomalyDetector, PerformanceOptimizer
from src.visualizer import PerformanceVisualizer


def analyze_performance(hours: int = 24, generate_charts: bool = True, 
                       train_models: bool = True) -> dict:
    """
    Perform comprehensive performance analysis.
    
    Args:
        hours: Hours of data to analyze
        generate_charts: Whether to generate visualization charts
        train_models: Whether to train ML models
        
    Returns:
        Analysis results dictionary
    """
    print(f"🔍 Starting performance analysis for last {hours} hours...")
    
    # Initialize components
    db = DatabaseManager()
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'data_period_hours': hours,
        'models_trained': False,
        'charts_generated': False
    }
    
    try:
        # Get data
        print("📊 Retrieving performance data...")
        df = db.get_recent_metrics(hours)
        
        if df.empty:
            print("❌ No data available for analysis")
            return {'error': 'No data available'}
        
        print(f"✓ Retrieved {len(df)} data points")
        
        # Basic statistics
        print("📈 Computing basic statistics...")
        stats = {
            'data_points': len(df),
            'time_range': {
                'start': df['timestamp'].min().isoformat(),
                'end': df['timestamp'].max().isoformat()
            },
            'cpu_stats': {
                'mean': df['cpu_percent'].mean(),
                'max': df['cpu_percent'].max(),
                'min': df['cpu_percent'].min(),
                'std': df['cpu_percent'].std(),
                'high_usage_periods': len(df[df['cpu_percent'] > 80])
            },
            'memory_stats': {
                'mean': df['memory_percent'].mean(),
                'max': df['memory_percent'].max(),
                'min': df['memory_percent'].min(),
                'std': df['memory_percent'].std(),
                'high_usage_periods': len(df[df['memory_percent'] > 85])
            },
            'disk_stats': {
                'mean': df['disk_percent'].mean(),
                'max': df['disk_percent'].max(),
                'min': df['disk_percent'].min(),
                'std': df['disk_percent'].std(),
                'high_usage_periods': len(df[df['disk_percent'] > 90])
            }
        }
        results['basic_statistics'] = stats
        
        # Performance summary from database
        print("📋 Getting performance summary...")
        summary = db.get_performance_summary(hours)
        results['performance_summary'] = summary
        
        # Anomaly detection from database
        print("🚨 Detecting anomalies...")
        anomalies = db.identify_performance_anomalies()
        results['statistical_anomalies'] = {
            'count': len(anomalies),
            'anomalies': anomalies[:10]  # Top 10 anomalies
        }
        
        # ML Analysis
        if train_models and len(df) >= 20:
            print("🤖 Training ML models...")
            
            # Performance predictor
            predictor = PerformancePredictor()
            try:
                predictor_performance = predictor.train_models(df)
                results['predictor_performance'] = predictor_performance
                print(f"✓ Performance predictor trained (CPU R²: {predictor_performance['cpu_r2']:.3f})")
            except Exception as e:
                print(f"⚠️  Predictor training failed: {e}")
                results['predictor_error'] = str(e)
            
            # Anomaly detector
            anomaly_detector = AnomalyDetector()
            try:
                anomaly_summary = anomaly_detector.train(df)
                results['anomaly_detector_summary'] = anomaly_summary
                print(f"✓ Anomaly detector trained (anomaly rate: {anomaly_summary['anomaly_rate']:.1%})")
            except Exception as e:
                print(f"⚠️  Anomaly detector training failed: {e}")
                results['anomaly_detector_error'] = str(e)
            
            # Performance optimizer
            optimizer = PerformanceOptimizer()
            try:
                patterns = optimizer.analyze_performance_patterns(df)
                results['performance_patterns'] = patterns
                print("✓ Performance patterns analyzed")
            except Exception as e:
                print(f"⚠️  Pattern analysis failed: {e}")
                results['pattern_analysis_error'] = str(e)
            
            results['models_trained'] = True
        
        # Generate visualizations
        if generate_charts:
            print("📊 Generating performance charts...")
            visualizer = PerformanceVisualizer()
            try:
                chart_files = visualizer.create_performance_dashboard(df)
                results['generated_charts'] = chart_files
                results['charts_generated'] = True
                print(f"✓ Generated {len(chart_files)} charts")
            except Exception as e:
                print(f"⚠️  Chart generation failed: {e}")
                results['chart_error'] = str(e)
        
        # Performance insights
        print("💡 Generating insights...")
        insights = generate_insights(stats, summary, anomalies)
        results['insights'] = insights
        
        print("✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        results['error'] = str(e)
    
    finally:
        db.close()
    
    return results


def generate_insights(stats: dict, summary: dict, anomalies: list) -> list:
    """Generate actionable insights from analysis results."""
    insights = []
    
    # CPU insights
    cpu_mean = stats['cpu_stats']['mean']
    cpu_high_periods = stats['cpu_stats']['high_usage_periods']
    
    if cpu_mean > 70:
        insights.append({
            'type': 'performance',
            'severity': 'high' if cpu_mean > 85 else 'medium',
            'message': f'High average CPU usage ({cpu_mean:.1f}%) indicates system stress',
            'recommendation': 'Consider CPU optimization or scaling'
        })
    
    if cpu_high_periods > 0:
        insights.append({
            'type': 'performance',
            'severity': 'medium',
            'message': f'{cpu_high_periods} periods of high CPU usage (>80%) detected',
            'recommendation': 'Identify and optimize CPU-intensive processes'
        })
    
    # Memory insights
    memory_mean = stats['memory_stats']['mean']
    memory_high_periods = stats['memory_stats']['high_usage_periods']
    
    if memory_mean > 80:
        insights.append({
            'type': 'performance',
            'severity': 'high' if memory_mean > 90 else 'medium',
            'message': f'High average memory usage ({memory_mean:.1f}%) may cause instability',
            'recommendation': 'Implement memory optimization or increase RAM'
        })
    
    # Disk insights
    disk_mean = stats['disk_stats']['mean']
    if disk_mean > 85:
        insights.append({
            'type': 'storage',
            'severity': 'high',
            'message': f'High disk usage ({disk_mean:.1f}%) requires attention',
            'recommendation': 'Clean up disk space or expand storage'
        })
    
    # Anomaly insights
    if len(anomalies) > 5:
        insights.append({
            'type': 'anomaly',
            'severity': 'medium',
            'message': f'{len(anomalies)} performance anomalies detected',
            'recommendation': 'Investigate anomalous behavior patterns'
        })
    
    # Stability insights
    cpu_std = stats['cpu_stats']['std']
    memory_std = stats['memory_stats']['std']
    
    if cpu_std > 20 or memory_std > 15:
        insights.append({
            'type': 'stability',
            'severity': 'medium',
            'message': 'High resource usage variability indicates unstable workload',
            'recommendation': 'Implement workload balancing and resource smoothing'
        })
    
    # Positive insights
    if cpu_mean < 50 and memory_mean < 60 and len(anomalies) < 3:
        insights.append({
            'type': 'positive',
            'severity': 'info',
            'message': 'System performance is stable and within optimal ranges',
            'recommendation': 'Continue current monitoring practices'
        })
    
    return insights


def print_analysis_report(results: dict):
    """Print formatted analysis report."""
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE PERFORMANCE ANALYSIS REPORT")
    print("="*80)
    print(f"Generated: {results['analysis_timestamp']}")
    print(f"Analysis Period: {results['data_period_hours']} hours")
    
    if 'error' in results:
        print(f"\n❌ Analysis Error: {results['error']}")
        return
    
    # Basic statistics
    if 'basic_statistics' in results:
        stats = results['basic_statistics']
        print(f"\n📈 BASIC STATISTICS")
        print(f"   Data Points: {stats['data_points']}")
        print(f"   Time Range: {stats['time_range']['start']} to {stats['time_range']['end']}")
        
        print(f"\n   CPU Usage:")
        print(f"      Average: {stats['cpu_stats']['mean']:.1f}%")
        print(f"      Peak: {stats['cpu_stats']['max']:.1f}%")
        print(f"      High Usage Periods: {stats['cpu_stats']['high_usage_periods']}")
        
        print(f"\n   Memory Usage:")
        print(f"      Average: {stats['memory_stats']['mean']:.1f}%")
        print(f"      Peak: {stats['memory_stats']['max']:.1f}%")
        print(f"      High Usage Periods: {stats['memory_stats']['high_usage_periods']}")
        
        print(f"\n   Disk Usage:")
        print(f"      Average: {stats['disk_stats']['mean']:.1f}%")
        print(f"      Peak: {stats['disk_stats']['max']:.1f}%")
    
    # ML Model Performance
    if results.get('models_trained'):
        print(f"\n🤖 MACHINE LEARNING ANALYSIS")
        
        if 'predictor_performance' in results:
            perf = results['predictor_performance']
            print(f"   Performance Predictor:")
            print(f"      CPU Prediction Accuracy (R²): {perf['cpu_r2']:.3f}")
            print(f"      Memory Prediction Accuracy (R²): {perf['memory_r2']:.3f}")
        
        if 'anomaly_detector_summary' in results:
            anom = results['anomaly_detector_summary']
            print(f"   Anomaly Detector:")
            print(f"      Training Samples: {anom['training_samples']}")
            print(f"      Anomaly Rate: {anom['anomaly_rate']:.1%}")
        
        if 'performance_patterns' in results:
            patterns = results['performance_patterns']
            print(f"   Performance Patterns:")
            for cluster_name, cluster_info in patterns.items():
                if isinstance(cluster_info, dict) and 'performance_level' in cluster_info:
                    print(f"      {cluster_name}: {cluster_info['performance_level']} "
                          f"({cluster_info['size']} samples)")
    
    # Anomalies
    if 'statistical_anomalies' in results:
        anomalies = results['statistical_anomalies']
        print(f"\n🚨 ANOMALY DETECTION")
        print(f"   Total Anomalies: {anomalies['count']}")
        if anomalies['anomalies']:
            print("   Recent Anomalies:")
            for anom in anomalies['anomalies'][:5]:
                print(f"      {anom['type']}: {anom['value']:.1f}% at {anom['timestamp']} "
                      f"({anom['severity']} severity)")
    
    # Insights
    if 'insights' in results:
        insights = results['insights']
        print(f"\n💡 KEY INSIGHTS & RECOMMENDATIONS")
        
        high_priority = [i for i in insights if i['severity'] == 'high']
        medium_priority = [i for i in insights if i['severity'] == 'medium']
        info_items = [i for i in insights if i['severity'] == 'info']
        
        if high_priority:
            print("   🔴 HIGH PRIORITY:")
            for insight in high_priority:
                print(f"      • {insight['message']}")
                print(f"        → {insight['recommendation']}")
        
        if medium_priority:
            print("   🟡 MEDIUM PRIORITY:")
            for insight in medium_priority:
                print(f"      • {insight['message']}")
                print(f"        → {insight['recommendation']}")
        
        if info_items:
            print("   ℹ️  INFORMATION:")
            for insight in info_items:
                print(f"      • {insight['message']}")
    
    # Generated files
    if results.get('charts_generated') and 'generated_charts' in results:
        print(f"\n📊 GENERATED VISUALIZATIONS")
        for chart_file in results['generated_charts']:
            print(f"   • {chart_file}")
    
    print("="*80)


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(description='Comprehensive Performance Analysis')
    parser.add_argument('--hours', type=int, default=24,
                       help='Hours of data to analyze (default: 24)')
    parser.add_argument('--no-charts', action='store_true',
                       help='Skip chart generation')
    parser.add_argument('--no-ml', action='store_true',
                       help='Skip ML model training')
    parser.add_argument('--output', type=str, default=None,
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    # Run analysis
    results = analyze_performance(
        hours=args.hours,
        generate_charts=not args.no_charts,
        train_models=not args.no_ml
    )
    
    # Print report
    print_analysis_report(results)
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {args.output}")


if __name__ == "__main__":
    main()