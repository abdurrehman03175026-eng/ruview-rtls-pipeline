import numpy as np

class SignalFilterPipeline:
    def __init__(self, window_size=5, process_variance=0.1, measurement_variance=4.0):
        """
        Production-grade DSP Pipeline separating outlier scrubbing from trend estimation.
        """
        self.window_size = window_size
        self.buffer = []
        
        # Kalman State Parameters
        self.Q = process_variance
        self.R = measurement_variance
        self.x = -60.0  # Initial state estimate (typical baseline RSSI)
        self.P = 1.0    # Initial estimation error covariance

    def apply_filters(self, raw_rssi: float) -> float:
        """
        Applies a sequential two-stage processing pipeline:
        Stage 1: Hampel Filter (Rolling MAD) for transient outlier scrubbing.
        Stage 2: 1D Linear Kalman Filter for localized noise suppression.
        """
        # Maintain rolling window buffer
        self.buffer.append(raw_rssi)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
            
        # --- Stage 1: Hampel Filter / Rolling MAD Outlier Scrubbing ---
        clean_rssi = raw_rssi
        if len(self.buffer) == self.window_size:
            median = np.median(self.buffer)
            mad = np.median(np.abs(np.array(self.buffer) - median))
            
            # Use threshold factor scaling (4.5 * MAD matches standard statistical outbounds)
            threshold = max(4.5 * mad, 2.0) # Prevents divide-by-zero on flat signals
            
            # Scrub value if it exceeds acceptable variance limits
            if np.abs(raw_rssi - median) > threshold:
                clean_rssi = median  # Replace outlier with rolling median

        # --- Stage 2: Linear Kalman Filter Step ---
        self.P = self.P + self.Q                                    # Time Update (Predict)
        kalman_gain = self.P / (self.P + self.R)                    # Measurement Update (Gain)
        self.x = self.x + kalman_gain * (clean_rssi - self.x)       # Update State Estimate
        self.P = (1 - kalman_gain) * self.P                         # Update Covariance
        
        return self.x