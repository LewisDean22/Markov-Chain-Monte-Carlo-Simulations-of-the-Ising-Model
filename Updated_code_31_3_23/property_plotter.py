# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:00:38 2023

How is the early 'per spin' gonna effect avd(M^4) ???

Update pvar to give object type too

@author: lewis
"""
import matplotlib.pyplot as plt
import numpy as np  # noqa
from property_calculator import *  # noqa
import os
from print_formats import pvar  # noqa

import pandas as pd

SAVE_ALL = 1
SAVE_SEPERATE = 1
XLIM_MAX = 5
LINESTYLE = ('solid', 'dotted', 'dashed', 'dashdot', (0, (1, 1)))

METROPOLIS_DIRECTORY = "Monte_carlo_metropolis_data/"
WOLFF_DIRECTORY = "Monte_carlo_wolff_data/"
WORKING_DIRECTORY = METROPOLIS_DIRECTORY

CUMULANT_TOLERANCE = 10**-4


def get_user_input(question):
    while True:
        response = input(question + ' (y/n) ')
        if response == 'y':
            return True
        elif response == 'n':
            return False
        print('Please enter a valid response (y/n) ')


def file_finder(directory):

    energy_data = []
    magnetisation_data = []
    for file in os.listdir(directory):
        if file.startswith("Energy"):
            energy_data.append(file)
        if file.startswith("Magnetisation"):
            magnetisation_data.append(file)

    return energy_data, magnetisation_data


def plot_energy(length, temperature_data, energy_plot_data,
                save_seperate=SAVE_SEPERATE):

    plt.plot(temperature_data, energy_plot_data,
             label='{0}x{0}'.format(length))
    plt.xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    plt.ylabel(r'$\langle$ Energy $/rangle$')
    plt.title('E(T) per spin')
    plt.legend()

    if save_seperate:
        plt.savefig("property_plots/energy_plot_{0}x{0}".format(length),
                    dpi=600)

    plt.show()
    plt.close()


def plot_magnetisation(length, temperature_data, magnetisation_plot_data,
                       is_absolute, save_seperate=SAVE_SEPERATE):

    plt.plot(temperature_data, magnetisation_plot_data,
             label='{0}x{0}'.format(length))
    plt.xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    plt.ylabel(r'$\langle$ Magnetisation $\rangle$')
    if is_absolute:
        plt.title('|M(T)| per spin')
    else:
        plt.title('M(T) per spin')
    plt.legend()

    if save_seperate:
        plt.savefig("property_plots/{0}magnetisation_plot_{1}x{1}".format(
            'absolute_' if is_absolute == 1 else '', length),
            dpi=600)

    plt.show()
    plt.close()


def plot_heat_capacity(length, temperature_data, heat_capacity_plot_data,
                       save_seperate=SAVE_SEPERATE):

    fig, ax = plt.subplots()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$C_V$')
    ax.set_title(r'$C_V$ (T) per spin')
    ax.plot(temperature_data, heat_capacity_plot_data,
            label='{0}x{0}'.format(length))
    ax.legend()

    if save_seperate:
        plt.savefig("property_plots/heat_capacity_{0}x{0}".format(length),
                    dpi=600)

    plt.show()
    plt.close()


def plot_susceptibility(length, temperature_data, susceptibility_data,
                        save_seperate=SAVE_SEPERATE):

    fig, ax = plt.subplots()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$\chi$')
    ax.set_title(r'$\chi$ (T) per spin')
    ax.plot(temperature_data, susceptibility_data,
            label='{0}x{0}'.format(length))
    ax.legend()

    if save_seperate:
        plt.savefig("property_plots/susceptibility_{0}x{0}".format(length),
                    dpi=600)

    plt.show()
    plt.close()


def plot_absolute_susceptibility(length, temperature_data,
                                 susceptibility_abs_data,
                                 save_seperate=SAVE_SEPERATE):

    fig, ax = plt.subplots()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r"$\chi$'")
    ax.set_title(r"$\chi$' (T| per spin")
    ax.plot(temperature_data, susceptibility_abs_data,
            label='{0}x{0}'.format(length))
    ax.legend()

    if save_seperate:
        plt.savefig("property_plots/absolute_susceptibility_{0}x{0}".format(length),
                    dpi=600)

    plt.show()
    plt.close()


def plot_all_energies(energy_filenames, save_all=SAVE_ALL,
                      xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in energy_filenames:
        plot_data.append(calculate_energy_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, energy_plot_data, energy_variance_data,
         heat_capacity_plot_data) = data

        ax.plot(temperature_data, energy_plot_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    plt.xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    plt.ylabel(r'$\langle$ Energy $\rangle$')
    plt.title('E(T) per spin')
    plt.legend()

    if save_all:
        plt.savefig("property_plots/all_energies", dpi=600)

    plt.show()
    plt.close()


def plot_all_energy_variances(energy_filenames, save_all=SAVE_ALL,
                              xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in energy_filenames:
        plot_data.append(calculate_energy_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, energy_plot_data, energy_variance_data,
         heat_capacity_plot_data) = data

        ax.plot(temperature_data, energy_variance_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    plt.xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    plt.ylabel('Energy variance')
    plt.title('Var(E) per spin as a function of temperature')
    plt.legend()

    if save_all:
        plt.savefig("property_plots/all_energy_variances", dpi=600)

    plt.show()
    plt.close()


def plot_all_magnetisations(magnetisation_filenames, save_all=SAVE_ALL,
                            xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in magnetisation_filenames:
        plot_data.append(calculate_magnetic_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = data

        ax.plot(temperature_data, magnetisation_plot_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$\langle$ Magnetisation $\rangle$')
    ax.set_title('M(T) per spin')
    plt.legend()

    if save_all:
        plt.savefig("property_plots/all_magnetisations", dpi=600)

    plt.show()
    plt.close()


def plot_all_magnetisation_variances(magnetisation_filenames, save_all=SAVE_ALL,
                                     xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in magnetisation_filenames:
        plot_data.append(calculate_magnetic_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = data

        ax.plot(temperature_data, magnetisation_variance_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel('Magnetisation variance')
    ax.set_title('Var(M) per spin as a function of temperature')
    plt.legend()

    if save_all:
        plt.savefig("property_plots/all_magnetisation_variances", dpi=600)

    plt.show()
    plt.close()


def plot_all_absolute_magnetisations(magnetisation_filenames, save_all=SAVE_ALL,
                                     xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in magnetisation_filenames:
        plot_data.append(calculate_magnetic_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = data

        ax.plot(temperature_data, magnetisation_abs_plot_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$\langle$ Absolute Magnetisation $\rangle$')
    ax.set_title('|M(T)| per spin')
    plt.legend()

    if save_all:
        plt.savefig("property_plots/all_absolute_magnetisations", dpi=600)

    plt.show()
    plt.close()


def plot_all_heat_capacities(energy_filenames, save_all=SAVE_ALL,
                             xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in energy_filenames:
        plot_data.append(calculate_energy_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, energy_plot_data, energy_variance_data,
         heat_capacity_plot_data) = data

        t_c_arg = np.argmax(heat_capacity_plot_data)
        print('Curie temp for {0}x{0} through argmax = '.format(length) + (
            str(temperature_data[t_c_arg])))

        ax.plot(temperature_data, heat_capacity_plot_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.legend()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$C_V$')
    ax.set_title(r'$C_V$ (T) per spin')
    ax.set_xlim(0, xlim_max)

    if save_all:
        plt.savefig("property_plots/all_heat_capacities", dpi=600)

    plt.show()
    plt.close()


def plot_all_susceptibilities(magnetisation_filenames, save_all=SAVE_ALL,
                              xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in magnetisation_filenames:
        plot_data.append(calculate_magnetic_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = data

        ax.plot(temperature_data, susceptibility_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.legend()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r'$\chi$')
    ax.set_title(r'$\chi$ (T) per spin')
    ax.set_xlim(0, xlim_max)

    if save_all:
        plt.savefig("property_plots/all_susceptibilities", dpi=600)

    plt.show()
    plt.close()


def plot_all_absolute_susceptibilities(magnetisation_filenames, save_all=SAVE_ALL,
                                       xlim_max=XLIM_MAX, linestyle=LINESTYLE):
    plot_data = []
    for dataset in magnetisation_filenames:
        plot_data.append(calculate_magnetic_properties(dataset))

    fig, ax = plt.subplots()

    for count, data in enumerate(plot_data):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = data

        ax.plot(temperature_data, susceptibility_abs_data,
                label='{0}x{0}'.format(length),
                linestyle=linestyle[count])

    ax.legend()
    ax.set_xlabel('T (K)')
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.set_ylabel(r"$\chi$'")
    ax.set_title(r"$\chi$' (T) per spin")
    ax.set_xlim(0, xlim_max)

    if save_all:
        plt.savefig("property_plots/all_absolute_susceptibilities", dpi=600)

    plt.show()
    plt.close()


def main(directory=WORKING_DIRECTORY, tolerance=CUMULANT_TOLERANCE):

    plot_seperate = get_user_input('Would you like to create seperate plots?')
    plot_all = get_user_input('Would you like to create joint dataset plots?')

    energy_data_list, magnetisation_data_list = file_finder(directory)
        
    if plot_seperate:
        
        for energy_filename in energy_data_list:
            (length, temperature_data, energy_plot_data, energy_variance_data,
             heat_capacity_data) = (calculate_energy_properties(energy_filename))

            plot_energy(length, temperature_data, energy_plot_data)
            plot_heat_capacity(length, temperature_data,
                           heat_capacity_data)

        for magnetisation_filename in magnetisation_data_list:
            (length, temperature_data, magnetisation_plot_data,
             magnetisation_abs_plot_data, magnetisation_variance_data,
             susceptibility_data, susceptibility_abs_data, cumulant) = (
                 calculate_magnetic_properties(magnetisation_filename))
        
            
            plot_magnetisation(length, temperature_data,
                               magnetisation_plot_data, is_absolute=0)
            plot_magnetisation(length, temperature_data,
                               magnetisation_abs_plot_data, is_absolute=1)
            plot_susceptibility(length, temperature_data,
                                susceptibility_data)
            plot_absolute_susceptibility(length, temperature_data,
                                         susceptibility_abs_data)    

    if plot_all:
        
        plot_all_energies(energy_data_list)
        plot_all_energy_variances(energy_data_list)
        plot_all_heat_capacities(energy_data_list)
        plot_all_magnetisations(magnetisation_data_list)
        plot_all_absolute_magnetisations(magnetisation_data_list)
        plot_all_magnetisation_variances(magnetisation_data_list)
        plot_all_susceptibilities(magnetisation_data_list)
        plot_all_absolute_susceptibilities(magnetisation_data_list)
        
    return None


if __name__ == "__main__":
    main()
