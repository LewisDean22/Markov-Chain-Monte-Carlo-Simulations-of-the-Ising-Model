# -*- coding: utf-8 -*-
"""
Title: Print variable
------------------------------------------------------------------------
                         description
------------------------------------------------------------------------
Created: Wed Feb 15 16:37:00 2023
Author: Robin de Freitas
UID: 10887826
Contact: robin.defreitas@student.manchester.ac.uk
"""
from inspect import currentframe

def pvar(var):
    frame = currentframe().f_back
    frame_locals = frame.f_locals
    frame_globals = frame.f_globals

    for name, val in {**frame_locals, **frame_globals}.items():
        if val is var:
            print(f"{name}: {val}")
