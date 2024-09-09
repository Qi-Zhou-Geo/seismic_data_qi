#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-09-09
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz-potsdam.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do not distribute this code without the author's permission

from obspy import read, Stream, UTCDateTime, read_inventory

def remove_sensor_response_manually(trace, sensorType):
    '''
    visuzlice the PSD

    Parameters:
    - st (obspy.core.stream): seismic stream that deconvolved, make sure the stream only hase one trace
    - sensorType (str): sensor type

    Returns:
    - st (obspy.core.stream): seismic stream that removed the sensor response
    '''

    from obspy.signal.invsim import simulate_seismometer
    corrected_trace = trace.copy()

    paz_geophone_pe6b = {
        'poles': [(-15.88 + 23.43j),
                  (-15.88 - 23.43j)],
        'zeros': [0j, 0j],
        'gain': 32,
        'sensitivity': 1.3115e8
    }

    paz_SmartSolo_IGU_16_5hz = {
        'poles': [-22.211059 + 22.217768j, -22.211059 + 22.217768j],
        'zeros': [0j, 0j],
        'gain': 24,
        'sensitivity': 7.68e1}

    if sensorType == "geophone":
        sensorLogger = paz_geophone
    elif sensorType == "trillum":
        sensorLogger = paz_trillum
    elif sensorType == "SmartSolo_5Hz":
        sensorLogger = paz_SmartSolo_IGU_16_5hz
    elif sensorType == "geophone_pe6b":
        sensorLogger = paz_geophone_pe6b
    else:
        print("please check the sensorType")

    corrected_data = simulate_seismometer(trace[0].data, trace[0].stats.sampling_rate,
                                          paz_remove=sensorLogger,  # or paz_trillum depending on your choice
                                          remove_sensitivity=True)


    corrected_trace[0].data = corrected_data

    return corrected_trace

