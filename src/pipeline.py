from data.process_data import ProcessData, SetProcessData
from app_config import config

# Plant A
data_A = ProcessData(
                        plant_name='Plant A',
                        circuit_names=['Circuit 1', 'Circuit 2', 'Circuit 3'],
                        specifications_limits = {'Circuit 1': {'LSL': 60.0, 'USL': 70.0},
                                                'Circuit 2': {'LSL': 90.0, 'USL': 100.0},
                                                'Circuit 3': {'LSL': 80.0, 'USL': 85.0}},
                        ppk_goals = {'Circuit 1': 1.0,
                                'Circuit 2': 1.0,
                                'Circuit 3': 1.33}
                        )

# Plant B
data_B = ProcessData(
                    plant_name='Plant B',
                    circuit_names=['Circuit 1', 'Circuit 2'],
                    specifications_limits = {'Circuit 1': {'LSL': 40.0, 'USL': 70.0},
                                            'Circuit 2': {'LSL': 50.0, 'USL': 100.0}},
                    ppk_goals = {'Circuit 1': 1.0,
                                'Circuit 2': 1.0}
                    )

# Industrial park
data_ind_park = SetProcessData(process_data_objs=[data_A, data_B])
