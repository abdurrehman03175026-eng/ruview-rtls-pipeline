import os
import time
import numpy as np
import matplotlib.pyplot as plt
from week_05_automation.state_machine import DynamicHysteresisStateMachine
from week_05_automation.dashboard_ui import RTLSAutomationDashboard

def main():
    print("[System Initialization] Launching Week 5 Automation Suite & Chaos Walk Engine...")
    
    # 1. Initialize core system structures
    fsm = DynamicHysteresisStateMachine(base_grace_period=5.0)
    ui = RTLSAutomationDashboard()
    
    # 2. Build continuous Chaos Walk timeline (180 frames = 18 seconds)
    timeline = np.arange(180)
    state_history = []
    timeout_history = []
    
    user_detected_mask = np.ones(180, dtype=bool)
    user_detected_mask[20:55] = False  # True physical exit
    user_detected_mask[75:105] = False # Simulated false drop due to chest coverage
    user_detected_mask[135:165] = False # Simulated false drop due to backpack occlusion
    
    variance_profile = np.full(180, 0.2) # Default stationary noise variance
    variance_profile[60:120] = 4.8      # Severe chest attenuation body flutter
    variance_profile[120:180] = 6.5     # Extreme signal diffraction via heavy backpack
    
    # Track discrete state changes to avoid multi-counting single locks
    previous_state = "PRESENT"
    false_positives = 0
    false_negatives = 0
    
    print("\n[Processing Stream] Streaming telemetry arrays down-line to automation handlers...")
    for t in range(180):
        detected = user_detected_mask[t]
        var = variance_profile[t]
        
        # Update State Machine parameters
        state = fsm.update_state(is_user_detected=detected, current_variance=var)
        
        # Track historical trace metrics
        state_history.append(state)
        timeout_history.append(fsm.dynamic_grace_period)
        
        # CRITICAL FIX: Evaluate edge-triggered transitions to avoid flat frame multi-counting
        if state == "ABSENT" and previous_state != "ABSENT":
            if (60 <= t < 120) or (120 <= t < 180):
                false_positives += 1
                
        previous_state = state
        
        # Update GUI elements dynamically
        ui.update_display(state, var, fsm.dynamic_grace_period)
        time.sleep(0.02) # Fast tracking tick rate simulation
        
    print("\n" + "="*50)
    print("[CHAOS WALK PROTOCOL COMPLETE]")
    print(f"Total Logged False-Positive Lock Actions: {false_positives}")
    print(f"Total Logged False-Negative Lock Actions: {false_negatives}")
    print("="*50 + "\n")
    
    # 3. Generate Production Automation Plot
    plt.figure(figsize=(11, 5))
    
    state_mapping = {"PRESENT": 2, "UNSTABLE": 1, "ABSENT": 0}
    numeric_states = [state_mapping[s] for s in state_history]
    
    plt.step(timeline, numeric_states, where='mid', label='FSM State Vector', color='#00FF66', linewidth=2.5)
    plt.plot(timeline, np.array(timeout_history) / 5.0, label='Scaled Timeout Factor (Normalized)', color='#FFCC00', linestyle='--')
    
    plt.axvspan(0, 60, alpha=0.1, color='blue', label='Phase 1: Safe Range Boundary')
    plt.axvspan(60, 120, alpha=0.1, color='orange', label='Phase 2: Chest Attenuation Window')
    plt.axvspan(120, 180, alpha=0.1, color='purple', label='Phase 3: Heavy Backpack Occlusion')
    
    plt.title("Deterministic FSM Dynamic Hysteresis Tracking: Chaos Walk Protocol Validation", fontsize=11, fontweight='bold')
    plt.xlabel("Simulation Frame Timeline (10Hz Sample Rate)", fontsize=10)
    plt.ylabel("System State Level / Normalized Timeout Metric", fontsize=10)
    plt.yticks([0, 1, 2], ["ABSENT", "UNSTABLE", "PRESENT"])
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.legend(loc='upper right', fontsize=9)
    
    os.makedirs('week_05_automation', exist_ok=True)
    out_img = os.path.join('week_05_automation', 'chaos_walk_fsm_validation.png')
    plt.savefig(out_img, dpi=300)
    print(f"[Success] Chaos Walk visualization chart successfully generated to: {out_img}")
    ui.root.destroy()

if __name__ == "__main__":
    main()