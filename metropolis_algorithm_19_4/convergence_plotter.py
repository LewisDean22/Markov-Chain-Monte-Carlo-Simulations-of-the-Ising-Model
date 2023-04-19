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


LENGTH = 2
J_CONST = 1
TEMP = 1.7
NUMBER_OF_ITERATIONS = LENGTH**2
NUMBER_OF_MC_LOOPS = 10000


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
        user_input = input("Do you expect this temperature to be high or low?"
                           "\n(low temp gives absolute magnetisation)"
                           "\n[high/low]: ")
        if user_input == "high":
            return True
        if user_input == "low":
            return False
        print(Style.BRIGHT + Fore.RED + "Please input high or low (or Ctrl+c to exit).")
        print(Style.RESET_ALL)
    

def plot_magnetisation(loop_number, magnetisation, title, temperature,
                        save, high_temp, length=LENGTH):
    fig, ax = plt.subplots()
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    ax.set_xlabel("MC loop")
    ax.set_ylabel("Magnetisation")
    ax.set_title("{} initialisation: {}, T = {} | {}".format(title, length,
                                                             temperature, time_str))
    
    if high_temp:
        ax.plot(loop_number, magnetisation, color='red', marker = 'x')
        ax.set_ylim(-1.05,1.05)
        if save:
            plt.savefig("convergence_plots/High_temp_magnetisation_{}_initialisation_{}".format(title, length), dpi=600)
    else:
        absolute_magnetisation = np.abs(magnetisation)
        ax.plot(loop_number, absolute_magnetisation, color='blue')
        ax.set_ylim(-0.05,1.05)
        if save:
            plt.savefig("convergence_plots/Low_temp_magnetisation_{}_initialisation_{}".format(title, length), dpi=600)

    plt.show()
    # plt.close()
    

def plot_energy(loop_number, energy, title, temperature,
                        save, high_temp, length=LENGTH):
    fig, ax = plt.subplots()
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    ax.set_xlabel("MC loop")
    ax.set_ylabel("Energy")
    ax.set_title("{} initialisation: {}, T = {} | {}".format(title, length,
                                                             temperature, time_str))
    
    ax.plot(loop_number, energy, color='green')
    ax.set_ylim(-1.05,1.05)
    if save:
        plt.savefig("convergence_plots/Energy_{}_initialisation_{}".format(title, length),
                    dpi=600)

    plt.show()
    plt.close()


def main():
    
    save = get_save_confirmation()
    high_temp = get_high_or_low_expected_temperature()

    loop_range = range(1, NUMBER_OF_MC_LOOPS+1, 1)
    
    initial_state_random = initialise_random_state(LENGTH)
    new_state_random, energies_random, magnetisations_random =  find_state_progression(initial_state_random, TEMP, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
    normalised_magnetisation_random = magnetisations_random / NUMBER_OF_ITERATIONS
    normalised_energy_random = energies_random / NUMBER_OF_ITERATIONS
    
    initial_state_ones = initialise_ones_state(LENGTH)
    new_state_ones, energies_ones, magnetisations_ones = find_state_progression(initial_state_ones, TEMP, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
    normalised_magnetisation_ones = magnetisations_ones / NUMBER_OF_ITERATIONS
    normalised_energy_ones = energies_ones / NUMBER_OF_ITERATIONS
    
    
    plot_magnetisation(loop_range, normalised_magnetisation_random, "random",
                        TEMP, save, high_temp)
    plot_magnetisation(loop_range, normalised_magnetisation_ones, "ones",
                        TEMP, save, high_temp)
    # plot_energy(loop_range, normalised_energy_random, "random",
    #                     TEMP, save, high_temp)
    # plot_energy(loop_range, normalised_energy_ones, "ones",
    #                     TEMP, save, high_temp)
    
    
    return None


if __name__ == "__main__":
    main()