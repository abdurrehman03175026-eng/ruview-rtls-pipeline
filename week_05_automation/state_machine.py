import time

class DynamicHysteresisStateMachine:
    def __init__(self, base_grace_period=5.0):
        self.current_state = "PRESENT"
        self.base_grace_period = base_grace_period
        self.dynamic_grace_period = base_grace_period
        self.unstable_start_time = None

    def update_state(self, is_user_detected: bool, current_variance: float) -> str:
        """
        Dynamically scales the timeout window using real-time signal variance.
        High Noise Variance = Stretched Grace Window to protect against false drops.
        """
        current_time = time.time()
        
        # Adaptive Hysteresis Scaling Calculation
        # Variance acts as an expansion multiplier capped at a maximum 15-second window
        scaling_factor = min(current_variance * 1.5, 10.0)
        self.dynamic_grace_period = self.base_grace_period + scaling_factor

        if is_user_detected:
            self.current_state = "PRESENT"
            self.unstable_start_time = None
        else:
            if self.current_state == "PRESENT":
                self.current_state = "UNSTABLE"
                self.unstable_start_time = current_time
            elif self.current_state == "UNSTABLE":
                elapsed_unstable = current_time - self.unstable_start_time
                if elapsed_unstable >= self.dynamic_grace_period:
                    self.current_state = "ABSENT"
                    # Soft execution flag for cross-platform simulation safety
                    self._trigger_os_lock()
                    
        return self.current_state

    def _trigger_os_lock(self):
        print("[AUTOMATION FLAG] Execution Condition Met: Dispatching Workstation Lock Command.")
        # os.system("rundll32.exe user32.dll,LockWorkStation")