# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:49:30 2023

@author: lewis
"""
import re
import numpy as np
from print_formats import pvar #noqa
import time as tm #noqa


WOLFF_DIRECTORY = "Monte_carlo_wolff_data/"
WOLFF_CUMULANT_DIRECTORY = "Wolff_cumulant_data/"
WORKING_DIRECTORY = WOLFF_CUMULANT_DIRECTORY


def identify_file_labels(data_filename):
    labels = re.findall("[^_]*", data_filename)
    length = re.findall("\d+", data_filename)[0]
    MC_steps = labels[6]
    run_time = labels[-4]
    
    return length, MC_steps, run_time


def split_energy_data(length, mc_steps, run_time,
                      directory=WORKING_DIRECTORY):
    filename = "Energy_{0}x{0}_MC_{1}_wolff_{2}_Seconds".format(
        length, mc_steps, run_time)
    
    energy_data = (np.genfromtxt(directory + filename,
                                 delimiter=",", skip_header=1))
    
    temperature = energy_data[:, 0]
    energy = energy_data[:, 1]
    energy_squared = energy_data[:, 2]
    
    return temperature, energy, energy_squared


def split_magnetisation_data(length, mc_steps, run_time,
                             directory=WORKING_DIRECTORY):
    filename = "Magnetisation_{0}x{0}_MC_{1}_wolff_{2}_Seconds".format(
        length, mc_steps, run_time)
    magnetisation_data = (np.genfromtxt(directory + filename,
                                        delimiter=",", skip_header=1))

    temperature = magnetisation_data[:, 0]
    magnetisation = magnetisation_data[:, 1]
    magnetistion_abs = magnetisation_data[:, 2]
    magnetisation_squared = magnetisation_data[:, 3]
    magnetisation_4 = magnetisation_data[:, 4]
    
    return [temperature, magnetisation, magnetistion_abs,
            magnetisation_squared, magnetisation_4]


def find_energy_variance(average_energy, average_energy_squared):

    return (average_energy_squared - average_energy**2)


def find_magnetisation_variance(average_magnetisation,
                                average_magnetisation_squared):
    
    return (average_magnetisation_squared - average_magnetisation**2)


def find_heat_capacity(energy_variance, temperature):
    
    heat_capacity = energy_variance / temperature**2

    return heat_capacity


def find_susceptibility(average_magnetisation, average_magnetisation_squared,
                        temperature):

    susceptibility = (average_magnetisation_squared - average_magnetisation**2) / temperature
    
    return susceptibility


def find_relative_permeability(susceptibility):

    return 1/(1-susceptibility)


def find_curie_temperature_cumulant(average_magnetisation_squared,
                                    average_magnetisation_4):
    
    cumulant = 1 - average_magnetisation_4 / (3*average_magnetisation_squared**2)
    return cumulant


def calculate_energy_properties(energy_filename):
    length, MC_steps, run_time = identify_file_labels(energy_filename)
    
    temperature, energy, energy_squared = split_energy_data(length,
                                                            MC_steps,
                                                            run_time)
    energy_variance = find_energy_variance(energy,
                                           energy_squared)
    
    heat_capacity = find_heat_capacity(energy_variance, temperature)
    
    return [length, temperature, energy, energy_variance, heat_capacity]


def calculate_magnetic_properties(magnetisation_filename):
    length, MC_steps, run_time = identify_file_labels(magnetisation_filename)
        
    (temperature, magnetisation, magnetisation_abs, magnetisation_squared,
     magnetisation_4) = split_magnetisation_data(length, MC_steps,
                                                 run_time)
    
    magnetisation_variance = find_magnetisation_variance(magnetisation,
                                                         magnetisation_squared)
    
    susceptibility = find_susceptibility(magnetisation, magnetisation_squared,
                                         temperature)
    susceptibility_abs = find_susceptibility(magnetisation_abs,
                                             magnetisation_squared,
                                             temperature)
    
    cumulant = find_curie_temperature_cumulant(magnetisation_squared,
                                               magnetisation_4)
    
    return [length, temperature, magnetisation, magnetisation_abs,
            magnetisation_variance, susceptibility, susceptibility_abs,
            cumulant]

