# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         What are the best boundary conditions
                         for wolff?
------------------------------------------------------------------------
Created: Mon Mar 13 12:51:42 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""


import numpy as np
from wolff_algorithm import find_cluster_progression
from initialise_model import initialise_random_state
import time as tm
import datetime
from colorama import Style, Fore
from joblib import Parallel, delayed
import pandas as pd

J_CONST = 1
LENGTH = 9
NUMBER_OF_MC_STEPS = 10000
INITIAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 0.5
TEMPERATURE_STEP = 0.1
TRANSIENT_PERIOD = 500

NUMBER_OF_CORES_USED = -1

WOLFF_TRANSIENTS = "Wolff_transient_data/"

WOLFF_DIRECTORY = "Monte_carlo_wolff_data/"
WOLFF_CUMULANT_DIRECTORY = "Wolff_cumulant_data/"
WORKING_DIRECTORY = WOLFF_DIRECTORY

MAGNETISATION_HEADERS = ['Temperature', 'Magnetisation',
                         'Absolute magnetisation', 'Magnetisation^2',
                         'Magnetisation^4']
ENERGY_HEADERS = ['Temperature', 'Energy', 'Energy^2']

SAVE_OBSERVABLES = True


def print_start_time():
    
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    print(Style.BRIGHT + Fore.GREEN + 'START TIME: {}'.format(time_str))
    

def calculate_average(observable, length=LENGTH,
                      mc_loops=NUMBER_OF_MC_STEPS):
    '''
    Turns observable data for a given temperature into an ensemble average, per
    spin site, of that observable for the inputted lattice size.

    '''
    
    return np.array(observable) / (mc_loops)


def generate_data_file(temperature_column, observable_columns, run_time,
                       header_list, length=LENGTH,
                       directory=WORKING_DIRECTORY,
                       mc_steps=NUMBER_OF_MC_STEPS):
    
    observable_type = header_list[1]
    data_length = len(temperature_column)
    column_number = 1 + len(observable_columns)
    
    file = np.empty((data_length, column_number))
    file[:,0] = temperature_column
    for count, column in enumerate(observable_columns, 1):
        file[:,count] = column

    observable_dataframe = pd.DataFrame(file, columns=header_list)
    filename = directory + "{0}_{1}x{1}_MC_{2}_wolff_{3:.0f}_Seconds".format(
        observable_type,length, mc_steps, run_time)
    observable_dataframe.to_csv(filename, index=0, header=1, sep=',')

    return None


def generate_transient_data_file(temperature_column, magnetisation_columns,
                                 length=LENGTH, directory=WOLFF_TRANSIENTS,
                                 period=TRANSIENT_PERIOD):
    
    width = len(temperature_column)
    height = len(magnetisation_columns[0]) + 1
    
    file = np.zeros((height, width))
    file[0, :] = temperature_column
    for index in range(width):
        file[1:, index] = magnetisation_columns[index]

    observable_dataframe = pd.DataFrame(file)
    filename = directory + "Transients_{0}x{0}_PERIOD_{1}_wolff".format(
        length, period)
    observable_dataframe.to_csv(filename, index=0, header=0, sep=',')

    return None


def parallel_temp_steps(temp, length=LENGTH):
    
    initial_state = initial_state = initialise_random_state(length)
    
    (equilibrium_state,
     transient_energy,
     transient_magnetisation_data) = find_cluster_progression(initial_state, temp,
                                                  LENGTH,
                                                  TRANSIENT_PERIOD,
                                                  J_CONST)
    # new_state = equilibrium_state
    (arbitrary_state, energies, 
     magnetisations) = find_cluster_progression(equilibrium_state,
                                                temp,
                                                length,
                                                NUMBER_OF_MC_STEPS,
                                                J_CONST)
                                                
    total_magnetisation = np.sum(magnetisations)
    total_magnetisation_abs = np.sum(abs(magnetisations))
    total_magnetisation_squared = np.sum((magnetisations)**2)
    total_magnetisation_4 = np.sum((magnetisations)**4)
    
    total_energy = np.sum(energies)
    total_energy_squared = np.sum((energies)**2)
    
    
    return [temp, transient_magnetisation_data, total_magnetisation, total_magnetisation_abs,
            total_magnetisation_squared, total_magnetisation_4,
            total_energy, total_energy_squared]


def main(n_cores=NUMBER_OF_CORES_USED):
    
    print_start_time()
    start_main = tm.time()
    
    temperature_range = np.arange(MINIMUM_TEMPERATURE,
                                  INITIAL_TEMPERATURE + TEMPERATURE_STEP,
                                  TEMPERATURE_STEP)[::-1]

    total_temp_steps = len(temperature_range)

    magnetisation = np.zeros(total_temp_steps)
    magnetisation_abs = np.zeros(total_temp_steps)
    magnetisation_squared = np.zeros(total_temp_steps)
    magnetisation_4 = np.zeros(total_temp_steps)
    
    energy = np.zeros(total_temp_steps)
    energy_squared = np.zeros(total_temp_steps)
    
    transient_magnetisations = np.zeros((total_temp_steps, TRANSIENT_PERIOD))
    
    results = Parallel(n_jobs=n_cores)(
        delayed(parallel_temp_steps)(temp) for temp in temperature_range)
    
    for index, array in enumerate(results):
        (temp, transient_magnetisation_data, total_magnetisation,
         total_magnetisation_abs, total_magnetisation_squared,
         total_magnetisation_4, total_energy,
         total_energy_squared) = array
    
        magnetisation[index] = total_magnetisation
        magnetisation_abs[index] = total_magnetisation_abs
        magnetisation_squared[index] = total_magnetisation_squared
        magnetisation_4[index] = total_magnetisation_4
        energy[index] = total_energy
        energy_squared[index] = total_energy_squared
        
        for count, val in enumerate(transient_magnetisation_data):
            transient_magnetisations[index][count] = val
        
    energy_list = calculate_average((energy, energy_squared))
    magnetisation_list = calculate_average((magnetisation, magnetisation_abs,
                                            magnetisation_squared,
                                            magnetisation_4))
    
    end_main = tm.time()
    run_time = end_main-start_main
    
    if SAVE_OBSERVABLES:
        generate_data_file(temperature_range, magnetisation_list, run_time,
                           MAGNETISATION_HEADERS)
    
        generate_data_file(temperature_range, energy_list, run_time,
                           ENERGY_HEADERS)
        
        generate_transient_data_file(temperature_range,
                                     transient_magnetisations)
    
    
    end_main = tm.time()
    print(Fore.RESET + "Run time = {:.0f} s".format(run_time))
    
    return 0

if __name__ == "__main__":
    main()