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
from P2P_functions import class2array

#---------------------------------------
# Defining class, attribute, and instances for AEZ. Add new instances for new streams. 
class Stream:
    component = "first_component.py" # update this attribute for each modeled component
    all_streams = []
    def __init__(self, s, i, c, T, P, N, x_KOH, x_H2O_l, x_H2O_v, x_H2, x_O2):
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

#---------------------------------------
# Include all components for respective shell --- list in flow diagram order
components_sub_system = ["x.py", "y.py"]
components_sub_system_streams = np.array([[2,1], # amount of inlet streams in respective component
                                   [2,2], # amount of outlet streams in respective component
                                   [[1,2],[3]], # stream tags for each inlet stream of respective component
                                   [[3,4],[5,6]]], dtype=object) # stream tags for each outlet stream of respective component

#---------------------------------------
# Defining chosen components and current density to solve 
cs_index_start = 0
cs_index_stop = 2
components_list = components_sub_system[cs_index_start:cs_index_stop]; #print('components_list = ', len(components_list))
streams = components_sub_system_streams[:,cs_index_start:cs_index_stop];  #print('streams = ', (streams[1,1]))

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

# Define current range
i_start = 0.1; i_end = 0.7; i_step = 0.1;  # change the start value, end value, and step value (can change to the same value to run at 1 current density value)
i_range = np.arange(i_start, i_end+i_step, i_step); #print(i_range) #[A/cm^2] current density range 
i_index_start = 0
i_index_stop = -1
current_range = i_range[i_index_start:i_index_stop]

# Defining properties to be collected
T_list = []; 

# Define input array at chosen starting component
c = 0 # index of starting component of components_list
s_1 = 1 # must match s_in_track[0] of starting component
s_2 = 2 #  must match s_in_track[1] of starting component
i = i_start # initial current density value
T_in = 298.15 # [K]
P_in = 5*101325 # [Pa]
N_in = 0.1602; 
x_KOH = 0.147; x_H2O_l = 0.853; x_H2O_v = 0; x_H2 = 0; x_O2 = 0

# Define initial streams with defined class for object oriented data transfer
s_1 = Stream(s_1, i, c, T_in, P_in, N_in, x_KOH, x_H2O_l, x_H2O_v, x_H2, x_O2); #print(s_1.N)
s_2 = Stream(s_2, i, c, T_in, P_in, N_in, x_KOH, x_H2O_l, x_H2O_v, x_H2, x_O2)
streams_in = [s_1, s_2]; # add/delete Stream objects depending on starting component
streams_in_start = streams_in # defined so that inlet conditions don't change as current density increases (only for starting component)
input_array = class2array((streams_in[0]), (streams_in)); array_in = input_array