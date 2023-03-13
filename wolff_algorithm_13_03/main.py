# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Mon Mar 13 12:51:42 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""


import numpy as np
from wolff_algorithm import find_cluster_progression
import time as tm
from colorama import Style, Fore

LENGTH = 25
NUMBER_OF_ITERATIONS = 100_000
TRANSIENT_PERIOD = 500
J_CONST = 1
MINIMUM_TEMPERATURE = 0.5
MAXIMUM_TEMPERATURE = 5
TEMPERATURE_STEP = 0.1
NORM = LENGTH**2 * NUMBER_OF_ITERATIONS


def main():
    start = tm.time()
    number_of_steps = ((MAXIMUM_TEMPERATURE - MINIMUM_TEMPERATURE) / TEMPERATURE_STEP) + 1
    print(number_of_steps)
    number_of_steps = int(number_of_steps) # this int is a hack need to ensure number of steps goes nicely
    print(number_of_steps)
    
    magnetisation = np.zeros(number_of_steps)
    magnetisation_abs = np.zeros(number_of_steps)
    magnetisation_squared = np.zeros(number_of_steps)
    magnetisation_4 = np.zeros(number_of_steps)
    
    energy = np.zeros(number_of_steps)
    energy_squared = np.zeros(number_of_steps)
    
    temperature_range = np.zeros(number_of_steps)
    
    temperature = MAXIMUM_TEMPERATURE
    count = 0
    while temperature >= MINIMUM_TEMPERATURE:
    
        new_state, a, b, c, d, e, f = find_cluster_progression(temperature, LENGTH, TRANSIENT_PERIOD, J_CONST)
    
        (g, total_magnetisation, 
         total_magnetisation_abs, 
         total_magnetisation_squared, 
         total_magnetisation_4, 
         total_energy, 
         total_energy_squared) = find_cluster_progression(temperature, LENGTH, NUMBER_OF_ITERATIONS, J_CONST)
    
        magnetisation[count] = total_magnetisation * NORM #Normalise here
        magnetisation_abs[count] = total_magnetisation_abs * NORM
        magnetisation_squared[count] = total_magnetisation_squared * NORM
        magnetisation_4[count] = total_magnetisation_4 * NORM
        
        energy[count] = total_energy * NORM
        energy_squared[count] = total_energy_squared * NORM
        
        temperature_range[count] = temperature

        count += 1
        temperature -= TEMPERATURE_STEP
        
        print(Style.BRIGHT + Fore.RED + "Temperature: {}".format(temperature))
        print(Style.RESET_ALL)
        
    
    magnetisation_data = np.column_stack((temperature_range,
                                          magnetisation,
                                          magnetisation_abs,
                                          magnetisation_squared,
                                          magnetisation_4))
    energy_data = np.column_stack((temperature_range, energy, energy_squared))
    
    print(magnetisation_data)
    print(energy_data)
    
    np.savetxt("magnetisation_{0}x{0}.csv".format(LENGTH), magnetisation_data, delimiter=',')
    np.savetxt("energy_{0}x{0}.csv".format(LENGTH), energy_data, delimiter=',')
    
    
    end = tm.time()
    print('Time taken: {:.3f}s'.format(end - start))
    return 0

if __name__ == "__main__":
    main()