import datetime
import numpy as np
import pandas as pd
import typing as t

class ProcessData():
    """
    Create a new object that contains all informations needed to calculate the
    capability indices.

    ...

    Attributes:
        plant_name (str): Name of the plant where the data is being colected
        circuit_names (list): List of strings for each circuit where the measurements occur
        specifications_limits (dict): Dictionary with specification limits ('LSL' and 'USL') defined for each
                                    circuit name given in the circuit_names attribute.
        ppk_goals (dict): Dictionary with ppk goal defined for each circuit name given in the circuit_name
                        attribute.
        data (pd.DataFrame, optional): DataFrame with columns named on the circuit names and timestamp index.
                                    Obs.: If data is not given, the dataset will be generated using the
                                    '_create_sample_data' method.
    """
    def __init__(self,
                plant_name: str,
                circuit_names: t.Sequence[str],
                specifications_limits: dict,
                ppk_goals: dict,
                data: pd.DataFrame = None):
        self.plant_name = plant_name

        self.data = data
        self.specifications_limits = specifications_limits
        self.ppk_goals = ppk_goals

        if isinstance(circuit_names, list):
            self.circuit_names = circuit_names
        else:
            self.circuit_names = [circuit_names]

        self._check_for_specifications_limits()
        self._check_for_ppk_goals()

        if data is None:
            self.data = self._create_sample_data()

        self._check_for_data_columns()

    def _check_for_specifications_limits(self):
        """
        Check if all the circuits listed in the 'circuit_names' attribute has an related specification
        limits in the 'specifications_limits' attribute. This check is simple and only verify if the
        circuit name is a key in the 'specifications_limits' attribute.
        """
        set_circ_names = set(self.circuit_names)
        set_circ_spec_lim = set(self.specifications_limits.keys())

        if set_circ_names.difference(set_circ_spec_lim) != set():
            raise OSError("There are missing values for specification limits for the circuit(s): ", ", ".join(set_circ_names.difference(set_circ_spec_lim)))
        if set_circ_spec_lim.difference(set_circ_names) != set():
            raise OSError("There are extra values of specification limits for the circuit(s): ", ", ".join(set_circ_spec_lim.difference(set_circ_names)))

    def _check_for_ppk_goals(self):
        """
        Check if all the circuits listed in the 'circuit_names' attribute has an related ppk goal
        in the 'ppk_goals' attribute. This check is simple and only verify if the circuit name is a key
        in the referred attribute.
        """
        set_circ_names = set(self.circuit_names)
        set_circ_ppk_goals = set(self.ppk_goals.keys())

        if set_circ_names.difference(set_circ_ppk_goals) != set():
            raise OSError("There are missing values for ppk goal for the circuit(s): ", ", ".join(set_circ_names.difference(set_circ_ppk_goals)))
        if set_circ_ppk_goals.difference(set_circ_names) != set():
            raise OSError("There are extra values of ppk goal for the circuit(s): ", ", ".join(set_circ_ppk_goals.difference(set_circ_names)))

    def _check_for_data_columns(self):
        """
        Check if all the circuits listed in the 'circuit_names' attribute has an related column
        in the input data.
        """
        set_circ_names = set(self.circuit_names)
        set_data_columns = set(self.data.columns)

        if set_circ_names.difference(set_data_columns) != set():
            raise OSError("There are missing columns in the input data for the circuit(s): ", ", ".join(set_circ_names.difference(set_data_columns)))
        if set_data_columns.difference(set_circ_names) != set():
            raise OSError("There are extra columns in the input data for the circuit(s): ", ", ".join(set_data_columns.difference(set_circ_names)))

    def _create_sample_data(self) -> pd.DataFrame:
        """
        Create a set of samples for each circuit listed in the 'circuit_names' attribute.
        The samples are generated considering the specification limits given for the specific circuit,
        although the are noise added to the signal to simulate unexpected behavior.
        """

        index_data_input = pd.date_range(start = datetime.datetime.now()- datetime.timedelta(days=90),
                            end = datetime.datetime.now(),
                            freq = '1H')

        n_samples = len(index_data_input)
        n_samples_instability = int(n_samples / 3)
        values = np.zeros(shape=(n_samples, len(self.circuit_names)))

        for i, circ in enumerate(self.circuit_names):
            lsl = self.specifications_limits[circ]['LSL']
            usl = self.specifications_limits[circ]['USL']

            expected_average = (usl + lsl) / 2
            max_expected_std = (usl - lsl) / 7
            simulated_std = np.random.uniform(low=0.1 * max_expected_std, high=max_expected_std)

            values[:,i] = (np.ones(shape=(n_samples, 1)) * expected_average +\
                            np.random.normal(loc = 0.0, scale=simulated_std, size=(n_samples, 1))).reshape(-1,)


            # Adding instability
            idx_instability = np.random.choice(range(0, n_samples - n_samples_instability))

            simulated_average_instability = np.random.uniform(low=-max_expected_std, high=max_expected_std)
            simulated_std_instability = np.random.uniform(low=max_expected_std, high=1.25 * max_expected_std)

            values[idx_instability : idx_instability + n_samples_instability, i] = (
                values[idx_instability : idx_instability + n_samples_instability, i] +
                np.random.normal(loc = simulated_average_instability, scale=simulated_std_instability,
                                 size=(n_samples_instability, 1)).reshape(-1,)
            )

        data = pd.DataFrame(
            data = values,
            index = index_data_input,
            columns = self.circuit_names
        )

        return data

class SetProcessData():
    """
    Create new object that contains a set of multiple ProcessData objects.
    ...

    Attributes:
        process_data_obj (list): List with multiple ProcessData objects.

    Methods:
        __getitem__(plant_name): Return the ProcessData object for given 'plant_name'

    """
    def __init__(self, process_data_objs):

        if not isinstance(process_data_objs, list):
            process_data_objs = list(process_data_objs)
        self.process_data_objs = process_data_objs

        self.list_plant_names = [obj.plant_name for obj in process_data_objs]

    def __getitem__(self, plant_name):
        idx_plant_name = self.list_plant_names.index(plant_name)
        return self.process_data_objs[idx_plant_name]
