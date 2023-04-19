# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 23:37:16 2023

Note: the rounding for the sake of the titles is not perfect and would break
if Temp step wasn't 0.1

When you want to stop plotting convergence plots for old data, move into a 
'Storage' folder made inside of Metropolis_transient_data/. Do not delete any
old data unnecessarily.

@author: lewis
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re

METROPOLIS_TRANSIENTS = "Metropolis_transient_data/"
WOLFF_TRANSIENTS = "Wolff_transient_data/"
WORKING_DIRECTORY = WOLFF_TRANSIENTS

# Set to 'MAX' or an integer
MC_STEP_PLOT_LIMIT = 'MAX'


def file_finder(directory):

    transient_data = []
    for file in os.listdir(directory):
        transient_data.append(file)

    return transient_data


def identify_file_labels(data_filename):
    labels = re.findall("[^_]*", data_filename)
    length = re.findall("\d+", data_filename)[0]
    period = labels[-4]
    
    return length, period


def import_data(filename,
               directory=WORKING_DIRECTORY):
    
    data = (np.genfromtxt(directory + filename,
                          delimiter=",", skip_header=0))
    
    return data


def main(directory=WORKING_DIRECTORY):
    
    transient_datasets = file_finder(directory)
    for file in transient_datasets:
        length, period = identify_file_labels(file)
        transient_data = import_data(file)
        
        total_spins = int(length)**2
        mc_steps = np.arange(1, int(period) + 1 , 1)
        
        for index, temp in enumerate(transient_data[0]):
            
            temp = round(temp, 1)
            magnetisation_data = transient_data[1:, index] / total_spins
        
            plt.xlabel("MC Steps")
            if MC_STEP_PLOT_LIMIT != 'MAX':
                plt.xlim(MC_STEP_PLOT_LIMIT)
            plt.ylabel("Magnetisation per spin")
            plt.title("T = {0}, {1}x{1} thermalisation plot".format(temp,
                                                                    length))
            plt.plot(mc_steps, magnetisation_data)
            
            plt.show()
            plt.close()
    

if __name__ == "__main__":
    main()
