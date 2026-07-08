import numpy as np
import pandas as pd
from scipy.stats import skew

class TimeSeriesFeatureExtractor:
    def __init__(self, window_size=30): # 30 frames at 10Hz = 3 seconds
        self.window_size = window_size

    def extract_matrix(self, raw_signal, label_id):
        """Transforms a 1D raw stream into a structured ML feature matrix."""
        features = []
        labels = []
        
        # Slide a window across the timeline
        for i in range(len(raw_signal) - self.window_size + 1):
            window = raw_signal[i:i + self.window_size]
            
            # Compute advanced features required by management
            mean_val = np.mean(window)
            std_dev = np.std(window)
            skewness = skew(window)
            
            # Handle edge case for zero variance fields
            if np.isnan(skewness): 
                skewness = 0.0
                
            # First-order variance / Delta Velocity (rate of change between consecutive points)
            delta_velocity = np.var(np.diff(window))
            
            features.append([mean_val, std_dev, skewness, delta_velocity])
            labels.append(label_id)
            
        return np.array(features), np.array(labels)