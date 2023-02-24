# -*- coding: utf-8 -*-
"""
Title: Initialise state
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 10:55:37 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from numpy import random


def initialise_ones_state(length):
    initial_state = np.ones((length, length))
    return initial_state


# def initialise_random_state(length):
#     initial_state = random.randint(0, 2, size=(length, length))
#     zero_positions = np.where(initial_state == 0)
#     for i in range(len(zero_positions[0])):
#         x = zero_positions[0][i]
#         y = zero_positions[1][i]
#         initial_state[x][y] = -1
#     return initial_state


def initialise_random_state(length):
    initial_state = random.choice((-1, 1), size=(length, length))
    return initial_state
