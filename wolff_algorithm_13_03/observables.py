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

def calculate_expected_of_observable(observable, norm):
    total_observable = np.sum(observable)
    return total_observable * norm


def calculate_hamiltonian(J, spin_coordinate, spins_state):
    modulo_length = len(spins_state)
    i = spin_coordinate[0]
    j = spin_coordinate[1]
    
    left = (i - 1) % modulo_length
    right = (i + 1) % modulo_length
    up = (j - 1) % modulo_length
    down = (j + 1) % modulo_length
    
    # pvar(i)
    # pvar(j)
    # pvar(left)
    # pvar(right)
    # pvar(up)
    # pvar(down)
    
    hamiltonian_sum = (spins_state[i, j] * (spins_state[left, j]
                                          + spins_state[right, j]
                                          + spins_state[i, up]
                                          + spins_state[i, down]))
    energy = -J * hamiltonian_sum
    return energy


def calculate_state_energy(J, spins_state):  ## Maybe a divide by 2 here somewhere.
    state_energy = 0
    for i in range(len(spins_state)):
        for j in range(len(spins_state)):
            spin_energy = calculate_hamiltonian(J, (i,j), spins_state)
            state_energy += spin_energy
    return 0.5 * state_energy


def calculate_state_magnetisation(spins_state):
    state_magnetisation = np.sum(spins_state)
    return state_magnetisation


def calculate_total_magnetisation(magnetisations):
    total_magnetisation = np.sum(magnetisations)
    return total_magnetisation


def calculate_total_absolute_magnetisation(magnetisations):
    total_absolute_magnetisation = np.sum(np.abs(magnetisations))
    return total_absolute_magnetisation


def calculate_total_magnetisation_squared(total_magnetisation):
    total_magnetisation_squared = np.sum(total_magnetisation**2)
    return total_magnetisation_squared


def calculate_total_magnetisation_quarted(total_magnetisation):
    total_magnetisation_quarted = np.sum(total_magnetisation**4)
    return total_magnetisation_quarted







def calculate_expected_state_energy(state_energy, spins_state):  ##IDK about this one either
    expected_state_energy = state_energy / (2 * len(spins_state)**2)
    return expected_state_energy







