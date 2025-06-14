# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 11:10:37 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk

Improve speed with arrays

"""

import numpy as np
from initialise_model import initialise_random_state
from new_state_generation import find_new_state
from show_state import plot_state
from observables import *


def find_state_progression(spins_state, T, J, length, number_of_iterations, steps):
    new_state = spins_state
    energies = []
    magnetisations = []

    for i in range(steps):
        new_state, energy_of_state, magnetisation_of_state = find_new_state(J, T, new_state, length, number_of_iterations)
        energies += [energy_of_state]
        magnetisations += [magnetisation_of_state]
    
    #plot_state(new_state, str(i))
    energies = np.array(energies)
    magnetisations = np.array(magnetisations)
    
    return new_state, energies, magnetisations
