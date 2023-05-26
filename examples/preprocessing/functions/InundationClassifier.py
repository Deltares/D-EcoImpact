import os
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import netCDF4 as nc

from shapely.geometry import Point
from sklearn import linear_model

import xarray as xr
import dfm_tools as dfmt

class FloodingRegressor:
    def __init__(self, map_file, hisfile, crs=None):
        # Import net_cdf
        print('Reading netcdf ...')
        self.map_file = map_file
        self.his_file = hisfile
        self.xr_map = dfmt.open_partitioned_dataset(map_file)
        self.xr_his = xr.open_mfdataset(hisfile, preprocess=dfmt.preprocess_hisnc)
        self._read_grid(crs)
        self._read_map_water_depths()
        self._read_his_water_levels()
        print('Netcdf imported into python class')

    def _read_grid(self, crs):
        # Import grid as pandas dataframe
        x = self.xr_map['mesh2d_node_x'].values
        y = self.xr_map['mesh2d_node_y'].values
        self.grid = pd.DataFrame(data=dict(x=x, y=y))

        # handle coordinate system if None was provided
        if crs is None:
            grid_diagonal_width = np.sqrt((np.max(x) - np.min(x)) ** 2 + (np.max(y) - np.min(y)) ** 2)
            if grid_diagonal_width <= 100:
                warnings.warn('No crs provided, assumed spherical')
                self.crs = 'spherical'
            else:
                warnings.WarningMessage('No crs provided, assumed cartesian')
                self.crs = 'cartesian'

    def _read_map_water_depths(self):
        waterdepths = self.xr_map['mesh2d_waterdepth']
        self.map_water_depths = waterdepths.to_pandas()

    def _read_his_water_levels(self):
        # Import stations from his
        stations_pd = self.xr_his['stations'].to_dataframe()

        # Match station locations to the closest node in the model grid
        station_ids = []
        station_dists = []
        for station in stations_pd.iterrows():
            if self.crs == "cartesian":
                dist = np.sqrt((self.xr_map['mesh2d_node_x'].values - station[1].station_x_coordinate) ** 2 +
                               (self.xr_map['mesh2d_node_y'].values - station[1].station_y_coordinate) ** 2)
            elif self.crs == "spherical":
                grid_points = gpd.GeoSeries([Point(xy) for xy in
                                             zip(self.xr_map['mesh2d_node_x'].values,
                                                 self.xr_map['mesh2d_node_y'].values)], crs='EPSG:4326')
                grid_pointsRD = grid_points.to_crs('EPSG: 28992')
                station_point = gpd.GeoSeries(Point(station[1].station_x_coordinate, station[1].station_y_coordinate),
                                              crs='EPSG:4326')
                station_pointRD = station_point.to_crs('EPSG: 28992')
                dist = grid_pointsRD.distance(station_pointRD[0]).values
            else:
                raise ValueError('Unknown crs; crs must be cartesian or spherical')
            ind_grid = np.where(dist == np.min(dist))
            station_ids.append(ind_grid[0][0])
            station_dists.append(dist)
        stations_pd['node_index'] = station_ids

        # subsample higher resolution .his data at dates form the .map file
        his_wl = self.xr_his['waterlevel'].to_pandas()
        #his_dwl_dt = his_wl.diff().div(his_wl.index.to_series().diff().dt.total_seconds(), axis=0)

        map_time_indices = []
        for map_time in self.map_water_depths.index:
            map_time_ind = np.where(self.xr_his.waterlevel.time.values == map_time)
            map_time_indices.append(map_time_ind[0][0])

        self.his_water_levels= his_wl.iloc[map_time_indices]

    def train_regressor(self, min_flood_depth = 0.05):
        z_minh = np.min(self.his_water_levels)
        z_maxh = np.max(self.his_water_levels)

        his_norm_wl = (self.his_water_levels - z_minh) / (z_maxh - z_minh)
        his_norm = his_norm_wl
        his_norm = his_norm.dropna(axis='columns')
        used_stations = his_norm.columns

        # create Baysian regression per cell
        regression_list = []
        n_cells = len(self.map_water_depths.columns)
        for ii_cel in range(n_cells):
            cell_flood = self.map_water_depths.iloc[:, ii_cel].values >= min_flood_depth
            cell_flood[np.isnan(cell_flood)] = False
            reg = linear_model.BayesianRidge()
            reg.fit(his_norm, cell_flood)
            regression_list.append(reg)
            print(f'Regression across grid {(ii_cel + 1) / n_cells * 100} percent complete \n')

        # store results
        self.normalization = {'z_min': z_minh, 'z_max': z_maxh}
        self.stations = used_stations,
        self.regressors = regression_list,

    def _normalize(self, pd_timeseries):
        return (pd_timeseries.loc[:, self.stations[0]] - self.normalization['z_min']) / (
                    self.normalization['z_max'] - self.normalization['z_min'])

    def predict(self, pandas_station_timeseries=None, plot=False):
        if pandas_station_timeseries is None:
            pandas_station_timeseries = self.xr_his['waterlevel'].to_pandas()
        norm_timeseries = self._normalize(pandas_station_timeseries)

        inundation_freq_list = []
        for regressor in self.regressors[0]:
            predictions = regressor.predict(norm_timeseries)
            inundation_freq = np.sum(predictions >=0.5) / len(predictions)
            inundation_freq_list.append(inundation_freq)

        # Save interpolation to the x_array dataset
        self.xr_map['inundation'] = (['mesh2d_nFaces'], inundation_freq_list)

        # Show the interpolated map
        if plot is True:
            pc = self.xr_map['inundation'].ugrid.plot(edgecolors='face', cmap='jet')
            plt.show()
        return inundation_freq_list

    def save(self, save_name):
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
                if (len(variable.dimensions) > 0):
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
                # add mesh2d

            # Add inundation variable
            x = dst.createVariable("mesh2d_inundation", "float64", ("mesh2d_nFaces"))
            mesh2d_dict = dict()
            mesh2d_dict["name"] = "mesh2d_inundation"
            mesh2d_dict["long_name"] = "Fraction of time cell is inundated"
            mesh2d_dict["mesh"] = "mesh2d"
            mesh2d_dict["location"] = "face"
            mesh2d_dict["cell_methods"] = "mesh2d_nFaces: mean"
            mesh2d_dict["cell_measures"] = "area: mesh2d_flowelem_ba"
            mesh2d_dict["units"] = "-"
            mesh2d_dict["grid_mapping"] = "wgs84"
            dst["mesh2d_inundation"].setncatts(mesh2d_dict)
            dst["mesh2d_inundation"][:] = self.xr_map['inundation'].values

if __name__ == "__main__":

    home_dir = r'p:\11207689-002-rest-coast-wp2\04_modelling\DMor\02_simulations\calibration\setup_sed\run06_WGS84_nowaves\output'
    map_file = r'ems_map.nc'
    his_file = r'ems_his.nc'

    test_reg = FloodingRegressor(os.path.join(home_dir, map_file), os.path.join(home_dir, his_file))
    test_reg.train_regressor()
    inundation_freq_list = test_reg.predict(plot=False)
    test_reg.save("test_inundation.nc")


