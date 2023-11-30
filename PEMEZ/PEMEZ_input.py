# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:38:06 2023

@author: rhl
"""

# Import directories, functions, toolboxes etc.
import math; import numpy as np; from numpy import log as ln; import matplotlib.pyplot as plt; from math import pi;
from scipy.integrate import odeint; from scipy.optimize import fsolve;
import CoolProp.CoolProp as CP; import cantera as CT;
import time; import xlsxwriter
import os;

#---------------------------------------
# Defining class, attribute, and instances for PEMEZ. Add new instances for new streams. 
class Stream:
    component = "" # update this attribute for each modeled component
    all_streams = []
    def __init__(self, s, i, c, T, P, N, x_KOH, x_H2O_l, x_H2O_v, x_H2, x_O2, x_N2):
        self.all_streams.append(self)
        self.s = s
        self.i = i
        self.c = c
        self.T = T
        self.P = P
        self.N = N
        self.x_KOH = x_KOH
        self.x_H2O_l = x_H2O_l
        self.x_H2O_v = x_H2O_v
        self.x_H2 = x_H2
        self.x_O2 = x_O2
        self.x_N2 = x_N2

#---------------------------------------
# Include all components for respective shell (PEMEZ)--- list in flow diagram order
# Refer to Operational Guide for stream tag information
components_subsytem = ['PEMEZ_stack.py', 'gas_liquid_separator.py']
components_subsystem_streams = np.array([[2,3], # amount of inlet streams in respective component
                                    [2,2], # amount of outlet streams in respective component
                                    [[1,2],[3,7,8]], # stream tags for each inlet stream of respective component
                                    [[3,4],[5,6]]], dtype=object) # stream tags for each outlet stream of respective component
components_subsystem_folders = ['PEMEZ_stack','PEMEZ_BoP']
path_system = r'' # paste in system path of specifc operating machine
path_subsystem = r'' # paste in subsystem path of specifc operating machine

# Importing custom functions for all components of subsystem
os.chdir(path_system) # changing current working directory (folder) back D2E P2P system folder to import custom created functions
from Functions import * # imports all created functions
os.chdir(path_subsystem) # changing current working directory (folder) back to subsystem folder to execute import functions, path is defined in PEMEZ_input
from sub_system_functions import *
#---------------------------------------
# Defining chosen components and current density to solve 
"""
The components that you want to run can be selected by slicing the array "components_subsystem" and array "components_subsystem_streams. 
Slice by taking all rows (:) and selecting which columns, or components, you want.
The ending index is not included. COLUMN SLICES FOR EACH ARRAY MUST MATCH.
For example: print(components_subsystem[1:2] 
                ['gas_liquid_separator.py']
For example: print(components_subsystem_streams[:,1:2] 
               [[3]
                [2]
                [list([3, 7, 8])]
                [list([5, 6])]]
"""
cs_index_start = 0
cs_index_stop = 2
components_list = components_subsystem[cs_index_start:cs_index_stop]; #print('components_list = ', len(components_list))
components_folders_list = components_subsystem_folders[cs_index_start:cs_index_stop]
streams = components_subsystem_streams[:,cs_index_start:cs_index_stop];  #print('streams = ', (streams[1,1]))

# Verification of chosen components
if len(components_list) != len(streams[0]):
    raise Exception('Column slices do not match. Please check slices for components_list and streams.')
for y in range(len(components_list)):
    component = components_list[y]
    if y+1 == len(components_list):
        break
    next_component = components_list[y+1]
    check = any(tag in streams[3,y] for tag in streams[2,y+1])
    if check == False:
        raise Exception('Components were not sliced in consecutive order. '+ component + ' does not have any inputs into '+ next_component )

"""Inputted physical parameters to be changed based on chosen components:

1. Define current range.
2. Define input array at chosen starting component.
3. Define input (initial) streams into the chosen starting component.

"""
# Define current range
i_start = 0.1; i_end = 0.7; i_step = 0.1;  # change the start value, end value, and step value (can change to the same value to run at 1 current density value)
i_range = np.arange(i_start, i_end+i_step, i_step); #print(i_range) #[A/cm^2] current density range 
i_index_start = 0
i_index_stop = -1
current_range = i_range[i_index_start:i_index_stop]; #print(current_range)

# Define input array at chosen starting component
Q_in = 110; Q_in = Q_in/(1000*3600) # [L/hr] converted to [m^3/s] 
#Q_in = 1.5 # [kg/s]
c = 0 # index of string array "components_PEMEZ" corresponding to model name of first component (AlkalineEZstack)
s_1 = 1 #  must match stream inlet tags in Stream Tag Table of Operational Guide
s_2 = 2 #  must match stream inlet tags in Stream Tag Table of Operational Guide
i = current_range[0] # initial current density value
T_in = 298.15 # [K]
P_in = 1e6 # [Pa]
species_in_ca = 1 # 
species_in_an = 1 # assumes anode and cathode flow rates are equal and sum to total flow rate
N_in_ca = species_in_ca; N_in_an = species_in_ca
x_KOH_ca = species_in_ca.x[0]; x_H2O_l_ca = species_in_ca.x[1]; 
x_KOH_an = species_in_an.x[0]; x_H2O_l_an = species_in_an.x[1];
x_H2O_v = 0; x_H2 = 0; x_O2 = 0; x_N2 = 0

# Define initial streams with defined class for object oriented data transfer
s_1 = Stream(s_1, i, c, T_in, P_in, N_in_ca, x_KOH_ca, x_H2O_l_ca, x_H2O_v, x_H2, x_O2, x_N2); #print(s_1.N)
s_2 = Stream(s_2, i, c, T_in, P_in, N_in_an, x_KOH_an, x_H2O_l_an, x_H2O_v, x_H2, x_O2, x_N2)
streams_in = [s_1, s_2]; # add/delete Stream objects depending on starting component
streams_in_start = streams_in # defined so that inlet conditions don't change as current density increases (only for starting component)
input_array = class2array((streams_in[0]), (streams_in)); array_in = input_array

#---------------------------------------
# Defining properties to be collected from chosen components
T_list_stack = []; 