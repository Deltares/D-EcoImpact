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

ds = _xr.Dataset(
    {
        "var_3d": (
            ["time", "mesh2d_nFaces"],
            _np.array(x),
        )
    }
)

y = _np.array([1, 0, -1, 0, 1, 2, 1, 0, -3, -4, -2, -1, -3, -5])


# Find peaks non-xarray way
peaks, _ = find_peaks(y)
# print(y, _, peaks)
# print(y[peaks])

# # Cast waveform to xr.DataArray
# x = xr.DataArray(x, dims="time")

# # Duplicate data along a new dimension
# rep = xr.DataArray(range(11), dims="repeat")
# x = x.broadcast_like(rep).assign_coords(repeat=rep)


def process_peaks(arr):
    print(arr)
    # Apply find_peaks
    peaks, _ = find_peaks(arr, prominence=1)
    new_arr = _np.full_like(arr, nan)

    return new_arr


# Apply function to array
results = _xr.apply_ufunc(
    process_peaks,
    ds,
    input_core_dims=[["time"]],
    output_core_dims=[["peaks"]],
    vectorize=True,
)


# # Should show repeats of peak results
print(results)
