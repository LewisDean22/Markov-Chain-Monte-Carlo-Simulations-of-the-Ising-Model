# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 20:03:13 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from initialise_model import initialise_random_state, initialise_ones_state
from monte_carlo_loop import find_state_progression
from show_state import plot_state
from observables import *
import matplotlib.pyplot as plt
import time as tm

J_CONST = 1 # High J corresponds to materials with high curie temperature
LENGTH = 3
NUMBER_OF_ITERATIONS = LENGTH
NUMBER_OF_MC_STEPS = 100_000
INITIAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 0.1
TEMPERATURE_STEP = 0.1
TRANSIENT_PERIOD = 1000
DIRECTORY = "Monte_carlo_data/"
SAVE = True


def main():
    start = tm.time()
    temperature_range = []
    energy = []  
    magnetisation = []

    temperature = INITIAL_TEMPERATURE
    initial_state = initialise_ones_state(LENGTH)
    
    while temperature >= MINIMUM_TEMPERATURE:
        equilibrium_state, arbitrary_energies, arbitrary_magnetisations = find_state_progression(initial_state, temperature, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, TRANSIENT_PERIOD) #no of loops to transient
        
        arbitrary_state, energies, magnetisations = find_state_progression(equilibrium_state, temperature, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_STEPS)
        
        total_magnetisation = np.sum(magnetisations)
        magnetisation += [total_magnetisation]
        total_energy = 0.5*np.sum(energies) # Factor of 0.5 added here??
        energy += [total_energy]
        temperature_range += [temperature]
        temperature -= TEMPERATURE_STEP
        print(temperature)
    
    magnetisation_data = np.zeros((len(temperature_range), 2))
    magnetisation_data[:,0] = temperature_range
    magnetisation_data[:,1] = magnetisation
    
    energy_data = np.zeros((len(temperature_range), 2))
    energy_data[:,0] = temperature_range
    energy_data[:,1] = energy
    
    if SAVE:
        np.savetxt(DIRECTORY + "magnetisation_{0}x{0}".format(LENGTH), magnetisation_data,
                   delimiter = ',')
        np.savetxt(DIRECTORY + "energy_{0}x{0}".format(LENGTH), energy_data,
                   delimiter = ',')
    end = tm.time()
    print("Run time = {:.3f} s".format(end-start))


if __name__ == "__main__":
    main()