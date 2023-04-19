# -*- coding: utf-8 -*-
"""
Title: Metropolis main
------------------------------------------------------------------------
      Export as csv for the real thing
      
      
      ----------> For Robino <-----------
      
      The main change is that now the averages are observable per spin because
      the division by L^2 is inside the sums. There is no more L^2 in the 
      calculate_avaerage function. We were originally finding the averages for
      the whole lattice and then just dividing by the number of spin sites.This
      is subtly different to the new approach and I have now derived different
      variances for use in the property calculator, which give the same plots
      as before.
      
      It probably doesn't matter since the plots are unchanged, but the point
      is that now we can show where our calculations have come from...
      
      There is a new cumulant directory too (shown in the global variables)
      which is where the data for curie_temp_calculator should be stored. It
      is very different data in both its temp range and temp step.
      
      This new directory needs selecting in the global variables of property
      calculator too when trying to use curie_temp_calculator, instead of the
      property_plotter.
      
      Does initial state = equilibrium state break the plots of non-absolute
      magnetisation per spin as now, for a given lattice size, they stay fixed
      at either + or -1 instead of converging on different ones for each new
      temp step. This may make the lattice evolution non-ergodic which may
      break some statistical mechanics stuff...
      
      Could we try a higher number of iterations before sampling from the
      state space? Maybe this would reduce the impact of critical slowdown
      close to the curie temperature.
      
      
------------------------------------------------------------------------
Created: Thu Feb 31 20:03:13 2003
Author: Robin De Freitas et Moi
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""
from initialise_model import initialise_random_state, initialise_ones_state #noqa
from monte_carlo_loop import find_state_progression

import numpy as np
import datetime
import time as tm
from colorama import Style, Fore
import pandas as pd
import cProfile
import pstats
import os #noqa


J_CONST = 1
LENGTH = 2
NUMBER_OF_ITERATIONS = LENGTH**2
NUMBER_OF_MC_STEPS = 10_000
INITIAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 0.5
TEMPERATURE_STEP = 0.1
TRANSIENT_PERIOD = 1000

RUNTIME_DIRECTORY = "Metropolis_runtime_data/"

METROPOLIS_DIRECTORY = "Monte_carlo_metropolis_data/"
METROPOLIS_CUMULANT_DIRECTORY = "Metropolis_cumulant_data/"
WORKING_DIRECTORY = METROPOLIS_DIRECTORY
SAVE_OBSERVABLES = True
SAVE_STATS = False

MAGNETISATION_HEADERS = ['Temperature', 'Magnetisation',
                         'Absolute magnetisation', 'Magnetisation^2',
                         'Magnetisation^4']
ENERGY_HEADERS = ['Temperature', 'Energy', 'Energy^2']


def print_start_time():
    
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    print(Style.BRIGHT + Fore.GREEN + 'START TIME: {}'.format(time_str))


def percentage_update(current_step, initial_temp=INITIAL_TEMPERATURE,
                      min_temp=MINIMUM_TEMPERATURE, temp_step=TEMPERATURE_STEP):
    
    number_of_steps_required = (initial_temp - min_temp)/temp_step
    percentage_done = (current_step/number_of_steps_required)*100
    if percentage_done <= 100:
        print(Style.BRIGHT + Fore.GREEN + '{:.0f}% complete...'.format(percentage_done))
    

def calculate_average(observable, length=LENGTH, mc_loops=NUMBER_OF_MC_STEPS):
    '''
    Turns observable data for a given temperature into an ensemble average, per
    spin site, of that observable for the inputted lattice size.

    '''
    
    return np.array(observable) / (mc_loops)


def generate_data_file(temperature_column, observable_columns, header_list,
                       length=LENGTH, directory=WORKING_DIRECTORY,
                       mc_steps=NUMBER_OF_MC_STEPS):
    
    observable_type = header_list[1]
    data_length = len(temperature_column)
    column_number = 1 + len(observable_columns)
    
    file = np.empty((data_length, column_number))
    file[:,0] = temperature_column
    for count, column in enumerate(observable_columns, 1):
        file[:,count] = column

    observable_dataframe = pd.DataFrame(file, columns=header_list)
    filename = directory + "{0}_{1}x{1}_MC_{2}_metropolis".format(observable_type,
                                                                  length, mc_steps)
    observable_dataframe.to_csv(filename, index=0, header=1, sep=',')

    return None


def generate_runtime_file(temperature_column, runtime_column,
                          length=LENGTH, directory=RUNTIME_DIRECTORY,
                          mc_steps=NUMBER_OF_MC_STEPS):
    
    file = np.column_stack((temperature_column, runtime_column))
    
    runtime_headers = ['Temperature', 'Monte carlo loop time']
    observable_dataframe = pd.DataFrame(file, columns=runtime_headers)
    filename = directory + "runtime_data_{0}x{0}_MC_{1}_metropolis".format(length,
                                                                           mc_steps)
    observable_dataframe.to_csv(filename, index=0, header=1, sep=',')

    return None


def main(length=LENGTH): 
    profiler = cProfile.Profile()
    profiler.enable()
    
    print_start_time()
    
    start_main = tm.time()
    current_step = 0
    
    temperature_range = []
    energy = []
    energy_squared = []
    magnetisation = []
    magnetisation_abs = []
    magnetisation_squared = []
    magnetisation_4 = []
    monte_carlo_loop_time = []
    
    temperature = INITIAL_TEMPERATURE
    initial_state = initialise_ones_state(length)
    
    while temperature >= MINIMUM_TEMPERATURE:
        temp_start_time = tm.time()
        
        equilibrium_state, arbitrary_energies, arbitrary_magnetisations = find_state_progression(initial_state, temperature, J_CONST, length, NUMBER_OF_ITERATIONS, TRANSIENT_PERIOD)
        
        arbitrary_state, energies, magnetisations = find_state_progression(equilibrium_state, temperature, J_CONST, length, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_STEPS)
        
        total_magnetisation = np.sum(magnetisations)
        total_magnetisation_abs = np.sum(abs(magnetisations))
        total_magnetisation_squared = np.sum((magnetisations)**2)
        total_magnetisation_4 = np.sum((magnetisations)**4)
        
        magnetisation += [total_magnetisation]
        magnetisation_abs += [total_magnetisation_abs]
        magnetisation_squared += [total_magnetisation_squared]
        magnetisation_4 += [total_magnetisation_4]
        
        total_energy = np.sum(energies)
        total_energy_squared = np.sum((energies)**2)
        
        energy += [total_energy] 
        energy_squared += [total_energy_squared]
        
        temperature_range += [temperature]
        temperature -= TEMPERATURE_STEP
        initial_state = equilibrium_state
        
        temp_end_time = tm.time()
        monte_carlo_loop_time += [temp_end_time-temp_start_time]
        
        current_step += 1
        percentage_update(current_step)
    
    energy_list = calculate_average((energy, energy_squared))
    magnetisation_list = calculate_average((magnetisation, magnetisation_abs,
                                            magnetisation_squared,
                                            magnetisation_4))
    if SAVE_OBSERVABLES:
        generate_data_file(temperature_range, magnetisation_list,
                           MAGNETISATION_HEADERS)
    
        generate_data_file(temperature_range, energy_list, ENERGY_HEADERS)
    
    generate_runtime_file(temperature_range, monte_carlo_loop_time)
    
    end_main = tm.time()
    print(Fore.RESET + "Run time = {:.3f} s".format(end_main-start_main))
    
    profiler.disable()
    
    if SAVE_STATS:
        profiler.dump_stats("execution_data.prof")
        stats = pstats.Stats("execution_data.prof")
        print('\n')
        stats.sort_stats("tottime").print_stats(10)
        os.system('cmd /k "snakeviz execution_data.prof"')


if __name__ == "__main__":
     main()