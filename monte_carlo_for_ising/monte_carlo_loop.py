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

J_CONST = 1
LENGTH = 5
NUMBER_OF_ITERATIONS = 10
NUMBER_OF_MC_LOOPS = 100
TEMPERATURE = 1


def find_state_progression(spins_state, J=J_CONST, length=LENGTH, number_of_iterations=NUMBER_OF_ITERATIONS, number_of_mc_loops=NUMBER_OF_MC_LOOPS):
    new_state = spins_state
    list_of_states = [new_state]
    for i in range(number_of_mc_loops):
        new_state = find_new_state(J, new_state, length, number_of_iterations)
        print('\nNEW STATE {}'.format(i))
        print(new_state)
        plot_state(new_state, str(i))
        list_of_states += [new_state]
        if np.all(new_state == 1) or np.all(new_state == -1):
            return list_of_states
    return list_of_states


def main():
    initial_state = initialise_random_state(LENGTH)
    find_state_progression(initial_state)


if __name__ == "__main__":
    main()