# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Wed Mar  1 15:14:56 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
from monte_carlo_loop import find_state_progression
from initialise_model import initialise_ones_state, initialise_random_state
# from monte_carlo_modules.print_formats import pvar
from colorama import Style, Fore


LENGTH = 32
J_CONST = 1
TEMP = 1.75
NUMBER_OF_ITERATIONS = LENGTH**2
NUMBER_OF_MC_LOOPS = 1000


def get_save_confirmation():
    while True:
        user_input = input("Would you like to save this plot? [y/n]: ")
        if user_input == "y":
            return True
        if user_input == "n":
            return False
        print(Style.BRIGHT + Fore.RED + "Please input y or n (or Ctrl+c to exit).")
        print(Style.RESET_ALL)


def get_high_or_low_expected_temperature():
    while True:
        user_input = input("Do you expect this temperature to be high or low? [high/low]: ")
        if user_input == "high":
            return True
        if user_input == "low":
            return False
        print(Style.BRIGHT + Fore.RED + "Please input high or low (or Ctrl+c to exit).")
        print(Style.RESET_ALL)


def plot_magnetisation_high_temp(loop_number, magnetisation, title, temperature, save, length=LENGTH):
    fig, ax = plt.subplots()
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    ax.plot(loop_number, magnetisation, color='red')
    ax.set_ylim(-1.05,1.05)
    ax.set_xlabel("MC loop")
    ax.set_ylabel("Magnetisation")
    ax.set_title("{} initialisation: {}, T = {} | {}".format(title, length, temperature, time_str))
    if save:
        plt.savefig("{}_initialisation_{}".format(title, length), dpi=600)
    plt.show()
    plt.close()

def plot_magnetisation_low_temp(loop_number, magnetisation, title, temperature, save, length=LENGTH):
    absolute_magnetisation = np.abs(magnetisation)
    fig, ax = plt.subplots()
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    ax.plot(loop_number, absolute_magnetisation, color='blue')
    ax.set_ylim(-0.05,1.05)
    ax.set_xlabel("MC loop")
    ax.set_ylabel("Magnetisation")
    ax.set_title("{} initialisation: {}, T = {} | {}".format(title, length, temperature, time_str))
    if save:
        plt.savefig("{}_initialisation_{}".format(title, length), dpi=600)
    plt.show()
    plt.close()


def main():
    
    save = get_save_confirmation()
    high_temp = get_high_or_low_expected_temperature()

    loop_range = range(1, NUMBER_OF_MC_LOOPS+1, 1)
    
    initial_state_random = initialise_random_state(LENGTH)
    new_state_random, energies_random, magnetisations_random =  find_state_progression(initial_state_random, TEMP, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
    normalised_magnetisation_random = magnetisations_random / NUMBER_OF_ITERATIONS
    
    initial_state_ones = initialise_ones_state(LENGTH)
    new_state_ones, energies_ones, magnetisations_ones = find_state_progression(initial_state_ones, TEMP, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
    normalised_magnetisation_ones = magnetisations_ones / NUMBER_OF_ITERATIONS
    
    if high_temp:
        plot_magnetisation_high_temp(loop_range, normalised_magnetisation_random, "Random", TEMP, save)
        plot_magnetisation_high_temp(loop_range, normalised_magnetisation_ones, "Ones", TEMP, save)
        return
    
    plot_magnetisation_low_temp(loop_range, normalised_magnetisation_random, "Random", TEMP, save)
    plot_magnetisation_low_temp(loop_range, normalised_magnetisation_ones, "Ones", TEMP, save)

    return 0


if __name__ == "__main__":
    main()





