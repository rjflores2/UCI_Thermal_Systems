# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:09:59 2023

@author: rhl
"""

# Import directories, functions, toolboxes etc.
import math; import numpy as np; from numpy import log as ln; import matplotlib.pyplot as plt
from math import pi,exp, floor, log, sqrt, tanh;
from scipy.integrate import odeint; from scipy.optimize import fsolve;
import CoolProp.CoolProp as CP; import cantera as CT;
import time; import xlsxwriter
import os,sys;
import pandas as pd

#---------------------------------------
# Defining class, attribute, and instances for H2_compressor. Add new instances for new streams. 
class Stream:
    component = "" # update this attribute for each modeled component
    all_streams = []
    def __init__(self, s, c, T, P, N, x_KOH, x_H2O_l, x_H2O_v, x_H2, x_O2, x_N2):
        self.all_streams.append(self)
        self.s = s
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
# Include all components for respective shell (H2_compressor)--- list in flow diagram order
# Refer to Operational Guide for stream tag information
components_H2_compressor = ['H2_compressor_head.py', 'heat_exchanger.py']
components_H2_compressor_streams = np.array([[2,2], # amount of inlet streams in respective component
                                    [2,2], # amount of outlet streams in respective component
                                    [[40,41],[42,44]], # stream tags for each inlet stream of respective component
                                    [[42,43],[45,46]]], dtype=object) # stream tags for each outlet stream of respective component
components_H2_compressor_folders = ['H2 Compressor Head','H2 Compressor BoP']
path_system = r"C:\Users\rhl\Desktop\Python_scripts\UCI_Thermal_Systems\UCI_Thermal_Systems"
path_subsystem = r"C:\Users\rhl\Desktop\Python_scripts\UCI_Thermal_Systems\UCI_Thermal_Systems\H2 Compressor"

# Importing custom functions for all components of subsystem
os.chdir(path_system) # changing current working directory (folder) back to Thermal Systems system folder to import custom created functions
from Functions import * # imports all created functions
os.chdir(path_subsystem) # changing current working directory (folder) back to subsystem folder to execute import functions, path is defined in H2_compressor_input
# from H2_compressor_functions import *
#---------------------------------------
# Defining chosen components and temperature to solve 
"""
The components that you want to run can be selected by slicing the array "components_H2_compressor" and array "components_H2_compressor_streams. 
Slice by taking all rows (:) and selecting which columns, or components, you want.
The ending index is not included. COLUMN SLICES FOR EACH ARRAY MUST MATCH.
For example: print(components_H2_compressor[1:2] 
                ['heat_exchanger.py']
For example: print(components_H2_compressor_streams[:,1:2] 
               [[2]
                [2]
                [list([42, 44])]
                [list([45, 46])]]
"""
cs_index_start = 0
cs_index_stop = 2
components_list = components_H2_compressor[cs_index_start:cs_index_stop]; #print('components_list = ', len(components_list))
components_folders_list = components_H2_compressor_folders[cs_index_start:cs_index_stop]
streams = components_H2_compressor_streams[:,cs_index_start:cs_index_stop];  #print('streams = ', (streams[0,1]))

# Verification of chosen components
if len(components_list) != len(streams[0]):
    raise Exception('Column slices do not match. Please check slices for components_list and streams.')
for y in range(len(components_list)):
    component_check = components_list[y]
    if y+1 == len(components_list):
        break
    next_component = components_list[y+1]
    check = any(tag in streams[3,y] for tag in streams[2,y+1])
    if check == False:
        raise Exception('Components were not sliced in consecutive order. '+ component_check + ' does not have any inputs into '+ next_component )

# Define range for variable of interest (temperature, mass flow rate, pressure, etc. of any stream)
available_parameters = {'1': 'H2 inlet temperature',
                        '2': 'H2 inlet pressure'
                        }
chosen_parameter_name = available_parameters['1']
chosen_parameter_start = 300; chosen_parameter_end = 330; chosen_parameter_step = 5;  # change the start value, end value, and step value based on chosen inlet parameter (units are based on chosen parameter)
chosen_parameter_range = np.arange(chosen_parameter_start, chosen_parameter_end+chosen_parameter_step, chosen_parameter_step); #print(chosen_parameter_range) # inlet parameter range 
chosen_parameter_index_start = 0
chosen_parameter_index_stop = -1
chosen_parameter_range = chosen_parameter_range[chosen_parameter_index_start:chosen_parameter_index_stop]; #print(temp_in_range)

# Define loop parameters
component_loops = True # True loops through chosen components more than once, False does not loop through chosen components
loop_parameter = 'Stage'

# Define ambient conditions to be used in all components
T_STD = 293.15; P_STD = 101325; # [K],[Pa] standard operating conditions 
T_amb = T_STD; T_amb_C = T_amb - 273.15; P_amb = P_STD # [K], [C], [Pa] ambient temperature and pressure

def component_inputs(first_index, component):
    """
    Define inlet streams and other related properties of each component. 
    Only 1 set of inlet streams is used and is dependent on inputs to variables cs_index_start and cs_index_stop.
    """
    # Enter below the specific properties of the compressor
    s = 2 # number of stages of mechanical H2 compressor
    t = 'diaphragm' # type of mechanical H2 compressor (only 2 options are diaphragm or reciprocating)
    # Define parameters of n stage diaphragm compressor
    cap = 11.8 # [NM3H] rated volumetric flow rate of compressor in normal m^3/hr (must correct for actual)
    comp_speed = 376.1 # [RPM] compressor speed
    motor_p = 5 # [HP] motor power rating
    motor_speed = 1770 # [RPM] motor speed
    v_cool = 10 # [LPM] cooling water volumetric flow rate
    T_cool_step = 12.2 # [deg C] max temperature rise 
    HX_type = 'counterflow'
    stage1_T_out = 183.1+273.15 # [K] discharge temperature of first stage
    stage1_P_out = 63.88*100000 # [Pa] discharge pressure of first stage
    stage1_motor_BHP = 2 # [HP] motor shaft power at stage 1
    stage2_T_out = 182.29+273.25 # [K] discharge temperature of second stage
    stage2_P_out = 350*100000 # [Pa] discharge pressure of second stage
    stage2_motor_BHP = 2.1 # [HP] motor shaft power at stage 2
    main_props = {'capacity': cap,
                  'compressor speed': comp_speed,
                  'motor power': motor_p,
                  'motor speed': motor_speed,
                  'cooling water flow': v_cool,
                  'temperature rise': T_cool_step,
                  'HX type': HX_type}
    props = [main_props,
             [stage1_T_out, stage1_P_out, stage1_motor_BHP],
             [stage2_T_out, stage2_P_out, stage2_motor_BHP]]
    
# Enter below the starting conditions of streams for each component     
    if first_index == 'H2_compressor_head.py' or component == 'H2_compressor_head.py' :
        c = 0 # index of string array "components_H2_compressor" corresponding to model name 
        x_KOH = 0; x_H2O_v = 0; x_O2 = 0; x_N2 = 0
        
        s_40 = 40 #  must match stream inlet tags in Stream Tag Table of Operational Guide
        N_in_p = 0.0095 # [mol/s] process inlet molar flowrate
        x_H2_p = 1; x_H2O_l_p = 0
        P_in_p = 1.034e+6 # [Pa] (150 psi operating pressure of Teledyne HMXt-200)
        T_in_p = 325 # [K]
        s_40 = Stream(s_40, c, T_in_p, P_in_p, N_in_p, x_KOH, x_H2O_l_p, x_H2O_v, x_H2_p, x_O2, x_N2) 
        
        s_41 = 41 #  must match stream inlet tags in Stream Tag Table of Operational Guide
        N_in_cw = 0.012 # [mol/s] cooling water inlet molar flowrate
        x_H2_cw = 0; x_H2O_l_cw = 1
        P_in_cw = 275790 # [Pa] (40 psi delivery pressure from AEZ and compressor chiller)
        T_in_cw = 288 # [K] (60 deg F setpoint of AEZ and compressor chiller)
        s_41 = Stream(s_41, c, T_in_cw, P_in_cw, N_in_cw, x_KOH, x_H2O_l_cw, x_H2O_v, x_H2_cw, x_O2, x_N2)
        
        streams_in = [s_40, s_41]; 
    
    elif first_index == 'heat_exchanger.py' or component == 'heat_exchanger.py':
        c = 1 # index of string array "components_H2_compressor" corresponding to model name 
        x_KOH = 0; x_H2O_v = 0; x_O2 = 0; x_N2 = 0
        
        s_42 = 42 #  must match stream inlet tags in Stream Tag Table of Operational Guide
        N_in_p = 0.0095 # [mol/s] process inlet molar flowrate
        x_H2_p = 1; x_H2O_l_p = 0
        P_in_p = 1.034e+6 # [Pa] (150 psi operating pressure of Teledyne HMXt-200)
        T_in_p = 325 # [K]
        s_42 = Stream(s_42, c, T_in_p, P_in_p, N_in_p, x_KOH, x_H2O_l_p, x_H2O_v, x_H2_p, x_O2, x_N2) 
        
        s_44 = 44 #  must match stream inlet tags in Stream Tag Table of Operational Guide
        N_in_cw = 0.012 # [mol/s] cooling water inlet molar flowrate
        x_H2_cw = 0; x_H2O_l_cw = 1
        P_in_cw = 275790 # [Pa] (40 psi delivery pressure from AEZ and compressor chiller)
        T_in_cw = 288 # [K] (60 deg F setpoint of AEZ and compressor chiller)
        s_44 = Stream(s_44, c, T_in_cw, P_in_cw, N_in_cw, x_KOH, x_H2O_l_cw, x_H2O_v, x_H2_cw, x_O2, x_N2)
        
        streams_in = [s_42, s_44]; 
        
    Inputs = {
         'Stage':s,
         'Type': t,
         'Properties': props,
         'Inlet streams': streams_in}
     
    return Inputs

if len(components_list) > 1:
    all_component_inputs = component_inputs(components_list[cs_index_start], components_list[cs_index_start])
else:
    all_component_inputs = component_inputs(components_list[0], components_list[0])
compressor_main_props = all_component_inputs['Properties'][0]
streams_in = all_component_inputs['Inlet streams']; #print(streams_in) 
streams_in_start = streams_in # defined so that inlet conditions don't change as current density increases (only for starting component)
input_array = class2array((streams_in[0]), (streams_in))
array_in = input_array

# Checking validity of inlet stream definitions
if (len(streams_in) != len(streams[2,0])):
    raise Exception('The amount of defined inlet streams does not match the amount of expected inlet streams.') 
else:
    for stream in streams_in:
        if stream.s not in streams[2,0]:
            raise Exception('Defined inlet streams are not an input into first component of components_list. Check variables s.')                         
                          
#---------------------------------------
# Defining properties to be collected from chosen components
parameter_work = []
parameter_heat_head = []
parameter_HX_heat = []