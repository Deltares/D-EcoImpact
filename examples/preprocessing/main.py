import os
import numpy as np
from examples.preprocessing.functions.calc_tide_levels import calc_tide_levels_peaks
from examples.preprocessing.functions.NetCDF_updater import NetCDF_map_updater
from examples.preprocessing.functions.InundationClassifier import FloodingRegressor

if __name__ == '__main__':
    home_dir = r'p:\11207689-002-rest-coast-wp2\04_modelling\DMor\02_simulations\calibration\setup_sed' \
               r'\run06_WGS84_nowaves\output'
    map_file = r'ems_map.nc'
    his_file = r'ems_his.nc'
    output_file = r'ems_deco_prep.nc'

    # update paths
    map_file = os.path.join(home_dir, map_file)
    his_file = os.path.join(home_dir, his_file)

    # Compute tide levels
    tides_df = calc_tide_levels_peaks(his_file)

    # make netcdf updater
    NC_updater = NetCDF_map_updater(map_file)

    # make tide levels
    tidal_levels = ["MLWS", "MLWN", "MSL", "MHWN", "MHWS"]
    tide_long_name = {
        "MLWS": "Mean Low Water Spring",
        "MLWN": "Mean Low Water Neap",
        "MSL":  "Mean Sea Level",
        "MHWN": "Mean High Water Neap",
        "MHWS": "Mean High Water Spring"}

    dry_mask = NC_updater.find_dry_falling_cells(min_water_depth=0.05)
    new_var_dicts_list = []
    for tide_level in tidal_levels:
        mask = None
        if tide_level in ["MLWS", "MLWN", "MSL"]:
            mask = dry_mask
        map_tide_values = NC_updater.interp_from_dataframe(tides_df, 'x_coordinate', 'y_coordinate', tide_level)
        new_var_dicts_list.append(NC_updater.make_netcdf_dict(
            tide_level,
            tide_long_name[tide_level],
            'm+NAP',
            map_tide_values,
            mask=mask)
        )

    # Subsample inundation with a baysean regressor
    inundation_regressor = FloodingRegressor(map_file, his_file)
    inundation_regressor.train_regressor()
    inundation_freq_list = inundation_regressor.predict(plot=False)
    inundation_dict = NC_updater.make_netcdf_dict('Inundation',
        "Fraction of time per year the cell is inundated",
        '-',
        np.array(inundation_freq_list))
    new_var_dicts_list.append(inundation_dict)

    # Save netcdf
    NC_updater.save_netcdf_with_dicts("test_map.nc", new_var_dicts_list)
