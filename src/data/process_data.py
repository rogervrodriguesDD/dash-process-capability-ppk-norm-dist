import datetime
import numpy as np
import pandas as pd
import typing as t

class ProcessData():
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

        if data is None:
            self.data = self._create_sample_data()

    def _check_for_specifications_limits(self):
        set_circ_names = set(self.circuit_names)
        set_circ_spec_lim = set(self.specifications_limits.keys())

        if set_circ_names.difference(set_circ_spec_lim) != set():
            raise OSError("There are missing values for specification limits for the circuit(s): ", ", ".join(set_circ_names.difference(set_circ_spec_lim)))
        if set_circ_spec_lim.difference(set_circ_names) != set():
            raise OSError("There are extra values of specification limits for the circuit(s): ", ", ".join(set_circ_spec_lim.difference(set_circ_names)))

    def _create_sample_data(self) -> pd.DataFrame:

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
