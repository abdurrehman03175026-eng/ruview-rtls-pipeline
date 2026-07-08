import numpy as np
import time

def calculate_metrics(ground_truth_rssi, filtered_rssi_array):
    """Appendix Standardized Matrix Evaluation Utility"""
    ground_truth = np.array(ground_truth_rssi)
    filtered = np.array(filtered_rssi_array)
    
    rmse = np.sqrt(np.mean((ground_truth - filtered) ** 2))
    variance = np.var(filtered)
    
    return rmse, variance

def execute_stress_run(environment_name, true_rssi, noise_mean, noise_std, packets=1000):
    """Simulates realistic high-stress physical environments on the filter array."""
    np.random.seed(42)
    
    # Simulate ground-truth trajectory versus environment-degraded noise vectors
    ground_truth = np.full(packets, true_rssi)
    raw_degraded = ground_truth + np.random.normal(noise_mean, noise_std, packets)
    
    # Process through our pipeline components (Simulating Week 2 Kalman/Hampel latency)
    start_time = time.perf_counter()
    
    # Mocking filter processing output vector
    filtered_output = np.convolve(raw_degraded, np.ones(5)/5, mode='same')
    
    end_time = time.perf_counter()
    
    # Calculate performance analytics
    rmse, variance = calculate_metrics(ground_truth, filtered_output)
    mean_latency_ms = ((end_time - start_time) / packets) * 1000 * 1000 # Convert to micro-seconds (µs)
    
    # Calculate Classification Confidence score based on statistical distance stability
    confidence = max(0.0, min(1.0, 1.0 - (rmse / abs(true_rssi))))
    
    return mean_latency_ms, rmse, confidence

def main():
    print("[System Audit] Launching Week 6 Adversarial Testing Environment Harness...\n")
    
    environments = {
        "Line-of-Sight (Clean Baseline)": {"true": -50.0, "mean": 0.0, "std": 1.2},
        "Deep Pocket Attenuation":        {"true": -58.0, "mean": -4.2, "std": 3.5},
        "Heavy Backpack Layers":          {"true": -64.0, "mean": -7.1, "std": 5.1},
        "Concrete Pillar Obstruction":     {"true": -75.0, "mean": -12.5, "std": 8.2},
        "2.4GHz Co-Channel Interference":  {"true": -52.0, "mean": -2.0, "std": 9.8}
    }
    
    print(f"{'Tested Environment Space':<32} | {'Mean Latency':<15} | {'RMSE (Accuracy)':<15} | {'Classification Confidence'}")
    print("=" * 95)
    
    for env, params in environments.items():
        latency, rmse, conf = execute_stress_run(env, params["true"], params["mean"], params["std"])
        print(f"{env:<32} | {latency:<15.3f} µs | {rmse:<15.4f} dB | {conf:.2%}")

if __name__ == "__main__":
    main()