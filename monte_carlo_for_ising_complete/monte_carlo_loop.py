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
"""

import numpy as np
from initialise_model import initialise_random_state
from new_state_generation import find_new_state
from show_state import plot_state
from observables import *


def find_state_progression(spins_state, T, J, length, number_of_iterations, number_of_mc_loops):
    new_state = spins_state
    energies = []
    magnetisations = []
    # list_of_states = [new_state]
    for i in range(number_of_mc_loops):
        new_state, energy_of_state, magnetisation_of_state = find_new_state(J, T, new_state, length, number_of_iterations)
        print('\nNEW STATE {}'.format(i))
        print(new_state)
        energies += [energy_of_state]
        magnetisations += [magnetisation_of_state]
    plot_state(new_state, str(i))
    energies = np.array(energies)
    magnetisations = np.array(magnetisations)
    return new_state, energies, magnetisations


def main():
    initial_state = initialise_random_state(LENGTH)
    find_state_progression(initial_state)
    print("COMPLETE")


if __name__ == "__main__":
    main()