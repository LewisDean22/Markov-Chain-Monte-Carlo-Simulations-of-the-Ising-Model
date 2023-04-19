# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 00:57:54 2023

Poorly made at the moment so the working directory needs updating both here
and in property calculator when running!!! <---------------------------

At a small temp range (2.22 - 2.28 and 0.001 temp steps) the cumulant plot
fluctuates drastically as opposed to being a smooth function. Therefore, the 
'intersection point' identified is smudged as there are many. Won't necessarily
be solved by a larger lattice size but instead a greater number of MC steps before
averaging. Plus, critical slowing down seems to be less about thermalisation
and more about autocorrelation times. Thus, maybe the number of iterations before
sampling should incease. Or no local update algorithm altogether and instead use
a cluster algortithm like the Wolff algorithm.

Higher MC steps = smoother cumulant plot (more precise by less fluctuation)
Larger lattice size = cumulant intersection method gives a more accurate T_c?
But the curve gets steeper indicating a lower intersection temperature?

Gathering the data for this is now taking a very long time (all 10^6 MC steps
and 7+hours for 25 metropolis 8x8 and 7+hours for 50 metropolis 4x4). Would
benefit from Cython or cache decorators (where could the latter see application?)

NEEDS FIXING TO BE PER SPIN AGAIN I ASSUME??

@author: lewis
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd #noqa
from property_calculator import * #noqa

LINESTYLE = ('solid', 'dotted', 'dashed', 'dashdot', (0, (1, 1)))
METROPOLIS_CUMULANT_DIRECTORY = "Metropolis_cumulant_data/"
WORKING_DIRECTORY = METROPOLIS_CUMULANT_DIRECTORY
# Read the document header if having directory issues!

SAVE = True


def magnetisation_file_finder(directory):
    
    magnetisation_data_list = []
    for file in os.listdir(directory):
        if file.startswith("Magnetisation"):
            magnetisation_data_list.append(file)
    
    return magnetisation_data_list


def file_truncator(data_files):
    '''
    This was made quickly to deal with an error in data files of different
    length. The file truncator works for when there is variation in the minimum
    temperature set in the metropolis main script.
    
    Made to fix the 1_000_000 step (4x4) from the 2.0-2.4 K because the other
    data files have 100_000 steps with temp range 1.9-2.4 K. Having the same
    temp step is essential for the premise of cumulant intersection
    identification.

    '''
    lengths = []
    truncated_files = []
    
    for file in data_files:
        lengths += [len(file)]
    min_length = np.min(lengths)
    for file in data_files:
        truncated_files += [file[:min_length]]
    
    return np.array(truncated_files)
    
    
def main(directory=WORKING_DIRECTORY, linestyle=LINESTYLE,
         save=SAVE):
    '''
    Crucially, the MC steps must be high because the cumulant plot shows how
    fluctuations in cumulant value due to poor averaging creates a plethora of
    intersection points between cumulant pairs.
    
    Maybe instead of standard deviations which include smaller lattice sizes
    with a less accurate binder cumulant, you could just find the ratio of the
    two best cumulant datasets (highest sizes and 10^6 MC steps).
    Then do curie_temp_index = np.argmin(abs(ratio - 1))
    

    '''
    
    magnetisation_data_list = magnetisation_file_finder(directory)
    curie_cumulants = []
    lengths_list = []

    for count, magnetisation_filename in enumerate(magnetisation_data_list):
        (length, temperature_data, magnetisation_plot_data,
         magnetisation_abs_plot_data, magnetisation_variance_data,
         susceptibility_data, susceptibility_abs_data, cumulant) = (
             calculate_magnetic_properties(magnetisation_filename))
        
        plt.plot(temperature_data, cumulant,
                 label='{0}x{0}'.format(length),
                 linestyle=linestyle[count])
        
        curie_cumulants += [cumulant]
        lengths_list += [length]
    
    plt.legend()
    plt.title("Binder cumulant about critical point")
    plt.xlabel('Temperature')
    plt.ylabel("Binder cumulant")
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.005))
    plt.xticks(fontsize=8)
    
    if save:
        plt.savefig(directory + "cumulant_intersection_plot",
                    dpi=600)
    
    plt.show()  
    plt.close()
    
    curie_cumulants = file_truncator(np.array(curie_cumulants, dtype=object))
    curie_cumulants = np.array(curie_cumulants, dtype=float)
    
    width = len(curie_cumulants[0])
    height = len(magnetisation_data_list)
    np.reshape(curie_cumulants, (width,height))
    
    # header_list = np.around(temperature_data[:width], 2)
    # indices = []
    # for count in range(height):
    #     length = lengths_list[count]
    #     indices.append('{0}x{0} Cumulant'.format(length)) 
    
    # cumulant_dataframe = pd.DataFrame(curie_cumulants, columns=header_list)
    # cumulant_dataframe.insert(0, 'Temperature', indices)
    # cumulant_dataframe.insert(1, '|' , ['|']*len(indices))
    # filename = directory + "cumulant_dataframe"
    # cumulant_dataframe.to_csv(filename, index=0, header=1, sep=',')
    
    cumulant_std = np.std(curie_cumulants, axis=0)
    
    for count, value in enumerate(np.sort(cumulant_std), 1):
        if count <= 5:
            temp_index = np.where(cumulant_std == value)[0][0]
            print("Intersection {0} : T = {1:.3f}".format(count,
                                                          temperature_data[temp_index]))
        else:
            break
    
    curie_temperature_arg = np.argmin(cumulant_std)
    curie_temperature = temperature_data[curie_temperature_arg]
    print("Curie temperature = {0:.3f}".format(curie_temperature))
    
    # plt.legend(bbox_to_anchor=(1.4, 1), edgecolor='k', facecolor='w',
    #            fontsize=10)

    # textbox = dict(boxstyle='round', edgecolor='k', facecolor='w',
    #                alpha=0.75)
    # label = "Intersection at T = " + str(curie_temperature)
    # plt.text(1.04, 0.25, label)


if __name__ == "__main__":
    main()