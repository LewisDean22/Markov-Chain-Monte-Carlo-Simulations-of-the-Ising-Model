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
    initial_state = np.ones((length, length), dtype=np.int8)
    return initial_state


def initialise_random_state(length):
    initial_state = random.choice((-1, 1), size=(length, length))
    return initial_state
