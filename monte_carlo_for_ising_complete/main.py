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
from initialise_model import initialise_random_state
from monte_carlo_loop import find_state_progression
from show_state import plot_state
from observables import *
import matplotlib.pyplot as plt

J_CONST = 1
LENGTH = 5
NUMBER_OF_ITERATIONS = LENGTH**2
NUMBER_OF_MC_LOOPS = 1000
INITIAL_TEMPERATURE = 5
MINIMUM_TEMPERATURE = 0.5
TEMPERATURE_STEP = 0.1
TRANSIENT_PERIOD = 100
NORM = 1 / (NUMBER_OF_MC_LOOPS * NUMBER_OF_ITERATIONS)
SAVE = False


def main():
    temperature_range = []
    energy = []  
    magnetisation = []

    temperature = INITIAL_TEMPERATURE
    initial_state = initialise_random_state(LENGTH)
    
    while temperature >= MINIMUM_TEMPERATURE:
        equilibrium_state, arbitrary_energies, arbitrary_magnetisations = find_state_progression(initial_state, temperature, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, TRANSIENT_PERIOD) #no of loops to transient
        
        arbitrary_state, energies, magnetisations = find_state_progression(equilibrium_state, temperature, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
        
        total_magnetisation = np.sum(magnetisations)
        magnetisation += [total_magnetisation]
        total_energy = np.sum(energies)
        energy += [total_energy]
        temperature_range += [temperature]
        temperature -= TEMPERATURE_STEP
    
    magnetisation_data = np.zeros((len(temperature_range), 2))
    magnetisation_data[:,0] = temperature_range
    magnetisation_data[:,1] = magnetisation
    
    energy_data = np.zeros((len(temperature_range), 2))
    energy_data[:,0] = temperature_range
    energy_data[:,1] = energy
    
    if SAVE:
        np.savetxt("magnetisation_{0}x{0}".format(LENGTH), magnetisation_data)
        np.savetxt("energy_{0}x{0}".format(LENGTH), energy_data)


if __name__ == "__main__":
    main()
