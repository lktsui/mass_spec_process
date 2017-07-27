import numpy as np
import os
from datetime import datetime


def load_mass_spec_data():

    """
    Loads the mass_spec.csv file from the input directory


    :return:
    """
    data_collect = False
    t_0 = datetime.strptime("00:00:00", "%H:%M:%S")
    ms_elapsed_time_array = []
    ms_signals = {}
    for index, line in enumerate(open(os.path.join('input', 'mass_spec.csv'), 'r').readlines()):

        if data_collect:

            data_elements = line.split(',')
            timestamp = data_elements[0]
            time_obj = datetime.strptime(timestamp, "%H:%M:%S")
            elapsed_time = (time_obj-t_0).total_seconds()
            ms_elapsed_time_array.append(float(elapsed_time))

            for key in ms_signals.keys():

                data_index = ms_signals[key]['index']
                concentration_str =  data_elements[data_index]
                concentration_signal = float(concentration_str)
                ms_signals[key]['array'].append(concentration_signal)

        else:
            if line.startswith("\"Time"):

                # set the gas channels
                header_elements = line.split(',')
                for index, key in enumerate(header_elements[2:-1]):
                    ms_signals[key] = {"index":index+2, "array":[]}
                data_collect = True

    return np.array(ms_elapsed_time_array), ms_signals

def load_temperature_data():


    data_collect = False
    temp_time_array = []
    temperature_array = []
    for index, line in enumerate(open(os.path.join('input', 'temperature.txt'), 'r').readlines()):

        if data_collect:

            data_elements = line.split(';')
            if len(data_elements) > 2:
                elapsed_time = float(data_elements[1])*60
                temp = float(data_elements[0])
                temp_time_array.append(elapsed_time)
                temperature_array.append(temp)
        else:
            if line.startswith("##Temp"):
               data_collect = True

    return np.array(temp_time_array), np.array(temperature_array)


def output_data(ms_elapsed_time_array, ms_signals, temp_time_array, temperature_array):

    output_file = open(os.path.join('output', 'output.txt'), 'w')

    ms_signals_interp = []

    header = "Time (s), Temperature (DegC),"
    for key in sorted(ms_signals.keys()):
        header += key +","
        signal_array = np.array(ms_signals[key]['array'])
        interp_signal_array = np.interp(temp_time_array, ms_elapsed_time_array, signal_array)
        ms_signals_interp.append(interp_signal_array)

    header += '\n'
    output_file.write(header)

    for index, time_point in enumerate(temp_time_array):
        data_line = "%6.4e, %6.4e,"%(time_point, temperature_array[index])

        for signal_array in ms_signals_interp:
            signal_point = signal_array[index]
            data_line += "%6.4e,"%signal_point

        data_line += "\n"
        output_file.write(data_line)





if __name__ == '__main__':

    ms_elapsed_time_array, ms_signals = load_mass_spec_data()
    temp_time_array, temperature_array = load_temperature_data()
    output_data(ms_elapsed_time_array, ms_signals, temp_time_array, temperature_array)
