# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:00:38 2023

@author: lewis
"""
import matplotlib.pyplot as plt
import numpy as np
from property_calculator import *
import os
from print_formats import pvar

SAVE_ALL = True
SAVE_SEPERATE = True
XLIM_MAX = 5

DIRECTORY = "Monte_carlo_data/"


def file_finder(directory=DIRECTORY):
    
    energy_data = []
    magnetisation_data = []
    for file in os.listdir(directory):
        if file.startswith("energy"):
            energy_data.append(file)
        if file.startswith("magnetisation"):
            magnetisation_data.append(file)
            
    return energy_data, magnetisation_data

def plot_observable(filename, save_seperate=SAVE_SEPERATE):
    
    observable_type, lattice_size, temperature_data, observable_plot_data = (
        calculate_properties(filename))
    
    fig, ax = plt.subplots()
    ax.plot(temperature_data, observable_plot_data,
            label = '{0}x{0}'.format(lattice_size))
    ax.legend()
    ax.set_xlabel('T (K)')
    
    if observable_type == 'magnetisation':
        ax.set_ylabel(r'$\chi$') 
        ax.set_title(r'$\chi$ (T)')
        if save_seperate:
            plt.savefig("property_plots/susceptibility_{0}x{0}".format(lattice_size),
                        dpi=600)
    if observable_type == 'energy':
        ax.set_ylabel(r'$\langle C_V \rangle$') 
        ax.set_title(r'$\langle C_V \rangle$ (T)')
        if save_seperate:
            plt.savefig("property_plots/heat_capacity_{0}x{0}".format(lattice_size),
                        dpi=600)
    
    plt.show()
    plt.close()


def plot_all_observables(filenames, save_all=SAVE_ALL, xlim_max=XLIM_MAX):
    
    plot_data = []
    for dataset in filenames:
        plot_data.append(calculate_properties(dataset))
        
    fig, ax = plt.subplots()
    for i in range(len(plot_data)):
        observable_type, lattice_size, temperature_data, observable_plot_data = plot_data[i]
        ax.plot(temperature_data, observable_plot_data,
                label = '{0}x{0}'.format(lattice_size))
    
    ax.legend()
    ax.set_xlabel('T (K)')
    ax.set_xlim(0, xlim_max)
    if observable_type == 'magnetisation':
        ax.set_ylabel(r'$\chi$') 
        ax.set_title(r'$\chi$ (T)')
    if observable_type == 'energy':
        ax.set_ylabel(r'$\langle C_V \rangle$') 
        ax.set_title(r'$\langle C_V \rangle$ (T)')
    
    if save_all and (observable_type == 'magnetisation'):
        plt.savefig("property_plots/all_susceptibilities", dpi=600)
    if save_all and (observable_type == 'energy'):
        plt.savefig("property_plots/all_heat_capacities", dpi=600)    
        
    plt.show()
    plt.close()


def main():
    
    energy_data, magnetisation_data = file_finder()
    
    for dataset in energy_data:
        plot_observable(dataset)
    for dataset in magnetisation_data:
        plot_observable(dataset)
        
    plot_all_observables(energy_data)
    plot_all_observables(magnetisation_data)
        
    return None


if __name__ == "__main__":
    main()