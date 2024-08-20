#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-04-28
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz-potsdam.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do NOT distribute this code without the author's permission

from obspy import read, Stream, UTCDateTime, read_inventory

global SAC_PATH, OUTPUT_DIR
SAC_PATH = "/storage/vast-gfz-hpc-01/project/seismic_data_qi/seismic/EU/Illgraben/"
OUTPUT_DIR = "/storage/vast-gfz-hpc-01/home/qizhou/1projects/" # set your output path

print(SAC_PATH)

def load_seismic_signal(data_start, data_end, station, component="EHZ", remove_sensor_response=False):
    '''
    Load seismic signal

    Parameters:
    - data_start (str): the start time to select data, e.g., 2017-04-03 12:00:00
    - data_end (str): the start time to select data, e.g., 2017-04-03 13:00:00
    - station (str): seismic station name
    - component (str): seismic component name
    - remove_sensor_response (bool, optial): for deconvolove

    Returns:
    - st (obspy.core.stream): seismic stream
    '''

    d1 = UTCDateTime(data_start)
    d2 = UTCDateTime(data_end)

    sac_dir = f"{SAC_PATH}{d1.year}/{station}/{component}/"

    if d1.year in [2013, 2014]:
        seismic_network = "GM"
    elif d1.year in [2017, 2018, 2019, 2020]:
        seismic_network = "9S"


    if d1.julday == d2.julday:
        data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(d1.julday).zfill(3)}"
        st = read(sac_dir + data_name)
    else:
        st = Stream()
        for n in np.arange(d1.julday, d2.julday+1):
            data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(n).zfill(3)}"
            st += read(sac_dir + data_name)


    st = st.trim(starttime=d1, endtime=d2, nearest_sample=False)
    st.merge(method=1, fill_value='latest', interpolation_samples=0)
    st._cleanup()
    st.detrend('linear')
    st.detrend('demean')
    st.filter("bandpass", freqmin=1, freqmax=45)


    if remove_sensor_response is True:
        inv = read_inventory(f"{SAC_PATH}metadata_2017-2020.xml")
        st.remove_response(inventory=inv)

    return st

data_start, data_end, station = "2017-06-09 12:00:00", "2017-06-09 18:00:00", "ILL12"
st = load_seismic_signal(data_start, data_end, station, component="EHZ", remove_sensor_response=False)
st.plot(outfile=f"{OUTPUT_DIR}{data_start}")