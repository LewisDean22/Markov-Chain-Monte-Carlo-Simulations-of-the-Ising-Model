# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Wed Feb 22 09:53:03 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
import ising_model_bit_flip_lewis_incorperated_21_02_23 as ising
from print_formats import pvar


J_CONST = 1
LENGTH = 5
NUMBER_OF_ITERATIONS = 10
NUMBER_OF_MC_LOOPS = 100
TEMPERATURE = 1


def find_state_progression(spins_state, J=J_CONST, length=LENGTH, number_of_iterations=NUMBER_OF_ITERATIONS, number_of_mc_loops=NUMBER_OF_MC_LOOPS):
    new_state = spins_state
    list_of_states = [new_state]
    for i in range(number_of_mc_loops):
        new_state = ising.find_new_state(J, new_state, length, number_of_iterations)
        print('\nNEW STATE {}'.format(i))
        print(new_state)
        ising.plot_state(new_state, str(i))
        list_of_states += [new_state]
        if np.all(new_state == 1) or np.all(new_state == -1):
            return list_of_states
    return list_of_states


def main():
    initial_state = ising.initialise_random_state(LENGTH)
    find_state_progression(initial_state)


if __name__ == "__main__":
    main()
    