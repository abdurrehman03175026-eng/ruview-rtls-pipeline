import os
import numpy as np
import matplotlib.pyplot as plt
from week_03_fusion.fusion_engine import MultiNodeFusionEngine

def main():
    print("[System Initialization] Booting Week 3 Multi-Receiver Fusion Harness...")
    
    # Simulate a 360-degree rotation test over 150 frames (15 seconds)
    # As a person rotates, Node 1 gets blocked while Node 2 gets a clear line-of-sight
    np.random.seed(24)
    timeline = np.arange(150) * 0.1
    base_signal = -55.0
    noise_1 = np.random.normal(0, 1.5, 150)
    noise_2 = np.random.normal(0, 1.5, 150)
    
    # Simulate Node 1 getting blocked by body attenuation in the first half
    node_01_rssi = np.full(150, base_signal) + noise_1
    node_01_rssi[20:75] -= 14.0 # 14 dB human body attenuation drop
    
    # Simulate Node 2 getting blocked in the second half as the user rotates
    node_02_rssi = np.full(150, base_signal) + noise_2
    node_02_rssi[80:135] -= 15.0 # 15 dB human body attenuation drop
    
    # Package into spatial topology data structure
    topology_telemetry = {
        'receiver_node_01': node_01_rssi,
        'receiver_node_02': node_02_rssi
    }
    
    # Execute Network Fusion
    engine = MultiNodeFusionEngine()
    fused_spatial_stream = engine.fuse_max_unattenuated(topology_telemetry)
    
    # Quantify the exact reduction in human body attenuation degradation
    avg_single_receiver = np.mean([np.mean(node_01_rssi), np.mean(node_02_rssi)])
    avg_fused_receiver = np.mean(fused_spatial_stream)
    attenuation_recovery = np.abs(avg_fused_receiver - avg_single_receiver)
    
    print("\n" + "="*50)
    print(f"[FUSION ANALYSIS COMPLETED]")
    print(f"Mean Single-Node Signal Strength: {avg_single_receiver:.2f} dBm")
    print(f"Mean Fused-Topology Signal Strength: {avg_fused_receiver:.2f} dBm")
    print(f"Net Attenuation Recovery: +{attenuation_recovery:.2f} dB")
    print("="*50 + "\n")
    
    # Build Production Coverage Log Graph
    plt.figure(figsize=(10, 5))
    plt.plot(timeline, node_01_rssi, label='Satellite Node 01 (South)', color='#1f77b4', alpha=0.5, linestyle='--')
    plt.plot(timeline, node_02_rssi, label='Satellite Node 02 (North)', color='#ff7f0e', alpha=0.5, linestyle='-.')
    plt.plot(timeline, fused_spatial_stream, label='Fused Spatial Stream (Max Un-attenuated)', color='#2ca02c', linewidth=2.5)
    
    plt.title("Multi-Receiver Coverage Log Graph: 360-Degree Rotation Test", fontsize=12, fontweight='bold')
    plt.xlabel("Test Timeline Duration (Seconds)", fontsize=10)
    plt.ylabel("Received Signal Strength (RSSI/CSI Amplitude dBm)", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='lower left')
    
    os.makedirs('week_03_fusion', exist_ok=True)
    output_plot = os.path.join('week_03_fusion', 'multi_node_coverage_log.png')
    plt.savefig(output_plot, dpi=300)
    print(f"[Success] Multi-node coverage visualization saved to: {output_plot}")
    plt.show()

if __name__ == "__main__":
    main()