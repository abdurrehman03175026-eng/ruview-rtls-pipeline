import itertools
import numpy as np
from week_02_dsp.filters import SignalFilterPipeline

class DSPHyperparameterTuning:
    def __init__(self, q_grid=None, r_grid=None):
        self.q_grid = q_grid if q_grid else [0.01, 0.1, 1.0]
        self.r_grid = r_grid if r_grid else [1.0, 4.0, 16.0]

    def execute_grid_search(self, raw_signal, ground_truth):
        """Runs the 9 distinct tuning permutations and evaluates RMSE."""
        permutations = list(itertools.product(self.q_grid, self.r_grid))
        run_results = []
        
        for idx, (q, r) in enumerate(permutations, 1):
            pipeline = SignalFilterPipeline(window_size=5, process_variance=q, measurement_variance=r)
            filtered_track = []
            
            for packet in raw_signal:
                filtered_track.append(pipeline.apply_filters(packet))
                
            # Compute Root-Mean-Square Error against stationary ground truth
            rmse = np.sqrt(np.mean((np.array(filtered_track) - ground_truth) ** 2))
            
            run_results.append({
                'permutation_id': idx,
                'q': q,
                'r': r,
                'rmse': rmse,
                'filtered_signal': filtered_track
            })
            
        return run_results