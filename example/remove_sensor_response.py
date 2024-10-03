#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-09-23
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz-potsdam.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do NOT distribute this code without the author's permission

from obspy.signal.invsim import simulate_seismometer


def manually_remove_sensor_response(trace, sensor_type):
    '''
    manually remove the sensor response

    Parameters:
    - st (obspy.core.stream): seismic stream that deconvolved, make sure the stream only hase one trace
    - sensor_type (str): sensor type

    Returns:
    - st (obspy.core.stream): seismic stream that removed the sensor response
    '''

    corrected_trace = trace.copy()

    # reference,
    # https://www.gfz-potsdam.de/en/section/geophysical-imaging/infrastructure/geophysical-instrument-pool-potsdam-gipp/pool-components/clipp-werte
    # https://www.gfz-potsdam.de/en/section/geophysical-imaging/infrastructure/geophysical-instrument-pool-potsdam-gipp/pool-components/poles-and-zeros/trillium-c-120s
    # if you do not use the cube logger, the "Normalization factor" is 'gain'
    # if you do use the cube logger, refer link at "Sensitivity and clip values"

    paz_trillium_compact_120s_754 = {
        'zeros': [(0 + 0j),
                  (0 + 0j),
                  (-392 + 0j),
                  (-1960 + 0j),
                  (-1490 + 1740j),
                  (-1490 - 1740j)],

        'poles': [(-0.03691 + 0.03702j),
                  (-0.03691 - 0.03702j),
                  (-343 + 0j),
                  (-370 + 467j),
                  (-370 - 467j),
                  (-836 + 1522j),
                  (-836 - 1522j),
                  (-4900 + 4700j),
                  (-4900 - 4700j),
                  (-6900 + 0j),
                  (-15000 + 0j)],

        'gain': 4.34493e17,
        'sensitivity': 3.0172e8
    }

    paz_IGU_16HR_EB_3C_5Hz = {# works for Luding STA01, NOT for Dongchaun
        'zeros': [(0 + 0j),
                  (0 + 0j)],

        'poles': [(-22.211059 + 22.217768),
                  (-22.211059 - 22.217768j)],

        'gain': 76.7,
        'sensitivity': 6.40174e4
    }


    if sensor_type == "trillium_compact_120s_754":
        paz = paz_trillium_compact_120s_754
    elif sensor_type == "IGU_16HR_EB_3C_5Hz":
        paz = paz_IGU_16HR_EB_3C_5Hz
    else:
        print(f"please check the sensor_type: {sensor_type}")


    corrected_data = simulate_seismometer(trace[0].data, trace[0].stats.sampling_rate,
                                          paz_remove=paz, remove_sensitivity=True)
    corrected_trace[0].data = corrected_data

    return corrected_trace
