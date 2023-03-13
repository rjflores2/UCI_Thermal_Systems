# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:19:49 2023

@author: rhl
"""

import math; import numpy as np; from numpy import log as ln; from math import pi;
import CoolProp.CoolProp as CP;
#---------------------------------------

def Cp_mass(gas, T):
   """ (string, number) -> number
   Return the ideal-gas specific heat of the desired gas a function of temperature.
   T is in [K], mm is in [kg/mol] from CoolProp, Cp is in [J/kg/K]
   Source: B. G. Kyle, Chemical and Process Thermodynamics(Englewood Cliffs, NJ: Prentice-Hall, 1984).
   """
   import CoolProp.CoolProp as CP; 
   if gas == 'H2': # hydrogen
       a = 29.11; b = -0.1916*10**-2; c = 0.4003*10**-5; d = -0.8704*10**-9
       mm = CP.PropsSI('M', 'H2'); # molar mass
   elif gas == 'O2': # oxygen
       a = 25.48; b = 1.520*10**-2; c = -0.7155*10**-5; d = 1.312*10**-9
       mm = CP.PropsSI('M', 'O2'); # molar mass
   elif gas == 'H2O': # water vapor
       a = 32.24; b = 0.1923*10**-2; c = 1.055*10**-5; d = -3.595*10**-9
       mm = CP.PropsSI('M', 'H2O'); # molar mass
   elif gas == 'N2': # nitrogen
       a = 28.90; b = -0.1571*10**-2; c = 0.8081*10**-5; d = -2.873*10**-9
       mm = CP.PropsSI('M', 'N2'); # molar mass
   return ((a + (b*T)+(c*T**2)+(d*T**3))/mm)

#---------------------------------------

def Cp_mol(gas, T):
   """ (string, number) -> number
   Return the ideal-gas specific heat of the desired gas a function of temperature.
   T is in [K], Cp is in [J/mol/K]
   Source: B. G. Kyle, Chemical and Process Thermodynamics(Englewood Cliffs, NJ: Prentice-Hall, 1984).
   """
   import CoolProp.CoolProp as CP; 
   if gas == 'H2': # hydrogen
       a = 29.11; b = -0.1916*10**-2; c = 0.4003*10**-5; d = -0.8704*10**-9
   elif gas == 'O2': # oxygen
       a = 25.48; b = 1.520*10**-2; c = -0.7155*10**-5; d = 1.312*10**-9
   elif gas == 'H2O': # water vapor
       a = 32.24; b = 0.1923*10**-2; c = 1.055*10**-5; d = -3.595*10**-9
   elif gas == 'N2': # nitrogen
       a = 28.90; b = -0.1571*10**-2; c = 0.8081*10**-5; d = -2.873*10**-9
   return ((a + (b*T)+(c*T**2)+(d*T**3)))

#---------------------------------------

def h_CP(gas, P, T):
   """ (string, float, float) -> number
   Return the mass specific enthalpy of the desired gas a function of temperature and pressure.
   Pulled from COOL PROP library.
   T is in [K], h_CP is in [J/kg]
   """
   import CoolProp.CoolProp as CP; 
   if gas == 'H2':
       hm_CP = CP.PropsSI('H','T',T,'P',P,'H2'); 
   elif gas == 'O2':
       hm_CP = CP.PropsSI('H','T',T,'P',P,'O2'); 
   elif gas == 'H2O_L':
       hm_CP = CP.PropsSI('H','T|liquid',T,'P',P,'H2O'); 
   elif gas == 'H2O_V':
       hm_CP = CP.PropsSI('H','T|gas',T,'P',P,'H2O');
   return hm_CP

#---------------------------------------

def rxn_H(T_in, T_out):
    """ (float, float) -> float
    Return the molar enthalpy of the electrochemical reaction at specified inlet and outlet temperatures.
    T_in and T_out are in [K], rxn_H is in [J/mol]
    """
    O2_HformSTD = 0; # [J/mol] formation enthalpy of oxygen(g) at STD
    O2_SformSTD = 205; # [J/mol/K] formation enropy of oxygen(g) at STD
    H2_HformSTD = 0; # [J/mol] formation enthalpy of hydrogen(g) at STD
    H2_SformSTD = 130.68; # [J/mol/K] formation enropy of hydrogen(g) at STD
    H2O_HformSTD = -285830; # [J/mol] formation enthalpy of water(l) at STD
    H2O_SformSTD = 69.95; # [J/mol/K] formation enropy of water(l) at STD
    H2_Cp_in_fun = Cp_mol('H2', T_in) # [J/mol/K]
    O2_Cp_in_fun = Cp_mol('O2', T_in);  # [J/mol/K] 
    return (1*(H2_HformSTD + ((H2_Cp_in_fun + Cp_mol('H2', T_out))/2)*(T_out-T_in)) # H2_Hform (1/3) rxn_H 
         +0.5*(O2_HformSTD + ((O2_Cp_in_fun + Cp_mol('O2', T_out))/2)*(T_out-T_in)) # O2_Hform (2/3) rxn_H 
        -(1*H2O_HformSTD)) # (3/3) rxn_H 

#---------------------------------------

def rxn_S(T_in, T_out):
    """ (float, float) -> float
    Return the molar entropy of the electrochemical reaction heat at specified inlet and outlet temperatures.
    T_in and T_out are in [K], rxn_S is in [J/mol/K]
    """
    O2_HformSTD = 0; # [J/mol] formation enthalpy of oxygen(g) at STD
    O2_SformSTD = 205; # [J/mol/K] formation enropy of oxygen(g) at STD
    H2_HformSTD = 0; # [J/mol] formation enthalpy of hydrogen(g) at STD
    H2_SformSTD = 130.68; # [J/mol/K] formation enropy of hydrogen(g) at STD
    H2O_HformSTD = -285830; # [J/mol] formation enthalpy of water(l) at STD
    H2O_SformSTD = 69.95; # [J/mol/K] formation enropy of water(l) at STD
    H2_Cp_in_fun = Cp_mol('H2', T_in) # [J/mol/K]
    O2_Cp_in_fun = Cp_mol('O2', T_in);  # [J/mol/K] 
    return (1*(H2_SformSTD + ((H2_Cp_in_fun + Cp_mol('H2', T_out))/2)*(T_out-T_in)/((T_in+T_out)/2))  # H2_Sform (1/3) rxn_S 
            +0.5*(O2_SformSTD + ((O2_Cp_in_fun + Cp_mol('O2', T_out))/2)*(T_out-T_in)/((T_in+T_out)/2)) # O2_Sform (2/3) rxn_S 
            -(1*H2O_SformSTD)) # (3/3) rxn_S

#---------------------------------------

def class2array(stream, streams_array): 
    """ (Stream object, 1D array of Stream objects) -> 2D float array
    The Stream object must be be an object included in streams_array
    """
    import numpy as np;
    input_output_array =[]
    for parameter in stream.__dict__.items():
        input_output_array.append(parameter[1])
    rows = len(streams_array); columns = len(input_output_array); input_output_array = np.zeros((rows,columns)); #print(input_output_array)
    for index_s_in in range(len(streams_array)):
        stream = streams_array[index_s_in]
        for index_p in range(len(stream.__dict__.items())):
            parameters = stream.__dict__.items(); keys = list(parameters); parameter = keys[index_p] # https://stackoverflow.com/questions/4326658/how-to-index-into-a-dictionary
            input_output_array[index_s_in,index_p] = parameter[1]
    return input_output_array

#---------------------------------------

def Cv_mass(gas, P, T):
   """ (string, float, float) -> number
   Return the mass specific consant volume specifc heat of the desired gas a function of temperature and pressure.
   Pulled from COOL PROP library.
   T is in [K], Cv is in [J/kg/K]
   """
   import CoolProp.CoolProp as CP; 
   if gas == 'H2':
       Cv_mass_CP = CP.PropsSI('Cvmass','T',T,'P',P,'H2'); 
   elif gas == 'O2':
       Cv_mass_CP = CP.PropsSI('Cvmass','T',T,'P',P,'O2'); 
   elif gas == 'H2O_L':
       Cv_mass_CP = CP.PropsSI('Cvmass','T|liquid',T,'P',P,'H2O'); 
   elif gas == 'H2O_V':
       Cv_mass_CP = CP.PropsSI('Cvmass','T|gas',T,'P',P,'H2O');
   return Cv_mass_CP

#---------------------------------------
# Function output check
if __name__ == '__main__':
    # Assumed operation conditions to use in checking functions
    
    P = (500000) # [Pa]
    P_op_bar = P*1E-5 # [bar]
    T_in = 333.15 # [K]
    T_out = 333.15 # [K]
    T = T_out
    T_avg = (T_in+T_out)/2; T_avg_C = T_avg -273.15
    w = 25 # weight percent of electrolyte solution
    i =0.2
    print('Cp_mass = ', Cp_mass('H2', T), '[J/kg/K]')
    print('Cp_mol = ', Cp_mol('H2', T), '[J/mol/K]')
    print('h_CP = ', h_CP('H2O_L', P, T), '[J/kg]')
    print('rxn_H = ', rxn_H(T_in,T_out), '[J/mol]')
    print('rxn_S = ', rxn_S(T_in,T_out), '[J/mol/K]')
    print('Cv_mass = ', Cv_mass('H2', P, T), '[J/kg/K]')