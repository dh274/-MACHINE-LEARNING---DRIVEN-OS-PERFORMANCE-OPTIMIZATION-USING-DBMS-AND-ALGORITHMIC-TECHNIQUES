"""
Machine Learning Predictor for OS Performance Optimization
Implements Linear Regression for CPU and Memory usage prediction.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import joblib
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List
import os

class PerformancePredictor:
    """ML-based performance predictor using Linear Regression."""
    
    def __init__(self, model_dir: str = 'models'):
        """
        Initialize the performance predictor.
        
        Args:
            model_dir: Directory to save/load trained models
        """
        self.model_dir = model_dir
        self.cpu_model = LinearRegression()
        self.memory_model = LinearRegression()
        self.scaler = StandardScaler()
        
        self.is_trained = False
        self.last_training_time = None
        self.model_accuracy = {'cpu_r2': 0, 'memory_r2': 0, 'cpu_rmse': 0, 'memory_rmse': 0}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create model directory
        os.makedirs(model_dir, exist_ok=True)
        
        # Try to load existing models
        self.load_models()
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare features for ML training/prediction.
        
        Args:
            df: DataFrame with system metrics
            
        Returns:
            Tuple of (features, cpu_targets, memory_targets)
        """
        if df.empty or len(df) < 2:
            raise ValueError("Insufficient data for feature preparation")
        
        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Create time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['minute'] = pd.to_datetime(df['timestamp']).dt.minute
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Create lag features (previous values)
        df['cpu_lag1'] = df['cpu'].shift(1)
        df['memory_lag1'] = df['memory'].shift(1)
        df['disk_lag1'] = df['disk'].shift(1)
        df['network_lag1'] = df['network'].shift(1)
        
        # Create moving averages
        df['cpu_ma3'] = df['cpu'].rolling(window=3, min_periods=1).mean()
        df['memory_ma3'] = df['memory'].rolling(window=3, min_periods=1).mean()
        
        # Create trend features
        df['cpu_trend'] = df['cpu'].diff()
        df['memory_trend'] = df['memory'].diff()
        
        # Drop rows with NaN values
        df = df.dropna()
        
        if df.empty:
            raise ValueError("No valid data after feature engineering")
        
        # Select features
        feature_columns = [
            'hour', 'minute', 'day_of_week',
            'cpu_lag1', 'memory_lag1', 'disk_lag1', 'network_lag1',
            'cpu_ma3', 'memory_ma3', 'cpu_trend', 'memory_trend',
            'disk', 'network'
        ]
        
        features = df[feature_columns].values
        cpu_targets = df['cpu'].values
        memory_targets = df['memory'].values
        
        return features, cpu_targets, memory_targets
    
    def train_models(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """
        Train Linear Regression models for CPU and Memory prediction.
        
        Args:
            df: Training data DataFrame
            test_size: Fraction of data to use for testing
            
        Returns:
            Dict: Training results and model performance metrics
        """
        try:
            self.logger.info("🤖 Starting ML model training...")
            
            # Prepare features
            features, cpu_targets, memory_targets = self.prepare_features(df)
            
            if len(features) < 10:
                raise ValueError(f"Insufficient data for training: {len(features)} samples (need at least 10)")
            
            # Split data
            X_train, X_test, y_cpu_train, y_cpu_test, y_mem_train, y_mem_test = train_test_split(
                features, cpu_targets, memory_targets, test_size=test_size, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train CPU model
            self.cpu_model.fit(X_train_scaled, y_cpu_train)
            cpu_pred = self.cpu_model.predict(X_test_scaled)
            
            # Train Memory model
            self.memory_model.fit(X_train_scaled, y_mem_train)
            memory_pred = self.memory_model.predict(X_test_scaled)
            
            # Calculate performance metrics
            cpu_r2 = r2_score(y_cpu_test, cpu_pred)
            cpu_rmse = np.sqrt(mean_squared_error(y_cpu_test, cpu_pred))
            memory_r2 = r2_score(y_mem_test, memory_pred)
            memory_rmse = np.sqrt(mean_squared_error(y_mem_test, memory_pred))
            
            self.model_accuracy = {
                'cpu_r2': cpu_r2,
                'cpu_rmse': cpu_rmse,
                'memory_r2': memory_r2,
                'memory_rmse': memory_rmse,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            self.is_trained = True
            self.last_training_time = datetime.now()
            
            # Save models
            self.save_models()
            
            self.logger.info(f"✅ Models trained successfully!")
            self.logger.info(f"   CPU Model - R²: {cpu_r2:.3f}, RMSE: {cpu_rmse:.2f}")
            self.logger.info(f"   Memory Model - R²: {memory_r2:.3f}, RMSE: {memory_rmse:.2f}")
            
            return self.model_accuracy
            
        except Exception as e:
            self.logger.error(f"❌ Error training models: {e}")
            raise
    
    def predict_next_values(self, current_metrics: Dict, horizon_minutes: int = 5) -> Dict:
        """
        Predict CPU and Memory usage for the next N minutes.
        
        Args:
            current_metrics: Current system metrics
            horizon_minutes: Prediction horizon in minutes
            
        Returns:
            Dict: Prediction results
        """
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        try:
            # Create feature vector from current metrics
            now = datetime.now()
            
            # Simulate recent history for feature creation
            # In a real scenario, you'd get this from the database
            recent_data = {
                'timestamp': [now - timedelta(minutes=i) for i in range(5, 0, -1)] + [now],
                'cpu': [current_metrics.get('cpu', 0)] * 6,
                'memory': [current_metrics.get('memory', 0)] * 6,
                'disk': [current_metrics.get('disk', 0)] * 6,
                'network': [current_metrics.get('network', 0)] * 6
            }
            
            df = pd.DataFrame(recent_data)
            features, _, _ = self.prepare_features(df)
            
            if len(features) == 0:
                raise ValueError("Could not prepare features for prediction")
            
            # Use the latest feature vector
            latest_features = features[-1:] if len(features) > 0 else features
            features_scaled = self.scaler.transform(latest_features)
            
            # Make predictions
            predicted_cpu = self.cpu_model.predict(features_scaled)[0]
            predicted_memory = self.memory_model.predict(features_scaled)[0]
            
            # Ensure predictions are within reasonable bounds
            predicted_cpu = max(0, min(100, predicted_cpu))
            predicted_memory = max(0, min(100, predicted_memory))
            
            prediction_result = {
                'predicted_cpu': round(predicted_cpu, 2),
                'predicted_memory': round(predicted_memory, 2),
                'prediction_horizon_minutes': horizon_minutes,
                'prediction_time': now.isoformat(),
                'model_accuracy': self.model_accuracy,
                'confidence': self._calculate_confidence(predicted_cpu, predicted_memory)
            }
            
            self.logger.info(f"🔮 Prediction: CPU={predicted_cpu:.1f}%, Memory={predicted_memory:.1f}%")
            
            return prediction_result
            
        except Exception as e:
            self.logger.error(f"❌ Error making prediction: {e}")
            raise
    
    def _calculate_confidence(self, cpu_pred: float, memory_pred: float) -> str:
        """
        Calculate prediction confidence based on model accuracy.
        
        Args:
            cpu_pred: Predicted CPU value
            memory_pred: Predicted memory value
            
        Returns:
            str: Confidence level (high/medium/low)
        """
        avg_r2 = (self.model_accuracy['cpu_r2'] + self.model_accuracy['memory_r2']) / 2
        
        if avg_r2 > 0.8:
            return 'high'
        elif avg_r2 > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def save_models(self):
        """Save trained models to disk."""
        try:
            joblib.dump(self.cpu_model, os.path.join(self.model_dir, 'cpu_model.pkl'))
            joblib.dump(self.memory_model, os.path.join(self.model_dir, 'memory_model.pkl'))
            joblib.dump(self.scaler, os.path.join(self.model_dir, 'scaler.pkl'))
            joblib.dump(self.model_accuracy, os.path.join(self.model_dir, 'model_accuracy.pkl'))
            
            self.logger.info("✅ Models saved successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving models: {e}")
    
    def load_models(self):
        """Load trained models from disk."""
        try:
            cpu_model_path = os.path.join(self.model_dir, 'cpu_model.pkl')
            memory_model_path = os.path.join(self.model_dir, 'memory_model.pkl')
            scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
            accuracy_path = os.path.join(self.model_dir, 'model_accuracy.pkl')
            
            if all(os.path.exists(path) for path in [cpu_model_path, memory_model_path, scaler_path]):
                self.cpu_model = joblib.load(cpu_model_path)
                self.memory_model = joblib.load(memory_model_path)
                self.scaler = joblib.load(scaler_path)
                
                if os.path.exists(accuracy_path):
                    self.model_accuracy = joblib.load(accuracy_path)
                
                self.is_trained = True
                self.logger.info("✅ Models loaded successfully")
            else:
                self.logger.info("ℹ️ No pre-trained models found")
                
        except Exception as e:
            self.logger.error(f"❌ Error loading models: {e}")
    
    def get_model_info(self) -> Dict:
        """Get information about trained models."""
        return {
            'is_trained': self.is_trained,
            'last_training_time': self.last_training_time.isoformat() if self.last_training_time else None,
            'model_accuracy': self.model_accuracy,
            'cpu_model_features': len(self.cpu_model.coef_) if self.is_trained else 0,
            'memory_model_features': len(self.memory_model.coef_) if self.is_trained else 0
        }