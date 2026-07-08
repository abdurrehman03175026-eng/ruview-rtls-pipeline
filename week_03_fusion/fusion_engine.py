import numpy as np

class MultiNodeFusionEngine:
    def __init__(self):
        pass

    def fuse_max_unattenuated(self, node_data_dict):
        """
        Accepts a dictionary of active node telemetry arrays.
        Example: {'node_01': array([...]), 'node_02': array([...])}
        Returns a single fused timeline stream selecting the strongest path.
        """
        # Convert dictionary paths to a stacked matrix
        node_keys = list(node_data_dict.keys())
        stacked_matrix = np.column_stack([node_data_dict[k] for k in node_keys])
        
        # Core Requirement: Prioritize maximum un-attenuated signal value (closest to 0 dBm)
        fused_stream = np.max(stacked_matrix, axis=1)
        return fused_stream