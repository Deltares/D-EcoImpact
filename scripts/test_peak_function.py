from math import nan
import numpy as _np
import xarray as _xr
from scipy.signal import find_peaks

# Generate waveform

x = [
    [1, 0],
    [0, 3],
    [-1, 0],
    [0, 4],
    [1, 0],
    [2, 5],
    [1, 0],
    [0, 6],
    [-3, 0],
    [-4, 7],
    [-2, 0],
    [-1, 8],
    [-3, 0],
    [-5, 9],
]

y = [
    [1, 0, -1, 0, 1, 2, 1, 0, -3, -4, -2, -1, -3, -5],
    [0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9],
]

""" Should give:
[
    [NaN, NaN],
    [NaN, 3],
    [NaN, NaN],
    [NaN, 4],
    [NaN, NaN],
    [2, 5],
    [NaN, NaN],
    [NaN, 6],
    [NaN, NaN],
    [NaN, 7],
    [NaN, NaN],
    [-1, 8],
    [NaN, NaN],
    [NaN, 9],
]
"""
ds = _xr.Dataset(
    {
        "testA": (
            ["mes2d_nFaces", "time", "mesh2d_nLayers"],
            [_np.array(x), _np.array(x)],
        )
    },
    {
        "testB": (
            ["mes2d_nFaces", "mesh2d_nLayers", "time"],
            [_np.array(y), _np.array(y)],
        )
    },
)


def process_peaks(arr):
    # Apply find_peaks
    peaks, _ = find_peaks(arr, prominence=1)
    new_arr = _np.full_like(arr, -999)
    new_arr[peaks] = arr[peaks]
    return new_arr


ds = _xr.open_dataset("../data/FM-VZM_0000_map.nc")

# Apply function to array
results = _xr.apply_ufunc(
    process_peaks,
    ds.salinity,
    input_core_dims=[["time"]],
    output_core_dims=[["time"]],
    vectorize=True,
)


# # Should show repeats of peak results
