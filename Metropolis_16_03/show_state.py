# -*- coding: utf-8 -*-
"""
Title: __________
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Thu Feb 23 11:13:29 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def plot_state(state, label):    
    # create discrete colormap
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [-1,1,10]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    fig, ax = plt.subplots()
    ax.imshow(state, cmap=cmap, norm=norm)
    ax.set_title('Iteration {}'.format(label))

    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, len(state), 1))
    ax.set_yticks(np.arange(-0.5, len(state), 1))
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)
    
    plt.show()