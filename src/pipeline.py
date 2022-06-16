from data.process_data import (ProcessData)
from process_capability_index.utils import (calculate_cap_index_ppk)

# Plant A
data_A_c1 = ProcessData(
                        plant_name='Plant A',
                        circuit_names=['Circuit 1', 'Circuit 2'],
                        specifications_limits = {'Circuit 1': {'LSL': 60.0, 'USL': 70.0},
                                                'Circuit 2': {'LSL': 90.0, 'USL': 100.0}},
                        ppk_goals = {'Circuit 1': 1.0,
                                'Circuit 2': 1.0}
                        )

# Calculating Monthly Index for the circuits (needed to generate the options for the month selector)
df_A_c1_month = calculate_cap_index_ppk(data_A_c1, freq='BMS')
