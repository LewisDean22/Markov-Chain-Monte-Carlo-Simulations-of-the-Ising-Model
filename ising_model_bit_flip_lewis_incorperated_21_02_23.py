# -*- coding: utf-8 -*-
"""
Title: Ising Model Bit Flip
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Tue Feb 21 16:58:51 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from numpy import random
from print_formats import pvar
import copy
import matplotlib.pyplot as plt
from matplotlib import colors


def initialise_ones_state(length):
    """
    Generates an array of ones dimensions length x length.

    Parameters
    ----------
    length : integer

    Returns
    -------
    initial_state : numpy array of integers (ones)

    """
    initial_state = np.ones((length, length))
    return initial_state


def initialise_random_state(length):
    initial_state = random.randint(0, 2, size=(length, length))
    zero_positions = np.where(initial_state == 0)
    for i in range(len(zero_positions[0])):
        x = zero_positions[0][i]
        y = zero_positions[1][i]
        initial_state[x][y] = -1
    return initial_state


def flip_spin(spin):
    return -spin


def generate_torus(J, spins_state, length):  ##  Maybe look for modulo for larger lengths.  ## Length input unnecessary as inputing array?
    spins_state_torus = np.zeros((length+2, length+2))
    for i in range(length):
        for j in range(length):
            spins_state_torus[i+1, j+1] = spins_state[i,j]
    spins_state_torus[0, 1:-1] = spins_state[-1, :]  ## changed this from spins_state[2, :] to spins_state[-1, :] to generalise for length
    spins_state_torus[1:-1, 0] = spins_state[:, -1]  ## "
    spins_state_torus[1:-1, -1] = spins_state[:, 0]
    spins_state_torus[-1, 1:-1] = spins_state[0, :]
    return spins_state_torus


def calculate_hamiltonian(J, spin_coordinate, spins_state_torus):
    i = spin_coordinate[0] + 1  ## Going to give wrong coordinates in newly sized array?  ## Have added one to fix.
    j = spin_coordinate[1] + 1  ## "
    hamiltonian_sum = (spins_state_torus[i,j] * (spins_state_torus[i, j+1]
                                                 + spins_state_torus[i+1, j]
                                                 + spins_state_torus[i, j-1]
                                                 + spins_state_torus[i-1, j]))
    energy = -J * hamiltonian_sum
    return energy


def calculate_dE_of_spin(J, spin_coordinate, spins_state, spin, length):
    original_state_torus = generate_torus(J, spins_state, length)
    # pvar(original_state_torus)
    updated_state = copy.deepcopy(spins_state)
    flipped = flip_spin(spin)
    # pvar(flipped)
    updated_state[spin_coordinate] = flipped
    # pvar(updated_state)  ## Generate torus is getting rid of flipped bit value. Maybe saving to same place as original state.
                         ## Check toruses with multiple -ves.
    updated_state_torus = generate_torus(J, updated_state, length)
    # pvar(updated_state_torus)
    
    original_energy = calculate_hamiltonian(J, spin_coordinate, original_state_torus)
    # pvar(original_energy)  ## -4 for all energy  ## Should be +ve for original energy??
    updated_energy = calculate_hamiltonian(J, spin_coordinate, updated_state_torus)
    # pvar(updated_energy)  ## -4 for all energy
    dE = updated_energy - original_energy  ## All greater than zero for this initialised state so i guess thermal will flip some randomly.
    return dE


# def find_dE_of_spin(spin_coordinate, spins_state, inputs):
#     ## Code to determine probability of flip dependent on which spin
#     ## and other inputs.
#     ## Spin comes in as (x,y) coord so identifying spin with macro_state[x,y]
#     probability_of_flip = random.randint(0,2)
#     return probability_of_flip


def choose_spins_to_flip(length, number_of_iterations):
    """
    Generates a random set of coordinates in the array.

    Parameters
    ----------
    length : integer
    number_of_iterations : integer

    Returns
    -------
    spins_to_flip : numpy array of integers with dimensions number_of_iterations x 2.
    
    """
    spins_to_flip = random.randint(length, size=(number_of_iterations, 2))
    return spins_to_flip


def decide_to_flip_spin(J, spin_coordinate, spins_state, spin, length):
    dE_of_spin = calculate_dE_of_spin(J, spin_coordinate, spins_state, spin, length)
    pvar(dE_of_spin)  ## with random input seems to be +/- 8, +/- 4, +/- 2.0 or +/- 0, does this make sense? ## Now not seeing any minuses other than -0.0
    # dE_of_spin = 0
    if dE_of_spin <= 0:
        print('FLIP {}'.format(spin_coordinate))
        return True
    # if (logic_for_heat_transfer_prob):  ## Add logic for rand. no. >= exp(dE/kT)
    #     return True
    return False


def find_new_state(J, spins_state, length, number_of_iterations):
    spins_to_flip = choose_spins_to_flip(length, number_of_iterations)
    # pvar(spins_to_flip)
    new_state = np.copy(spins_state)
    for count, spin_position in enumerate(spins_to_flip):
        spin_coordinate = (spin_position[0], spin_position[1])
        spin = spins_state[spin_coordinate]
        spin_should_flip = decide_to_flip_spin(J, spin_coordinate, spins_state, spin, length)
        if spin_should_flip:
            new_state[spin_coordinate] = flip_spin(spin)
    return new_state


def plot_state(state, label):    
    # create discrete colormap
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [-1,1,10]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    fig, ax = plt.subplots()
    ax.imshow(state, cmap=cmap, norm=norm)
    ax.set_title('Iteration {}'.format(label))
    
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, len(state), 1));
    ax.set_yticks(np.arange(-0.5, len(state), 1));
    
    plt.show()


def main():
    length = 5
    number_of_iterations = 10
    J = 1
    initial_state = initialise_ones_state(length)
    # initial_state = random.randint(0, 2, size=(length, length))
    # print(initial_state)
    zero_positions = np.where(initial_state == 0)
    # for i in range(len(zero_positions[0])):
    #     x = zero_positions[0][i]
    #     y = zero_positions[1][i]
    #     initial_state[x][y] = -1
    # pvar(zero_positions)
    # print(initial_state)
    # plot_state(initial_state)
    
    new_state = find_new_state(J, initial_state, length, number_of_iterations)
    print(new_state)
    # plot_state(new_state)
    
    # new_state_1 = find_new_state(J, new_state, length, number_of_iterations)
    # print(new_state_1)
    # plot_state(new_state_1)
    
    # new_state_2 = find_new_state(J, new_state_1, length, number_of_iterations)
    # print(new_state_2)
    # plot_state(new_state_2)
        

    
    # num_minus_ones = len(np.where(new_state == -1.)[0])
    # pvar(num_minus_ones)
    # print('\n\n')
    # x = np.array(range(25)).reshape((5,5))
    # pvar(x)
    # x_torus = generate_torus(0, x, 5)
    # print(x_torus)
        


if __name__ == "__main__":
    main()
            
            
        
        
        
        
        
    
    