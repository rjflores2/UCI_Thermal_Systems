# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:24:47 2023

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
# Configurations
plt.close('all'); plt.rcParams['font.size'] = '16'; 
import warnings
warnings.simplefilter('default', RuntimeWarning)

#---------------------------------------
# Loading inputs and components to solve
exec(open('Sub_system_input.py').read())

#---------------------------------------
# Loops to run chosen components
# Runs models at only 1 current density value
if len(current_range) == 1: # checks to see if you are solving for only 1 current density
    # Defining storage matrices for 1 currenty densitiy
    sheets = len(components_list)+1; rows_in = np.sum(streams[0]); rows_out = np.sum(streams[1]); columns = len(array_in[0]); # defining dimensions for 3D matrices for storage
    array_in_master = np.zeros((sheets, rows_in, columns)) # Indexes: component #, row #, column value (row # is total amount of inlet streams) 
    array_out_master = np.zeros((sheets, rows_out, columns)) # Indexes: component #, row #, column value (row # is total amount of outlet streams)
    # Initial solving of first component to storage populate arrays and input/output streams
    i = streams_in[0].i
    component = components_list[0]
    array_in_master[0, 0:streams[0,0], :] = array_in; #print(array_in_master[0, x:(x+components_list[1][0]), :])
    exec(open(component).read())
    array_out_master[0, 0:streams[1,0], :] = array_out
    if len(components_list) > 1: # conditional statement to check if multiple are to be solved
        # Loop iteration for each component of components_list after first component
        for y in range(1,len(components_list)): # starting index 1 of components_list because first component of components_list was already solved
            streams_in =[]; 
            component = components_list[y]
            c = y; 
            for index_s_out in range(len(streams_out)): # for each outlet stream (starting at first component) --- defined at end of each component model
                stream = streams_out[index_s_out]
                if stream.s in streams[2,y]:
                    array_in_master[y, 0:streams[0,y], :] = array_out[index_s_out];
                    stream_in = Stream(stream.s, i, c, T_out, P_out, N_out, x_KOH_out, x_H2O_l_out, x_H2O_v_out, x_H2_out, x_O2_out)
                    streams_in.append(stream_in)
                else:
                    print('Stream ' + str(stream.s) + ' is not an input into ' + str(component))
            exec(open(component).read()) # ***solving model when condition is satisfied changes streams_out***
            array_out_master[y,0:(streams[1][y]),:] = array_out; #print(array_out_master) # storing output of current component
        
# Run models over a range of current densities
elif len(current_range) > 1 :
    # Defining storage matrices for a range of currenty densities
    sheets = len(components_list)+1; rows_in = len(current_range)*np.sum(streams[0]); rows_out = len(current_range)*np.sum(streams[1]); columns = len(array_in[0]); # defining dimensions for 3D matrices for storage
    array_in_master = np.zeros((sheets, rows_in, columns)) # Indexes: component #, row #, column value (row # is total amount of inlet streams) 
    array_out_master = np.zeros((sheets, rows_out, columns)) # Indexes: component #, row #, column value (row # is total amount of outlet streams)
    # Initial solving of first component to populate storage arrays and input/output streams
    for x in range(len(current_range)): # runs if you are solving over a range of current densities
        i = current_range[x]; 
        streams_in = streams_in_start # redefines starting streams to be starting values
        for y in range(len(components_list)):
            component = components_list[y]; c = y;
            for stream in streams_in:
                stream.i = i
                stream.c = c
            array_in = class2array(streams_in[0], streams_in)
            array_in_master[y, (x*streams[0,y]):(x*streams[0,y]+streams[0,y]), :] = array_in; #print(array_in_master[0, x:(x+components_list[1][0]), :])
            exec(open(component).read()); 
            array_out_master[y, (x*streams[1,y]):(x*streams[1,y]+streams[1,y]), :] = array_out
            streams_in =[]
            if y+1 == len(components_list):
                break
            for index_s_out in range(len(streams_out)): # for each outlet stream (starting at first component) --- defined at end of each component model
                stream = streams_out[index_s_out]
                if stream.s in streams[2,y+1]:
                    array_in_master[y+1,(x*streams[0,y+1]):(x*streams[0,y+1]+streams[0,y+1]), :]  = array_out[index_s_out]; #print(array_in_master[y+1,x:(x+components_list[1][y]), :]) # storing output of current component as input of next component 
                    stream_in = Stream(stream.s, i, c, T_out, P_out, N_out, x_KOH_out, x_H2O_l_out, x_H2O_v_out, x_H2_out, x_O2_out)
                    streams_in.append(stream_in); 
                else:
                    print('Stream ' + str(stream.s) + ' is not an input into ' + str(components_list[y+1]))
else: 
    raise Exception('Invalid current density range/value selected. Length of current_range must be equal to or greater than 1. Please check current_range.')

#---------------------------------------
# Execute data collection and plots
exec(open("Sub_system_data.py").read())

#---------------------------------------
print('Sub_system_initialize.py has finished running.')