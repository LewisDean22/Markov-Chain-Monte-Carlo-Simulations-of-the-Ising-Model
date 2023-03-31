# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 00:57:54 2023

Poorly made at the moment so the working directory needs updating both here
and in property calculator when running!!! <---------------------------

@author: lewis
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import math
import pandas as pd #noqa
from property_calculator import * #noqa

LINESTYLE = ('solid', 'dotted', 'dashed', 'dashdot', (0, (1, 1)))
METROPOLIS_CUMULANT_DIRECTORY = "Metropolis_cumulant_data/"
WORKING_DIRECTORY = METROPOLIS_CUMULANT_DIRECTORY
# Read the document header if having directory issues!

def magnetisation_file_finder(directory):
    
    magnetisation_data_list = []
    for file in os.listdir(directory):
        if file.startswith("Magnetisation"):
            magnetisation_data_list.append(file)
    
    return magnetisation_data_list


def file_truncator(data_files):
    '''
    This was made quickly to deal with an error in data files of different
    length. The file truncator works for when there is variation in the minimum
    temperature set in the metropolis main script.
    
    Made to fix the 1_000_000 step (4x4) from the 2.0-2.4 K because the other
    data files have 100_000 steps with temp range 1.9-2.4 K. Having the same
    temp step is essential for the premise of cumulant intersection
    identification.

    '''
    lengths = []
    truncated_files = []
    
    for file in data_files:
        lengths += [len(file)]
    min_length = np.min(lengths)
    for file in data_files:
        truncated_files += [file[:min_length]]
    
    return np.array(truncated_files)
    
    
def main(directory=WORKING_DIRECTORY, linestyle=LINESTYLE):
    '''
    Crucially, the MC steps must be high because the cumulant plot shows how
    fluctuations in cumulant value due to poor averaging creates a plethora of
    intersection points between cumulant pairs.

    '''
    
    magnetisation_data_list = magnetisation_file_finder(directory)
    curie_cumulants = []
    lengths_list = []

    for count, magnetisation_filename in enumerate(magnetisation_data_list):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = (
             calculate_magnetic_properties(magnetisation_filename))
        
        plt.plot(temperature_data, cumulant,
                 label='{0}x{0}'.format(length),
                 linestyle=linestyle[count])
        
        curie_cumulants += [cumulant]
        lengths_list += [length]

    plt.legend()
    plt.title("Cumulant intersection plot")
    plt.xlabel('Temperature')
    # plt.xlim(2, 2.25)
    plt.ylabel("Cumulant value")
    # plt.ylim(0.5, 0.8)
    plt.show()
    plt.close()
    
    curie_cumulants = file_truncator(np.array(curie_cumulants, dtype=object))
    curie_cumulants = np.array(curie_cumulants, dtype=float)
    
    width = len(curie_cumulants[0])
    height = len(magnetisation_data_list)
    np.reshape(curie_cumulants, (width,height))
    
    header_list = np.around(temperature_data[:width], 2)
    indices = []
    for count in range(height):
        length = lengths_list[count]
        indices.append('{0}x{0} Cumulant'.format(length)) 
    
    cumulant_dataframe = pd.DataFrame(curie_cumulants, columns=header_list)
    cumulant_dataframe.insert(0, 'Temperature', indices)
    cumulant_dataframe.insert(1, '|' , ['|']*len(indices))
    filename = directory + "cumulant_dataframe"
    cumulant_dataframe.to_csv(filename, index=0, header=1, sep=',')
    
    cumulant_std = np.std(curie_cumulants, axis=0)
    curie_temperature_arg = np.argmin(cumulant_std)
    curie_temperature = temperature_data[curie_temperature_arg]
    print("Cumulant Curie temperatures = {0:.2f}".format(curie_temperature))


if __name__ == "__main__":
    main()