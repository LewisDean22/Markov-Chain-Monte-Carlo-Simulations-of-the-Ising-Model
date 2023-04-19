# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:27:12 2023

Perhaps use finer temperature steps to get a smooth runtime curve - do for 
100,000 MC steps most, and for a small lattice size.

@author: lewis
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from property_calculator import identify_file_labels

RUNTIME_DIRECTORY = "Metropolis_runtime_data/"
SAVE = True


def split_runtime_data(length, mc_steps, directory=RUNTIME_DIRECTORY):
    filename = "runtime_data_{0}x{0}_MC_{1}_metropolis".format(length, mc_steps)
    
    runtime_data = (np.genfromtxt(directory + filename,
                                  delimiter=",", skip_header=1))
    
    temperature = runtime_data[:, 0]
    loop_time = runtime_data[:, 1]
    
    return temperature, loop_time


def plot_runtime_data(temperature, loop_time, length, mc_steps, save=SAVE):
    legend_label = '{0}x{0}\n{1} MC steps'.format(length, mc_steps)
    plt.plot(temperature, loop_time, label=legend_label, c='r')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    plt.xlabel('Temperature (K)')
    plt.ylabel('Monte Carlo loop time (s)')
    plt.title('Monte Carlo loop time as a function of temperature')
    plt.legend()
    
    if SAVE:
        plt.savefig("runtime_plots/runtime_{0}x{0}_MC_{1}".format(length,
                                                           mc_steps),
                    dpi=600)
    
    plt.show()
    plt.close()


def main(directory=RUNTIME_DIRECTORY):
    
    for file in os.listdir(directory):
        length, MC_steps = identify_file_labels(file)
        temperature, loop_time = split_runtime_data(length, MC_steps)
        plot_runtime_data(temperature, loop_time, length, MC_steps)
        
    return None


if __name__ == "__main__":
    main()
