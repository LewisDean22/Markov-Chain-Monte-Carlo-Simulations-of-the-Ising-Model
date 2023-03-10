# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:49:30 2023

@author: lewis
Magnetisation per spin to make comparisons between different lattice sizes
more apparent. Hence the norm dividing by total spin too.
"""
import re
import numpy as np
from print_formats import pvar
import matplotlib.pyplot as plt

DIRECTORY = "Monte_carlo_data/"
MC_STEPS = 10_000


def norm_constant(lattice_size, mc_loops=MC_STEPS):
    '''
    Turns observable data for a given temperature into an ensemble average
    of that observable for the inputted lattice size.

    '''
    return 1 / (mc_loops) # I believe the number of spins
    # should get involved later so only dividing by MC loops now.


def split_data(observable_type, latice_size):
    filename = observable_type + "_{0}x{0}".format(latice_size)
    observables_data = (np.genfromtxt(DIRECTORY + filename, delimiter=","))

    temperature = observables_data[:, 0]
    observable = observables_data[:, 1]
    return temperature, observable


def normalise_observable(observable, norm):

    return observable * norm


def find_heat_capacity(energy, temperature, norm, lattice_size):
    '''
    No extra n in heat capacity calc at the moment
    '''
    n = int(lattice_size)**2
    average_energy = normalise_observable(energy, norm)
    average_energy_squared = normalise_observable(energy**2, norm)
    heat_capacity = (average_energy_squared - (average_energy**2)) / (temperature)**2
    return heat_capacity


def find_susceptibility(magnetisation, temperature, norm):
    '''
    No extra n in calc at the moment
    '''
    average_magnetisation_squared = normalise_observable(magnetisation**2,
                                                         norm)
    average_magnetisation = normalise_observable(magnetisation, norm)
    susceptibility = (average_magnetisation_squared - average_magnetisation**2) / temperature
    return susceptibility


def find_relative_permeability(susceptibility):

    return 1/(1-susceptibility)


def calculate_properties(data_filename):

    lattice_size = re.findall("\d", data_filename)[0]
    observable_type = re.findall("[^_]*", data_filename)[0].lower()
    norm = norm_constant(int(lattice_size))
    total_spins = int(lattice_size)**2

    temperature, observable = split_data(observable_type, lattice_size)
    
    plt.plot(temperature, normalise_observable(observable, norm)/total_spins)
    if observable_type == 'energy':
        plt.title('E(T) per spin')
        plt.show()
    if observable_type == 'magnetisation':
        plt.title('M(T) per spin')
        plt.show()
        plt.plot(temperature, abs(normalise_observable(observable, norm)/total_spins))
        plt.title(r'$\mid$M(T)$\mid$ per spin')
        plt.show()
        

    if observable_type == 'energy':
        heat_capacity = find_heat_capacity(observable, temperature, norm, lattice_size)
        return observable_type, lattice_size, temperature, heat_capacity
    if observable_type == 'magnetisation':
        susceptibility = find_susceptibility(observable, temperature, norm)
        return observable_type, lattice_size, temperature, susceptibility

