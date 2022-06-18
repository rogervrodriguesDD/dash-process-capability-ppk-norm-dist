import datetime
from flask import Flask
import numpy as np
import pandas as pd
import pytest

from src.data.process_data import ProcessData

@pytest.fixture
def test_process_data_parameters():
    parameters = {
    'plant_name': 'Plant A',
    'circuit_names': ['Circuit 1', 'Circuit 2', 'Circuit 3'],
    'specifications_limits': {'Circuit 1': {'LSL': 60.0, 'USL': 70.0},
                            'Circuit 2': {'LSL': 90.0, 'USL': 100.0},
                            'Circuit 3': {'LSL': 80.0, 'USL': 85.0}},
    'ppk_goals': {'Circuit 1': 1.0,
                'Circuit 2': 1.0,
                'Circuit 3': 1.33}
    }

    yield parameters

@pytest.fixture
def test_one_circuit_process_data_parameters():
    parameters = {
    'plant_name': 'Plant A',
    'circuit_names': ['Circuit 1'],
    'specifications_limits': {'Circuit 1': {'LSL': 60.0, 'USL': 70.0}},
    'ppk_goals': {'Circuit 1': 1.0}
    }

    yield parameters

@pytest.fixture
def test_process_data_parameters_with_data_input(test_process_data_parameters):
    parameters = test_process_data_parameters
    index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=10),
                        end = datetime.datetime.now(),
                        freq = '4H')

    test_data_input = pd.DataFrame(
        data = np.random.random(size=(len(index_data_input), len(parameters['circuit_names']))),
        index = index_data_input,
        columns = parameters['circuit_names']
    )

    parameters['data'] = test_data_input

    yield parameters

@pytest.fixture
def missing_spec_lim_process_data_parameters():
    parameters = {
    'plant_name': 'Plant A',
    'circuit_names': ['Circuit 1', 'Circuit 2', 'Circuit 3'],
    'specifications_limits': {'Circuit 1': {'LSL': 60.0, 'USL': 70.0},
                            'Circuit 2': {'LSL': 90.0, 'USL': 100.0},
                           },
    'ppk_goals': {'Circuit 1': 1.0,
                'Circuit 2': 1.0,
                'Circuit 3': 1.33}
    }
    yield parameters

@pytest.fixture
def missing_ppk_goal_process_data_parameters():
    parameters = {
    'plant_name': 'Plant A',
    'circuit_names': ['Circuit 1', 'Circuit 2'],
    'specifications_limits': {'Circuit 1': {'LSL': 60.0, 'USL': 70.0},
                            'Circuit 2': {'LSL': 90.0, 'USL': 100.0},
                           },
    'ppk_goals': {'Circuit 1': 1.0,
                'Circuit 3': 1.33}
    }
    yield parameters

@pytest.fixture
def missing_columns_process_data_parameters_with_data_input(test_process_data_parameters):
    parameters = test_process_data_parameters
    index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=10),
                        end = datetime.datetime.now(),
                        freq = '4H')


    test_data_input = pd.DataFrame(
        data = np.random.random(size=(len(index_data_input), len(parameters['circuit_names']) - 1)),
        index = index_data_input,
        columns = parameters['circuit_names'][:-1]
    )

    parameters['data'] = test_data_input

    yield parameters

@pytest.fixture
def extra_columns_process_data_parameters_with_data_input(test_one_circuit_process_data_parameters):
    parameters = test_one_circuit_process_data_parameters
    index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=10),
                        end = datetime.datetime.now(),
                        freq = '4H')

    test_data_input = pd.DataFrame(
        data = np.random.random(size=(len(index_data_input), len(parameters['circuit_names']) + 1)),
        index = index_data_input,
        columns = parameters['circuit_names'] + ['Extra circuit']
    )

    parameters['data'] = test_data_input

    yield parameters

@pytest.fixture
def test_process_data_obj_stable_processes(test_process_data_parameters):
    parameters = test_process_data_parameters

    index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=90),
                        end = datetime.datetime.now(),
                        freq = '4H')

    n_samples = len(index_data_input)
    values = np.zeros(shape=(n_samples, len(parameters['circuit_names'])))

    for i, circ in enumerate(parameters['circuit_names']):
        lsl = parameters['specifications_limits'][circ]['LSL']
        usl = parameters['specifications_limits'][circ]['USL']

        expected_average = (usl + lsl) / 2
        max_expected_std = (usl - lsl) / 8
        simulated_std = np.random.uniform(low=0.1 * max_expected_std, high=max_expected_std)
        values[:,i] = (np.ones(shape=(n_samples, 1)) * expected_average + \
                        np.random.normal(loc = 0.0, scale=simulated_std, size=(n_samples, 1))).reshape(-1,)

    test_data_input = pd.DataFrame(
        data = values,
        index = index_data_input,
        columns = parameters['circuit_names']
    )

    parameters['data'] = test_data_input
    process_data_obj = ProcessData(**parameters)

    yield process_data_obj

@pytest.fixture
def test_process_data_obj_unstable_processes(test_process_data_parameters):
    parameters = test_process_data_parameters

    index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=90),
                        end = datetime.datetime.now(),
                        freq = '4H')

    n_samples = len(index_data_input)
    values = np.zeros(shape=(n_samples, len(parameters['circuit_names'])))

    for i, circ in enumerate(parameters['circuit_names']):
        lsl = parameters['specifications_limits'][circ]['LSL']
        usl = parameters['specifications_limits'][circ]['USL']

        expected_average = (usl + lsl) / 2
        min_expected_std = (usl - lsl) / 6
        simulated_std = np.random.uniform(low=min_expected_std, high=1.5*min_expected_std)
        values[:,i] = (np.ones(shape=(n_samples, 1)) * expected_average + \
                        np.random.normal(loc = 0.0, scale=simulated_std, size=(n_samples, 1))).reshape(-1,)

    test_data_input = pd.DataFrame(
        data = values,
        index = index_data_input,
        columns = parameters['circuit_names']
    )

    parameters['data'] = test_data_input
    process_data_obj = ProcessData(**parameters)

    yield process_data_obj
