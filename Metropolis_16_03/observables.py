# -*- coding: utf-8 -*-
"""
Title: Ising model observables
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 10:06:00 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from print_formats import pvar #noqa


def calculate_hamiltonian(J, spin_coordinate, spins_state):
    modulo_length = len(spins_state)
    i = spin_coordinate[0]
    j = spin_coordinate[1]

    left = (i - 1) % modulo_length
    right = (i + 1) % modulo_length
    up = (j - 1) % modulo_length
    down = (j + 1) % modulo_length
    hamiltonian_sum = (spins_state[(i, j)] * (spins_state[(left, j)]
                                          + spins_state[(right, j)]
                                          + spins_state[(i, up)]
                                          + spins_state[(i, down)]))
    
    energy = -J * hamiltonian_sum
    return energy


def calculate_boltzmann_factor(E, T):
    return np.exp(-E / T)


def calculate_state_energy(J, spins_state):
    state_energy = 0
    for i in range(len(spins_state)):

        for j in range(len(spins_state)):
            spin_energy = calculate_hamiltonian(J, (i,j), spins_state)
            state_energy += spin_energy

    return 0.5*state_energy


def calculate_state_magnetisation(spins_state):
    state_magnetisation = np.sum(spins_state)
    return state_magnetisation
