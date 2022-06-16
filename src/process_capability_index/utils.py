import pandas as pd
import numpy as np

def calculate_cap_index_ppk(process_data_obj: pd.DataFrame, freq: str ='BMS'):
    """
    Calculate the Ppk index for the Process Data object and time frequency given.

    Args:
        process_data_obj (pd.DataFrame): Process Data object on which the index will be calculated.
        freq (str, default='BMS'): Time unit used as reference to group the samples.
                                    Example: 'BMS' for month (Business Month Start, in this case), 'D' for day.

    Returns:
        capidx_ppk (pd.DataFrame): DataFrame with columns 'count', 'mean', 'std', 'ppi', 'pps', and 'ppk' for
                                each circuit given in the Process data object.
    """

    groups = process_data_obj.data.groupby(pd.Grouper(freq=freq))

    def ppi(x):
        return (np.mean(x) - spec_limits['LSL']) / np.std(x) / 3

    def pps(x):
        return (spec_limits['USL'] - np.mean(x) ) / np.std(x) / 3

    capidx_ppk = pd.DataFrame(index=groups.groups.keys())

    for circ in process_data_obj.circuit_names:
        spec_limits = process_data_obj.specifications_limits[circ]

        capidx_ppk_ = groups[[circ]].agg(['count','mean', 'std', ppi, pps])
        capidx_ppk_[(circ, 'PPK')] = capidx_ppk_[zip(2*[circ], ['ppi', 'pps'])].min(axis=1)

        capidx_ppk = pd.concat([capidx_ppk, capidx_ppk_], axis=1, ignore_index=False)

    return capidx_ppk
