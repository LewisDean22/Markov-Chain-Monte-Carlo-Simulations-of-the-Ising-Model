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
from wolff_algorithm import find_new_state_from_cluster_point
from new_state_generation import choose_spins_to_flip
from initialise_model import initialise_ones_state, initialise_random_state
from colorama import Style, Fore
from print_formats import pvar
from show_state import plot_state


LENGTH = 25
J_CONST = 1
TEMP = 2.5
NUMBER_OF_ITERATIONS = 500


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
                           "\n(If unsure enter high)"
                           "\n[high/low]: ")
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
    ax.set_xlabel("Cluster Number")
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
    ax.set_xlabel("Cluster Number")
    ax.set_ylabel("Magnetisation")
    ax.set_title("{} initialisation: {}, T = {} | {}".format(title, length, temperature, time_str))
    if save:
        plt.savefig("{}_initialisation_{}".format(title, length), dpi=600)
    plt.show()
    plt.close()


# def plot_magnetisation_real_time_high_temp(loop_number, magnetisation, title, temperature, save, length=LENGTH):
#     fig, ax = plt.subplots()

#     # animated=True tells matplotlib to only draw the artist when we
#     # explicitly request it
#     (ln,) = ax.plot(loop_number, magnetisation, animated=True)
    
#     # make sure the window is raised, but the script keeps going
#     plt.show(block=False)
    
#     # stop to admire our empty window axes and ensure it is rendered at
#     # least once.
#     #
#     # We need to fully draw the figure at its final size on the screen
#     # before we continue on so that :
#     #  a) we have the correctly sized and drawn background to grab
#     #  b) we have a cached renderer so that ``ax.draw_artist`` works
#     # so we spin the event loop to let the backend process any pending operations
#     plt.pause(0.1)
    
#     # get copy of entire figure (everything inside fig.bbox) sans animated artist
#     bg = fig.canvas.copy_from_bbox(fig.bbox)
#     # draw the animated artist, this uses a cached renderer
#     ax.draw_artist(ln)
#     # show the result to the screen, this pushes the updated RGBA buffer from the
#     # renderer to the GUI framework so you can see it
#     fig.canvas.blit(fig.bbox)
    
#     for j in range(100):
#         # reset the background back in the canvas state, screen unchanged
#         fig.canvas.restore_region(bg)
#         # update the artist, neither the canvas state nor the screen have changed
#         ln.set_ydata(np.sin(x + (j / 100) * np.pi))
#         # re-render the artist, updating the canvas state, but not the screen
#         ax.draw_artist(ln)
#         # copy the image to the GUI state, but screen might not be changed yet
#         fig.canvas.blit(fig.bbox)
#         # flush any pending GUI events, re-painting the screen if needed
#         fig.canvas.flush_events()
#         # you can put a pause in if you want to slow things down
        # plt.pause(.1)


