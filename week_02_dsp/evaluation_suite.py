import os
import matplotlib.pyplot as plt
from week_02_dsp.data_loader import LargeDatasetStreamer
from week_02_dsp.tuning_matrix import DSPHyperparameterTuning

def main():
    print("[System initialization] Booting RuView DSP Pipeline Evaluation Harness...")
    
    # 1. Stream the real extracted dataset slice
    streamer = LargeDatasetStreamer()
    raw_rssi, ground_truth = streamer.load_official_slice()
    
    # 2. Run Grid Search Analysis
    tuner = DSPHyperparameterTuning()
    results = tuner.execute_grid_search(raw_rssi, ground_truth)
    
    # Print clean analytical dashboard
    print(f"\n{'Config ID':<12}{'Q (Process)':<15}{'R (Measurement)':<18}{'RMSE Metric':<12}")
    print("=" * 57)
    for res in results:
        print(f"#{res['permutation_id']:<11}{res['q']:<15.2f}{res['r']:<18.1f}{res['rmse']:<12.4f} dB")
        
    best_config = min(results, key=lambda x: x['rmse'])
    print(f"\n[Optimal Configuration Found] ID #{best_config['permutation_id']} | Q={best_config['q']} | R={best_config['r']} yields lowest RMSE: {best_config['rmse']:.4f} dB")

    # 3. Build Production Visualization Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Scatter Matrix Plot - Using pure numerical array coordinates to avoid conversion errors
    x_indices = [r['permutation_id'] for r in results]
    rmse_scores = [r['rmse'] for r in results]
    colors = ['#d62728' if r['permutation_id'] == best_config['permutation_id'] else '#1f77b4' for r in results]
    
    ax1.scatter(x_indices, rmse_scores, c=colors, s=180, edgecolors='black', zorder=3)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Set explicit ticks using the config parameter combinations
    labels = [f"Q={r['q']}\nR={r['r']}" for r in results]
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(labels, fontsize=8)
    
    ax1.set_title("Hyperparameter Grid Search: RMSE Tuning Matrix", fontsize=12, fontweight='bold')
    ax1.set_ylabel("RMSE Value (Lower is Better)", fontsize=10)
    ax1.set_xlabel("Parameter Configurations (Q / R Ratio)", fontsize=10)
    
    # Signal Trajectory Track Plot
    ax2.plot(raw_rssi, label='Raw Telemetry (Environmental Outliers/Noise)', color='#d62728', alpha=0.35, linestyle=':')
    ax2.plot(ground_truth, label='Stationary Ground Truth (-60dBm)', color='black', alpha=0.9, linewidth=2)
    ax2.plot(best_config['filtered_signal'], label=f"Scrubbed + Filtered Track (Q={best_config['q']}, R={best_config['r']})", color='#2ca02c', linewidth=2.5)
    
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.set_title("Trajectory Analysis: Signal Track vs Noise Suppression", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Telemetry Frame Counter")
    ax2.set_ylabel("RSSI Amplitude (dBm)")
    ax2.legend(loc='lower left')
    
    plt.tight_layout()
    output_path = os.path.join('week_02_dsp', 'dsp_tuning_matrix.png')
    plt.savefig(output_path, dpi=300)
    print(f"[Success] Multi-axis analytical plot safely compiled to: {output_path}")
    plt.show()

if __name__ == "__main__":
    main()