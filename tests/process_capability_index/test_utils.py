from src.process_capability_index.utils import calculate_cap_index_ppk
from tests.test_fixtures import (
    test_process_data_parameters,
    test_process_data_obj_stable_processes,
    test_process_data_obj_unstable_processes
)

class TestCalculateCapIndexPPK(object):
    def test_calculate_ppk_stable_processes(self, test_process_data_obj_stable_processes):

        ppk_rep_monthly = calculate_cap_index_ppk(test_process_data_obj_stable_processes, freq='BMS')

        ppk_columns = zip(test_process_data_obj_stable_processes.circuit_names,
                        ['PPK'] * len(test_process_data_obj_stable_processes.circuit_names))

        message = \
        "The function 'calculate_cap_index_ppk' didn't present expected results for stable processes. Expected results: PPK >= 1.0"
        assert all(ppk_rep_monthly[ppk_columns].min(axis=0) >= 1.0), message

    def test_calculate_ppk_unstable_processes(self, test_process_data_obj_unstable_processes):

        ppk_rep_monthly = calculate_cap_index_ppk(test_process_data_obj_unstable_processes, freq='BMS')

        ppk_columns = zip(test_process_data_obj_unstable_processes.circuit_names,
                        ['PPK'] * len(test_process_data_obj_unstable_processes.circuit_names))

        message = \
        "The function 'calculate_cap_index_ppk' didn't present expected results for unstable processes. Expected results: PPK < 1.0"
        assert all(ppk_rep_monthly[ppk_columns].min(axis=0) < 1.0), message