def main():
    
    save = get_save_confirmation()
    high_temp = get_high_or_low_expected_temperature()

    loop_range = range(1, NUMBER_OF_ITERATIONS+1, 1)
    coordinates_to_flip = choose_spins_to_flip(LENGTH, NUMBER_OF_ITERATIONS)
    # print(coordinates_to_flip)
    
    initial_state_random = initialise_random_state(LENGTH)
    new_state_random = initial_state_random
    # loop_range = []
    normalised_magnetisation_random_list = []
    # initial_state_ones = initialise_ones_state(LENGTH)
    
    
    #####################################################
        
    # fig, ax = plt.subplots()

    # # animated=True tells matplotlib to only draw the artist when we
    # # explicitly request it
    # (ln,) = ax.plot(loop_range, normalised_magnetisation_random_list, animated=True)
    
    # # make sure the window is raised, but the script keeps going
    # plt.show(block=False)
    
    # # stop to admire our empty window axes and ensure it is rendered at
    # # least once.
    # #
    # # We need to fully draw the figure at its final size on the screen
    # # before we continue on so that :
    # #  a) we have the correctly sized and drawn background to grab
    # #  b) we have a cached renderer so that ``ax.draw_artist`` works
    # # so we spin the event loop to let the backend process any pending operations
    # plt.pause(0.1)
    
    # # get copy of entire figure (everything inside fig.bbox) sans animated artist
    # bg = fig.canvas.copy_from_bbox(fig.bbox)
    # # draw the animated artist, this uses a cached renderer
    # ax.draw_artist(ln)
    # # show the result to the screen, this pushes the updated RGBA buffer from the
    # # renderer to the GUI framework so you can see it
    # fig.canvas.blit(fig.bbox)
    
    ##################################################
    
    
    for count, spin_position in enumerate(coordinates_to_flip):
        
        
        #######################################################
        
        # fig.canvas.restore_region(bg)
        
        #######################################################
        
        
        coordinate = (spin_position[0], spin_position[1])
        new_state_random = find_new_state_from_cluster_point(new_state_random, coordinate, J_CONST, TEMP)
        # plot_state(new_state_random, 'random {}'.format(count))

        magnetisations_random = np.sum(new_state_random)
        normalised_magnetisation_random = magnetisations_random / LENGTH**2
        # loop_range += [count]
        # ln.set_ydata(normalised_magnetisation_random)
        normalised_magnetisation_random_list += [normalised_magnetisation_random]
        # plot_state(new_state_random, "random | T = {}".format(TEMP))
        print(Style.BRIGHT + Fore.RED + "RANDOM: {}".format(count))
        print(Style.RESET_ALL)
        
        
        #######################################################
        
        # ax.draw_artist(ln)
        # # copy the image to the GUI state, but screen might not be changed yet
        # fig.canvas.blit(fig.bbox)
        # # flush any pending GUI events, re-painting the screen if needed
        # fig.canvas.flush_events()
        # # you can put a pause in if you want to slow things down
        # # plt.pause(.1)

    

    initial_state_ones = initialise_ones_state(LENGTH)
    new_state_ones = initial_state_ones
    normalised_magnetisation_ones_list = []
    for count, spin_position in enumerate(coordinates_to_flip):
        coordinate = (spin_position[0], spin_position[1])
        new_state_ones = find_new_state_from_cluster_point(new_state_ones, coordinate, J_CONST, TEMP)
        magnetisations_ones = np.sum(new_state_ones)
        normalised_magnetisation_ones = magnetisations_ones / LENGTH**2
        normalised_magnetisation_ones_list += [normalised_magnetisation_ones]
        print(Style.BRIGHT + Fore.RED + "ONES: {}".format(count))
        print(Style.RESET_ALL)
    
    # new_state_ones, energies_ones, magnetisations_ones = find_new_state_from_cluster_point(initial_state_ones, TEMP, J_CONST, LENGTH, NUMBER_OF_ITERATIONS, NUMBER_OF_MC_LOOPS)
    # normalised_magnetisation_ones = magnetisations_ones / NUMBER_OF_ITERATIONS
    
    if high_temp:
        plot_magnetisation_high_temp(loop_range, normalised_magnetisation_random_list, "Random", TEMP, save)
        plot_magnetisation_high_temp(loop_range, normalised_magnetisation_ones_list, "Ones", TEMP, save)
        plot_state(new_state_random, "random | T = {}".format(TEMP))
        pvar(normalised_magnetisation_random_list)
        # pvar(normalised_magnetisation_ones_list)
        # plot_state
        return
    
    plot_magnetisation_low_temp(loop_range, normalised_magnetisation_random_list, "Random", TEMP, save)
    # plot_magnetisation_low_temp(loop_range, normalised_magnetisation_ones_list, "Ones", TEMP, save)

    plot_state(new_state_random, "random | T = {}".format(TEMP))

    pvar(normalised_magnetisation_random_list)
    # pvar(normalised_magnetisation_ones_list)

    return 0


if __name__ == "__main__":
    main()
