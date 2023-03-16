# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:49:30 2023

Curie temp is broken at the moment as it should be single-valued, not an array.

@author: lewis
"""
import re
import numpy as np
from print_formats import pvar #noqa
import time as tm #noqa

METROPOLIS_DIRECTORY = "Monte_carlo_metropolis_data/"
WOLFF_DIRECTORY = "Monte_carlo_wolff_data/"
WORKING_DIRECTORY = WOLFF_DIRECTORY


def identify_file_labels(data_filename):
    labels = re.findall("[^_]*", data_filename)
    length = re.findall("\d+", data_filename)[0]
    MC_steps = labels[-4]
    
    return length, MC_steps


def split_energy_data(length, mc_steps, directory=WORKING_DIRECTORY):
    filename = "Energy_{0}x{0}_MC_{1}_{2}".format(length, mc_steps,
                                                 ('metropolis' if directory==METROPOLIS_DIRECTORY
                                                  else 'wolff.csv'))
    
    energy_data = (np.genfromtxt(directory + filename,
                                 delimiter=",", skip_header=1))
    
    temperature = energy_data[:, 0]
    energy = energy_data[:, 1]
    energy_squared = energy_data[:, 2]
    
    return temperature, energy, energy_squared


def split_magnetisation_data(length, mc_steps,
                             directory=WORKING_DIRECTORY):
    filename = "Magnetisation_{0}x{0}_MC_{1}_{2}".format(length, mc_steps,
                                                         ('metropolis' if WORKING_DIRECTORY==METROPOLIS_DIRECTORY
                                                         else 'wolff.csv'))
    magnetisation_data = (np.genfromtxt(directory + filename,
                                        delimiter=",", skip_header=1))

    temperature = magnetisation_data[:, 0]
    magnetisation = magnetisation_data[:, 1]
    magnetistion_abs = magnetisation_data[:, 2]
    magnetisation_squared = magnetisation_data[:, 3]
    magnetisation_4 = magnetisation_data[:, 4]
    
    return [temperature, magnetisation, magnetistion_abs,
            magnetisation_squared, magnetisation_4]


def find_heat_capacity(average_energy, average_energy_squared, temperature,
                       length):
    total_spins = int(length)**2
    heat_capacity = (average_energy_squared - total_spins*average_energy**2) / temperature**2

    return heat_capacity


def find_susceptibility(average_magnetisation, average_magnetisation_squared,
                        temperature, length):
    total_spins = int(length)**2
    susceptibility = (average_magnetisation_squared - total_spins*average_magnetisation**2) / temperature
    return susceptibility


def find_relative_permeability(susceptibility):

    return 1/(1-susceptibility)


def find_curie_temperature(average_magnetisation_squared,
                           average_magnetisation_4):
    '''
    Look up how cumulants work

    '''
    
    curie_temp = 1 - average_magnetisation_4 / (3*average_magnetisation_squared)
    return curie_temp


def calculate_energy_properties(energy_filename):
    length, MC_steps = identify_file_labels(energy_filename)
    
    temperature, energy, energy_squared = split_energy_data(length,
                                                            MC_steps)
    heat_capacity = find_heat_capacity(energy, energy_squared,
                                       temperature, length)
    
    return [length, temperature, energy, heat_capacity]


def calculate_magnetic_properties(magnetisation_filename):
    length, MC_steps = identify_file_labels(magnetisation_filename)
        
    (temperature, magnetisation, magnetisation_abs, magnetisation_squared,
     magnetisation_4) = split_magnetisation_data(length, MC_steps)
    
    susceptibility = find_susceptibility(magnetisation, magnetisation_squared,
                                         temperature, length)
    
    curie_temp = find_curie_temperature(magnetisation_squared,
                                         magnetisation_4)
    
    return [length, temperature, magnetisation, magnetisation_abs,
            susceptibility, curie_temp]

