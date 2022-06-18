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

        # Creating the timestamps for the index
        current_date = datetime.datetime.now()
        previous_90d_date = current_date - datetime.timedelta(days = 90)
        start_date = datetime.datetime(year = previous_90d_date.year,
                                      month = previous_90d_date.month,
                                      day = 1)
        index = pd.date_range(start = start_date, end = current_date, freq = '4H')

        # Creating the dataframe
        data = pd.DataFrame(index=index)

        for circ in self.circuit_names:

            # Generating the sample points
            lls,uls  = self.specifications_limits[circ]['LSL'], self.specifications_limits[circ]['USL']
            mu = (lls + uls) / 2 + np.random.uniform(0.0, 2.5)
            sigma = np.random.uniform(0.0, 5.0)

            samples = np.random.normal(loc=mu, scale=sigma, size=len(index))

            data_ = pd.DataFrame(data=samples, index=index, columns=[circ])

            # Randomly drop some samples
            drop_pct = 0.1
            drop_index = np.random.choice([*range(len(index))], size=int(len(index) * drop_pct), replace=False)
            data_.iloc[drop_index] = np.nan

            data = pd.concat([data, data_], axis=1, ignore_index=False)

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
