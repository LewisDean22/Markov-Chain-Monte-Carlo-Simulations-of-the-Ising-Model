# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Sat Mar  4 16:45:37 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
from new_state_generation import calculate_dE_of_spin, choose_spins_to_flip
from observables import calculate_state_energy, calculate_state_magnetisation
from numpy import random
from show_state import plot_state #noqa
from print_formats import pvar #noqa
from colorama import Style, Fore #noqa


def identify_neighbours(spin_coordinate, length):
    i = spin_coordinate[0]
    j = spin_coordinate[1]
    
    left = (i - 1) % length
    right = (i + 1) % length
    up = (j - 1) % length
    down = (j + 1) % length
    return {(left, j), (right, j), (i, up), (i, down)}


def decide_to_flip_spin(spin_coordinate, spin_coordinate_neighbour, spins_state, J, probability_of_no_flip):
    spin = spins_state[spin_coordinate[0], spin_coordinate[1]]
    spin_neighbour = spins_state[spin_coordinate_neighbour[0], spin_coordinate_neighbour[1]]
    if spin != spin_neighbour:
        return False
    random_number = random.rand()
    if random_number < probability_of_no_flip:
        return True
    return False


def branch_cluster_from_point(spin_coordinate, spins_state, cluster_coordinates, J, probability_of_no_flip):
    neighbours = identify_neighbours(spin_coordinate, len(spins_state))
    possible_coordinates = neighbours - cluster_coordinates
    new_cluster_coordinates = set()
    for coordinate in possible_coordinates:
        flip_spin = decide_to_flip_spin(spin_coordinate, coordinate, spins_state, J, probability_of_no_flip)
        if flip_spin:
            new_cluster_coordinates.add(coordinate)
    return new_cluster_coordinates


def flip_cluster(spins_state, cluster_coordinates):
    new_state = np.copy(spins_state)
    for coordinate in cluster_coordinates:
        new_state[coordinate] *= -1
    return new_state


def find_new_state_from_cluster_point(spins_state, spin_coordinate, J, T):
    probability_of_no_flip = 1 - np.exp(-2 / T)
    cluster_coordinates = {spin_coordinate}
    tested_coordinates = set()
    coordinates_to_test = cluster_coordinates - tested_coordinates
    # count = 0
    while coordinates_to_test:
        for spin_coordinate in coordinates_to_test:
            new_cluster_coordinates = branch_cluster_from_point(spin_coordinate, spins_state, cluster_coordinates, J, probability_of_no_flip)
            cluster_coordinates = cluster_coordinates.union(new_cluster_coordinates)
            tested_coordinates.add(spin_coordinate)
        coordinates_to_test = cluster_coordinates - tested_coordinates
        
        new_state = flip_cluster(spins_state, cluster_coordinates)
        
        # plot_state(new_state, 'flipped') #cluster forming
        # count += 1
    
    # print("Cluster size: {}".format(len(cluster_coordinates)))
    #plot_state(new_state, 'New state') #whole cluster
    
    return new_state


def find_cluster_progression(state, temperature, length, number_of_iterations,
                             J):
    # plot_state(initial_state, "initial")
    spin_positions = choose_spins_to_flip(length, number_of_iterations)
    new_state = state
    energies = np.zeros(number_of_iterations)
    magnetisations = np.zeros(number_of_iterations)
    
    for count, spin_position in enumerate(spin_positions):

        spin_coordinate = (spin_position[0], spin_position[1])
        new_state = find_new_state_from_cluster_point(new_state, spin_coordinate, J, temperature)
        
        # print(Style.BRIGHT + Fore.RED + 'Iteration: {}'.format(count))
        # print(Style.BRIGHT + Fore.RED + 'Temperature: {}'.format(temperature))        
        # print(Style.RESET_ALL)
        # plot_state(new_state, count)
        # print('\n')
        
        state_energy = calculate_state_energy(J, new_state)
        energies[count] = state_energy
        
        state_magnetisation = calculate_state_magnetisation(new_state)
        magnetisations[count] = state_magnetisation
    
    return new_state, energies, magnetisations


