import numpy as np
import pandas as pd
import xarray as xr
import dfm_tools as dfmt
from scipy.signal import argrelextrema, find_peaks

def calc_tide_levels_peaks(his_file, stations = None, bedlevel_margin=0.1):
    """
    Calculates tidal levels MLWS, MLWN, MSL, MHWN, and MHWS by indentifying the peaks in the waterlevel time series at
    observation points. May not work properly for short simulations
    :param xr_his: xarray repressentation of the a Delft3dFm .._his.nc file. Obtained with the command
    xr.open_mfdataset(.._his.nc) where xr is the xarray package.
    :param stations: list of stations of which to determine tidal levels for [station 1, station 2, ...]
    :return: A pandas dataframe with MLWS, MLWN, MSL, MHWN, and MHWS per station
    """
    xr_his = xr.open_mfdataset(his_file, preprocess=dfmt.preprocess_hisnc)
    waterlevels_pd = xr_his['waterlevel'].to_pandas()
    bedlevels_pd = xr_his['bedlevel'].isel(time=[0]).to_pandas()
    dt_mean = np.mean((xr_his.time.values[1:-1] - xr_his.time.values[0:-2])/ np.timedelta64(1, "s"))  # average time step in his_file in s
    T_M2 = 12.42  # Tidal period in hours
    n_samples_per_tide = int(np.ceil((T_M2 * 3600) / dt_mean) + 1)
    n_tolerance = int((2 * 3600) / dt_mean + 1)  # tolerance for consecutive high/low tides within tidal period

    T_spring_neap = 14.76  # Period of spring-neap cycle in days
    n_tides_per_spring_neap = int(np.ceil((T_spring_neap * 24) / T_M2) + 1)

    MLWS_list =[]
    MLWN_list=[]
    MSL_list=[]
    MHWN_list=[]
    MHWS_list=[]

    if stations is None:
        stations = xr_his.stations.data
    else:
        check_stations_in_his(xr_his, stations)
    station_df = xr_his.stations.to_dataframe()

    for station in stations:
        # find low and high waters in timeseries:
        ind_LW = find_peaks(-waterlevels_pd[station], distance=int((n_samples_per_tide + n_tolerance) / 2))[0]
        ind_HW = find_peaks( waterlevels_pd[station], distance=int((n_samples_per_tide + n_tolerance) / 2))[0]

        LWs = waterlevels_pd[station].iloc[ind_LW].values
        LWs[LWs <= (bedlevels_pd[station].values + bedlevel_margin)] = np.nan
        HWs = waterlevels_pd[station].iloc[ind_HW].values
        MHW = np.nanmean(HWs)
        MLW = np.nanmean(LWs)
        tidal_range = MHW - MLW
        MSL = np.nanmean(waterlevels_pd[station].values)

        # find low and high water spring and neap
        LWSs = LWs[argrelextrema(LWs, np.less_equal, order=int(n_tides_per_spring_neap/2))[0]]
        LWNs = LWs[argrelextrema(LWs, np.greater_equal, order=int(n_tides_per_spring_neap/2))[0]]
        HWSs = HWs[argrelextrema(HWs, np.greater_equal, order=int(n_tides_per_spring_neap/2))[0]]
        HWNs = HWs[argrelextrema(HWs, np.less_equal, order=int(n_tides_per_spring_neap/2))[0]]

        # compute tidal levels
        if np.sum(np.isnan(LWs))/len(LWs) > 0.05:
            MLWS_list.append(np.nan)
            MLWN_list.append(np.nan)
            MSL_list.append(np.nan)
        else:
            MLWS_list.append(np.nanmean(LWSs))
            MLWN_list.append(np.nanmean(LWNs))
            MSL_list.append(MSL)
        MHWN_list.append(np.nanmean(HWNs))
        MHWS_list.append(np.nanmean(HWSs))

    return pd.DataFrame(data=dict(
            x_coordinate=station_df.station_x_coordinate,
            y_coordinate=station_df.station_y_coordinate,
            station=stations,
            MLWS=MLWS_list,
            MLWN=MLWN_list,
            MSL=MSL_list,
            MHWN=MHWN_list,
            MHWS=MHWS_list))

def check_stations_in_his(xr_his, stations):
    """
    Check if the list of stations in `stations` is present in t
    :param xr_his:
    :param stations:
    :return:
    """
    for station in stations:
        if station not in xr_his.stations.data:
            raise KeyError(f"No station with the name {station} found in the _his.nc file")
