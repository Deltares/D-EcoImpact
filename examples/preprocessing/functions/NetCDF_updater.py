import xarray as xr
import os
import dfm_tools as dfmt
import pandas as pd
import numpy as np
import netCDF4 as nc
from scipy.interpolate import RBFInterpolator

from calc_tide_levels import calc_tide_levels_peaks

class NetCDF_map_updater:
    ## Main methods
    def __init__(self, map_file):
        # Import net_cdf
        self.map_file = map_file
        print("Importing Delft3D-FM netcdfs ...")
        self.xr_map = dfmt.open_partitioned_dataset(map_file)
        if 'wgs84' in  self.xr_map.data_vars:
            self.coordinate_system = 'wgs84'
            self.epsg = self.xr_map.wgs84.epsg
        elif 'projected_coordinate_system' in  self.xr_map.data_vars:
            self.coordinate_system = 'projected_coordinate_system'
            self.epsg = self.xr_map.projected_coordinate_system.epsg
        else:
            raise Exception("No coordinate system recognised in netcdf")
        # Import grid as pandas dataframe
        x = self.xr_map['mesh2d_node_x'].values
        y = self.xr_map['mesh2d_node_y'].values
        self.grid = pd.DataFrame(data=dict(x=x, y=y))
        self.dry_falling_cells = None
        print("Delft3D-FM netcdf imported")

    def interp_from_dataframe(self, pd_dataframe, x_column, y_column, value_column):
        print("Interpolating samples across map grid")
        interp_points = np.array(list(zip(pd_dataframe[x_column].values,
                                          pd_dataframe[y_column].values)))
        grid_points = np.array(list(zip(self.xr_map.grid.face_x, self.xr_map.grid.face_y)))
        i_valid = ~np.isnan(pd_dataframe[value_column])
        interp_values = RBFInterpolator(interp_points[i_valid],
                                        pd_dataframe[value_column][i_valid],
                                        kernel="linear")(grid_points)
        return interp_values

    def make_netcdf_dict(self, name, long_name, unit, values , mask=None):
        """
        :param name: (string) name for the new variable in the NetCDF
        :param long_name: (string) description of the new variable
        :param unit: (string) unit of the new variable, e.g. kg/m^3
        :param values: (list or numpy array) value of the variable per grid cell. Must be the same size as the grid.
        :param mask: (list or numpy array of booleans) cells to be filled with Nan's. 1's are masked.
        """
        mesh2d_dict = dict()
        mesh2d_dict["name"] = "mesh2d_" + name
        mesh2d_dict["long_name"] = long_name
        mesh2d_dict["mesh"] = "mesh2d"
        mesh2d_dict["location"] = "face"
        mesh2d_dict["cell_methods"] = "mesh2d_nFaces: mean"
        mesh2d_dict["cell_measures"] = "area: mesh2d_flowelem_ba"
        mesh2d_dict["units"] = unit
        mesh2d_dict["grid_mapping"] = self.coordinate_system

        values = np.array(values)
        if mask is not None:
            values = values.astype('float')
            mask = np.array(mask, dtype='bool')
            values[mask] = np.nan

        netcdf_dict = {
            "attr": mesh2d_dict,
            "val": values
        }

        return netcdf_dict

    def save_netcdf_with_dicts(self, save_name, netcdf_dict_list):
        print("Saving results to netCDF ...")
        # add metadata
        with nc.Dataset(self.map_file) as src, nc.Dataset(save_name, "w") as dst:
            # copy global attributes all at once via dictionary
            dst.setncatts(src.__dict__)
            # copy dimensions
            for name, dimension in src.dimensions.items():
                dst.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
            # copy all file data except for the excluded
            for name, variable in src.variables.items():
                print(name)
                if len(variable.dimensions) > 0:
                    new_dimensions = variable.dimensions
                else:
                    new_dimensions = variable.dimensions
                print("---")
                print(variable.dimensions)
                print(variable.datatype)
                print(new_dimensions)
                print("---")
                x = dst.createVariable(name, variable.datatype, new_dimensions)

                # copy variable attributes all at once via dictionary
                temp_dict = src[name].__dict__
                dst[name].setncatts(temp_dict)

                # add the data
                dst[name][:] = src[name][:]

            # Add new variables from dictionaries
            for netcdf_dict in netcdf_dict_list:
                mesh_name = "mesh2d_" + netcdf_dict["attr"]["name"]
                x = dst.createVariable(mesh_name, str(netcdf_dict["val"].dtype), ("mesh2d_nFaces"))
                dst[mesh_name].setncatts(netcdf_dict["attr"])
                dst[mesh_name][:] = netcdf_dict["val"]
            print("netCDF saved")

    def find_dry_falling_cells(self, min_water_depth):
        # determine dry falling cells
        water_depths = self.xr_map['mesh2d_waterdepth'].to_pandas()
        ind_dry = water_depths.columns[(water_depths < min_water_depth).any()].to_list()
        mask = np.zeros(len(water_depths)).astype('bool')
        mask[ind_dry] = True
        return mask





