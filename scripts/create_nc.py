"""
This file creates a simple NetCDF containing a simplified 3D grid with 
3 data variables.
"""

import numpy as np
import xarray as xr

# Create coordinates
mesh2d_nFaces = 3
mesh2d_node_x = np.random.rand(mesh2d_nFaces)
mesh2d_node_y = np.random.rand(mesh2d_nFaces)
mesh2d_edge_x = np.random.rand(mesh2d_nFaces)
mesh2d_edge_y = np.random.rand(mesh2d_nFaces)
mesh2d_face_x = np.random.rand(mesh2d_nFaces)
mesh2d_face_y = np.random.rand(mesh2d_nFaces)
mesh2d_nLayers = 3
timesteps = 10

data_variable = np.zeros((timesteps, mesh2d_nFaces, mesh2d_nLayers))

mesh2d_interface_z = np.array([0, -1, -3, -7])
mesh2d_flowelem_bl = np.array([-7, -6, -3])
mesh2d_s1 = np.broadcast_to(np.array([0, -0.5, -3]), (timesteps, mesh2d_nFaces))

data_variable_A = data_variable.copy()
data_variable_B = data_variable.copy()
data_variable_C = data_variable.copy()

# Set different values on different levels
data_variable_A[0:5, :, 0] = np.array([11, 11, 3])
data_variable_A[0:5, :, 1] = np.array([14, 14, 3])
data_variable_A[0:5, :, 2] = np.array([19, 19, 3])
data_variable_A[6:9, :, 0] = np.array([5, 5, 2])
data_variable_A[6:9, :, 1] = np.array([3, 3, 2])
data_variable_A[6:9, :, 2] = np.array([1, 1, 2])

data_variable_B[:, :, 0] = np.array([11, 11, 11])
data_variable_B[:, :, 1] = np.array([14, 14, 14])
data_variable_B[:, :, 2] = np.array([19, 19, 19])
data_variable_B[:, 1, 2] = np.array([np.NaN])

data_variable_C[:, :, 0] = np.array([11, 11, 11])
data_variable_C[:, :, 1] = np.array([14, 14, 14])
data_variable_C[:, :, 2] = np.array([19, 19, 19])
data_variable_C[:, 1, 2] = np.array([-999])

# Create dataset
ds = xr.Dataset(
    {
        "var_3d_A": (
            ["time", "mesh2d_nFaces", "mesh2d_nLayers"],
            data_variable_A,
            {"location": "edge", "mesh": "mesh2d"},
        ),
        "var_3d_B": (
            ["time", "mesh2d_nFaces", "mesh2d_nLayers"],
            data_variable_B,
            {"location": "edge", "mesh": "mesh2d"},
        ),
        "var_3d_C": (
            ["time", "mesh2d_nFaces", "mesh2d_nLayers"],
            data_variable_C,
            {"location": "edge", "mesh": "mesh2d", "_FillValue": -999},
        ),
        "mesh2d_interface_z": (
            ["mesh2d_nInterfaces"],
            mesh2d_interface_z,
            {"location": "edge", "mesh": "mesh2d"},
        ),
        "mesh2d_flowelem_bl": (
            ["mesh2d_nFaces"],
            mesh2d_flowelem_bl,
            {"location": "edge", "mesh": "mesh2d"},
        ),
        "mesh2d_s1": (["time", "mesh2d_nFaces"], mesh2d_s1, {"location": "edge"}),
        "mesh2d": ([], 1, {"cf_role": "mesh_topology"}),
    },
    coords={
        "mesh2d_node_x": np.arange(mesh2d_nFaces),
        "mesh2d_node_y": np.arange(mesh2d_nFaces),
        "mesh2d_edge_x": np.arange(mesh2d_nFaces),
        "mesh2d_edge_y": np.arange(mesh2d_nFaces),
        "mesh2d_face_x": np.arange(mesh2d_nFaces),
        "mesh2d_face_y": np.arange(mesh2d_nFaces),
    },
)

ds.to_netcdf("simple_dataset.nc")
