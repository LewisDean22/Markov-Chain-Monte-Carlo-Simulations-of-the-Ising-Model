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
import copy
from numpy import random

def generate_torus(J, spins_state):  ##  Maybe look for modulo for larger lengths.  ## Length input unnecessary as inputing array?
    length = len(spins_state)
    spins_state_torus = np.zeros((length+2, length+2))
    for i in range(length):
        for j in range(length):
            spins_state_torus[i+1, j+1] = spins_state[i,j]
    spins_state_torus[0, 1:-1] = spins_state[-1, :]
    spins_state_torus[1:-1, 0] = spins_state[:, -1]
    spins_state_torus[1:-1, -1] = spins_state[:, 0]
    spins_state_torus[-1, 1:-1] = spins_state[0, :]
    return spins_state_torus


def calculate_hamiltonian(J, spin_coordinate, spins_state):
    spins_state_torus = generate_torus(J, spins_state)
    i = spin_coordinate[0] + 1
    j = spin_coordinate[1] + 1
    hamiltonian_sum = (spins_state_torus[i,j] * (spins_state_torus[i, j+1]
                                                 + spins_state_torus[i+1, j]
                                                 + spins_state_torus[i, j-1]
                                                 + spins_state_torus[i-1, j]))
    energy = -J * hamiltonian_sum
    return energy


def calculate_dE_of_spin(J, spin_coordinate, spins_state, spin):
    updated_state = copy.deepcopy(spins_state)
    flipped = -spin
    updated_state[spin_coordinate] = flipped
    original_energy = calculate_hamiltonian(J, spin_coordinate, spins_state)
    updated_energy = calculate_hamiltonian(J, spin_coordinate, updated_state)
    dE = updated_energy - original_energy
    return dE


def choose_spins_to_flip(length, number_of_iterations):
    spins_to_flip = random.randint(length, size=(number_of_iterations, 2))
    return spins_to_flip


def decide_to_flip_spin(J, spin_coordinate, spins_state, spin):
    dE_of_spin = calculate_dE_of_spin(J, spin_coordinate, spins_state, spin)
    if dE_of_spin <= 0:
        print('FLIP {}'.format(spin_coordinate))
        return True
    # if (logic_for_heat_transfer_prob):  ## Add logic for rand. no. >= exp(dE/kT)
    #     return True
    return False


def find_new_state(J, spins_state, length, number_of_iterations):
    spins_to_flip = choose_spins_to_flip(length, number_of_iterations)
    new_state = np.copy(spins_state)
    for count, spin_position in enumerate(spins_to_flip):
        spin_coordinate = (spin_position[0], spin_position[1])
        spin = spins_state[spin_coordinate]
        spin_should_flip = decide_to_flip_spin(J, spin_coordinate, spins_state, spin)
        if spin_should_flip:
            new_state[spin_coordinate] = -spin
    return new_state
