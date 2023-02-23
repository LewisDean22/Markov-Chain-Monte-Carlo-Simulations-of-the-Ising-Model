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
import ising_model_bit_flip_lewis_incorperated_21_02_23 as ising


def calculate_state_magnetisation(spins_state):
    state_magnetisation = np.sum(spins_state)
    return state_magnetisation


def calculate_absolute_state_magnetisation(spins_state):
    state_magnetisation = calculate_state_magnetisation(spins_state)
    absolute_state_magnetisation = np.abs(state_magnetisation)
    return absolute_state_magnetisation


def calculate_expected_magnetisation(magnetisation, spins_state):  ##IDK if this is right
    expected_state_magnetisation = magnetisation / (len(spins_state)**2)
    return expected_state_magnetisation


def calculate_state_energy(J, spins_state):
    state_energy = 0
    for i in spins_state:
        for j in i:
            spin_energy = ising.calculate_hamiltonian(J, (i,j), spins_state)
            state_energy += spin_energy
    return state_energy


def calculate_expected_state_energy(state_energy, spins_state):  ##IDK about this one either
    expected_state_energy = state_energy / (2 * len(spins_state)**2)
    return expected_state_energy







