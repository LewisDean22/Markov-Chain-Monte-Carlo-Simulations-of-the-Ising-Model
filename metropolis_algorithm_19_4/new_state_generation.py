# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 11:04:22 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from numpy import random
from observables import *
import time
from print_formats import pvar


def calculate_dE_of_spin(J, spin_coordinate, spins_state):
    spin_energy = calculate_hamiltonian(J, spin_coordinate, spins_state)
    dE = -2 * spin_energy
    return dE


def choose_spins_to_flip(length, number_of_iterations):
    spins_to_flip = random.randint(length, size=(number_of_iterations, 2))
    return spins_to_flip


def decide_to_flip_spin(J, T, spin_coordinate, spins_state):
    dE_of_spin = calculate_dE_of_spin(J, spin_coordinate, spins_state)
    if dE_of_spin < 0:
        return True
    
    random_number = random.rand()
    if random_number < np.exp(-dE_of_spin / T):
        return True
    return False


def find_new_state(J, T, spins_state, length, number_of_iterations):
    '''
    spin_states changed to new_state in two locations now.

    '''
    # spins_flipped = 0
    
    spins_to_flip = choose_spins_to_flip(length, number_of_iterations)
    new_state = np.copy(spins_state)
    for count, spin_position in enumerate(spins_to_flip):
        
        spin_coordinate = (spin_position[0], spin_position[1])
        spin = new_state[spin_coordinate]
        
        spin_should_flip = decide_to_flip_spin(J, T, spin_coordinate, new_state)
        if spin_should_flip:
            new_state[spin_coordinate] = -spin
            #spins_flipped += 1
    
    
    energy_of_state = calculate_state_energy(J, new_state)
    magnetisation_of_state = calculate_state_magnetisation(new_state)
    return new_state, energy_of_state, magnetisation_of_state
    
    

    