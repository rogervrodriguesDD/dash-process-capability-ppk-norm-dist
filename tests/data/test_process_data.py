import pytest

from src.data.process_data import (ProcessData, SetProcessData)
from tests.test_fixtures import (
    test_process_data_parameters,
    test_process_data_parameters_with_data_input,
    test_one_circuit_process_data_parameters,
    missing_spec_lim_process_data_parameters,
    missing_ppk_goal_process_data_parameters,
    missing_columns_process_data_parameters_with_data_input,
    extra_columns_process_data_parameters_with_data_input
)

class TestProcessDataClass(object):

    def test_process_data_class(self, test_process_data_parameters):
        test_data = ProcessData(**test_process_data_parameters)
        assert test_data
        assert len(test_data.data.columns) == len(test_process_data_parameters['circuit_names'])

    def test_process_data_class_with_data_input(self, test_process_data_parameters_with_data_input):
        test_data = ProcessData(**test_process_data_parameters_with_data_input)
        assert test_data
        assert len(test_data.data.columns) == len(test_process_data_parameters_with_data_input['circuit_names'])

    def test_one_circuit_process_data_class(self, test_one_circuit_process_data_parameters):
        test_data = ProcessData(**test_one_circuit_process_data_parameters)
        assert isinstance(test_data.circuit_names, list)
        assert len(test_data.circuit_names) == 1
        assert len(test_data.data.columns) == 1

    def test_missing_spec_lim_process_data_class(self, missing_spec_lim_process_data_parameters):
        with pytest.raises(OSError) as excinfo:
            ProcessData(**missing_spec_lim_process_data_parameters)

    def test_missing_ppk_goal_process_data_class(self, missing_ppk_goal_process_data_parameters):
        with pytest.raises(OSError) as excinfo:
            ProcessData(**missing_ppk_goal_process_data_parameters)

    def test_missing_columns_process_data_class_with_data_input(self, missing_columns_process_data_parameters_with_data_input):
        with pytest.raises(OSError) as excinfo:
            ProcessData(**missing_columns_process_data_parameters_with_data_input)

    def test_extra_columns_process_data_class_with_data_input(self, extra_columns_process_data_parameters_with_data_input):
        with pytest.raises(OSError) as excinfo:
            ProcessData(**extra_columns_process_data_parameters_with_data_input)
