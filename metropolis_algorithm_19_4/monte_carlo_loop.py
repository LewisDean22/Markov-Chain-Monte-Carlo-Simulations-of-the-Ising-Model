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
from new_state_generation import find_new_state
from show_state import plot_state #noqa


def find_state_progression(spins_state, T, J, length, number_of_iterations, steps):
    new_state = spins_state
    energies = np.zeros(steps)
    magnetisations = np.zeros(steps)
    
    for i in range(steps):
        new_state, energies[i], magnetisations[i] = (
            find_new_state(J, T, new_state, length, number_of_iterations))
    
    #plot_state(new_state, str(i))
    
    return new_state, energies, magnetisations
