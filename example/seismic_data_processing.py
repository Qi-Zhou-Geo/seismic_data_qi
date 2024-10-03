#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-02-23
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz-potsdam.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do not distribute this code without the author's permission

import os
import sys
import numpy as np
from obspy import read, Stream, read_inventory, signal
from obspy.core import UTCDateTime # default is UTC+0 time zone

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# import CONFIG_dir as a global variable
from config.config_dir import CONFIG_dir
# import manually remove sensor response
from calculate_features.remove_sensor_response import manually_remove_sensor_response

def load_seismic_signal(seismic_network, station, component, data_start, data_end, remove_sensor_response=True):

    # config the snesor parameter based on seismci network code
    if seismic_network == "9J" or seismic_network == "9S":
        sac_path = CONFIG_dir["sac_path_Illgraben"]
        response_type = "xml"
    elif seismic_network == "1A":
        sac_path = CONFIG_dir["sac_path_Museum"]
        response_type = "simulate"
    elif seismic_network == "LD":
        sac_path = CONFIG_dir["sac_path_Luding"]
        response_type = "simulate"
    else:
        print(f"please check the seismic_network: {seismic_network}")


    d1 = UTCDateTime(data_start)
    d2 = UTCDateTime(data_end)

    # make sure all you file is structured like this
    file_dir = f"{sac_path}{d1.year}/{station}/{component}/"

    if d1.julday == d2.julday:
        data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(d1.julday).zfill(3)}.mseed"
        st = read(file_dir + data_name)
    else:
        st = Stream()
        for n in np.arange(d1.julday-1, d2.julday+1):
            data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(n).zfill(3)}.mseed"
            st += read(file_dir + data_name)

    st.merge(method=1, fill_value='latest', interpolation_samples=0)
    st._cleanup()
    st.detrend('linear')
    st.detrend('demean')

    if remove_sensor_response is True:

        if response_type == "xml": # with xml file
            meta_file = [f for f in os.listdir(f"{sac_path}meta_data") if f.startswith(seismic_network)][0]
            inv = read_inventory(f"{sac_path}meta_data/{meta_file}")
            st.remove_response(inventory=inv)
        elif response_type == "simulate": # with poles and zeros
            st = manually_remove_sensor_response(st, "trillium_compact_120s_754")
        else:
            print(f"please check the response_type: {response_type}")
    else:
        pass

    st.filter("bandpass", freqmin=1, freqmax=45)
    st = st.trim(starttime=d1, endtime=d2, nearest_sample=False)
    st.detrend('linear')
    st.detrend('demean')

    return st


