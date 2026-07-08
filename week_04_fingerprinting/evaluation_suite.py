import numpy as np
from week_04_fingerprinting.feature_extractor import TimeSeriesFeatureExtractor
from week_04_fingerprinting.ablation_testbed import AblationModelTestbed

def generate_synthetic_profile(seed, baseline_rssi):
    """Generates continuous real-world simulated profile vectors."""
    np.random.seed(seed)
    base = np.full(300, baseline_rssi)
    noise = np.random.normal(0, 2.5, 300) + np.sin(np.linspace(0, 10, 300)) * 1.5
    return base + noise

def main():
    print("[System Initialization] Booting Week 4 Scene Classification Testing Suite...\n")
    
    # 1. Generate Raw Location Profiles (Class 1 = Desk, Class 2 = Doorway)
    desk_signal_train = generate_synthetic_profile(42, -52.0)
    door_signal_train = generate_synthetic_profile(43, -72.0)
    desk_signal_test = generate_synthetic_profile(44, -54.0)
    door_signal_test = generate_synthetic_profile(45, -74.0)
    
    # 2. Extract Window Matrices (3-Second Blocks)
    extractor = TimeSeriesFeatureExtractor(window_size=30)
    
    X_desk_tr, y_desk_tr = extractor.extract_matrix(desk_signal_train, 1)
    X_door_tr, y_door_tr = extractor.extract_matrix(door_signal_train, 2)
    X_train = np.vstack([X_desk_tr, X_door_tr])
    y_train = np.concatenate([y_desk_tr, y_door_tr])
    
    X_desk_te, y_desk_te = extractor.extract_matrix(desk_signal_test, 1)
    X_door_te, y_door_te = extractor.extract_matrix(door_signal_test, 2)
    X_test = np.vstack([X_desk_te, X_door_te])
    y_test = np.concatenate([y_desk_te, y_door_te])
    
    # 3. Define Ablation Configurations (0=Mean, 1=StdDev, 2=Skewness, 3=DeltaVelocity)
    scenarios = {
        "(1) Raw RSSI Averages Only": [0],
        "(2) RSSI Average + Rolling StdDev": [0, 1],
        "(3) Full Time-Series Feature Matrix": [0, 1, 2, 3]
    }
    
    print(f"{'Ablation Feature Configuration':<40} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10}")
    print("=" * 82)
    
    # Instantiate our new dedicated testbed engine
    testbed = AblationModelTestbed(n_neighbors=3)
    
    # Evaluate configurations sequentially
    for name, cols in scenarios.items():
        res = testbed.evaluate_feature_subset(X_train, y_train, X_test, y_test, cols)
        print(f"{name:<40} | {res['accuracy']:<10.4f} | {res['precision']:<10.4f} | {res['recall']:<10.4f}")

if __name__ == "__main__":
    main()