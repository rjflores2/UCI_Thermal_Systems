# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:28:46 2023

@author: Bobby
"""

if chosen_parameter_name == 'H2 inlet temperature':
    streams_in[0].T = parameter_value; #print('test',parameter_value)
elif chosen_parameter_name == 'H2 inlet pressure':
    streams_in[0].P = parameter_value
else:
    raise Exception('Invalid definition of chosen_parameter_name. Check definition in input module.')

# Define parameters and constants
final_stage_props = all_component_inputs['Properties'][all_component_inputs['Stage']]; #print(final_stage_props)
Tc = CP.PropsSI('Tcrit','H2') # [K] critical temperature
Pc = CP.PropsSI('Pcrit','H2') # [Pa] critical pressure
T_R = final_stage_props[0]/Tc; #print('T_R = ', T_R) # dimensionless reduced temperature
P_R = final_stage_props[1]/Pc; #print('P_R = ',P_R) # dimensionless reduced pressure
Z = CP.PropsSI('Z','T',final_stage_props[0],'P',final_stage_props[1],'H2'); #print('Compressibility factor Z = ',Z)
if Z > 1.2:
    raise Exception('Ideal gas model cannot be assumed. Check inputed temperature and pressure of final stage in H2_compressor_input.py module.')
T_N = 298.13 # [K] normal temperature
P_N = 101325 # [Pa] normal pressure
H2_den = CP.PropsSI('D','T', T_N,'P',P_N,'H2'); #print('H2 density = ', H2_den) # [kg/m^3] density at normal operating conditions to determine mass flow rate
R = CP.PropsSI('gas_constant','H2'); #print('R = ', R) # [J/mol/K] universal gas constant
H2_mm = CP.PropsSI('molarmass', 'H2') # [kg/mol]
R_H2 = R/H2_mm; #print('R_H2 = ', R_H2) # [J/kg/K]
h_H2_in = CP.PropsSI('Hmass','T',streams_in[0].T,'P',streams_in[0].P,'H2') # [J/kg] mass specifc enthalpy of H2
h_H2_out = CP.PropsSI('Hmass','T',loop_props[0],'P',loop_props[1],'H2') # [J/kg] mass specific enthalp of H2
H2_Cp = Cp_mass('H2', streams_in[0].P,streams_in[0].T); #print('H2 Cp = ' , H2_Cp) # mass specific constant pressure specifc heat[J/kg/K]
H2_Cv = Cv_mass('H2', streams_in[0].P,streams_in[0].T); #print('H2 Cv = ' , H2_Cv) # mass specific constant volume specific heat [J/kg/K]
k = H2_Cp/H2_Cv; #print('k = ', k)
mdot_H2 = (compressor_main_props['capacity'])*(H2_den/3600); #print(mdot_H2) # [kg/s]
# if s == 1: # calculate amount stored in buffer tank
#     print('s = ', s)
H2O_den = CP.PropsSI('D','T', streams_in[1].T,'P',streams_in[1].P,'H2O'); #print('H2O density = ', H2O_den) # [kg/m^3] density of cooling water
h_H2O_in = CP.PropsSI('Hmass','T',streams_in[1].T,'P',streams_in[1].P,'H2O') # [J/kg] mass specifc enthalpy of inlet cooling water
Cp_H2O = Cp_mass('H2O_L', streams_in[1].P, streams_in[1].T); #print('H2O Cp = ' , Cp_H2O) # mass specific constant pressure specifc heat[J/kg/K] of cooling water
mdot_H2O_total = (compressor_main_props['cooling water flow']*0.001/60)*H2O_den # [kg/s]
mdot_H2O = mdot_H2O_total/4; #print('CW mass flow rate = ', mdot_H2O, '[kg/s]') # [kg/s] initial guess to be solved later 

# Mass/energy balance
if all_component_inputs['Type'] == 'diaphragm': # assumes isothermal compressor work
    Wdot = mdot_H2*R_H2*((streams_in[0].T+loop_props[0])/2)*ln(loop_props[1]/streams_in[0].P); #print('Isothermal work = ', Wdot, ' [W]') # [W]
elif all_component_inputs['Type'] == 'reciprocating': # assumes adiabatic compressor work
    Wdot = mdot_H2*((k*R_H2*streams_in[0].T)/(k-1))*(((loop_props[1]/streams_in[0].P)**((k-1)/k)) -1); #print('Adiabatic work = ', Wdot, ' [W]') # [W]
dU = (h_H2_out-h_H2_in);# print('Change in enthalpy = ', dU, ' [J/kg]')
Wdot_act = mdot_H2*dU; #print('Actual work done = ', Wdot_act, ' [W]') # [W]
Qdot_cool = Wdot_act - Wdot; #print('Heat transfer out = ', Qdot_cool, ' [W]') # [W]
T_cw_out = (mdot_H2O*Cp_H2O*streams_in[1].T - Qdot_cool)/(mdot_H2O*Cp_H2O) ; #print('Cooling water outlet temperature = ', T_cw_out, ' [K]') # [K]

streams_out[0].T = loop_props[0] # [K] head outlet temperature is per inputed specs
streams_out[0].P = loop_props[1] # [Pa] head outlet pressure is per inputed specs
streams_out[0].N = streams_in[0].N
streams_out[0].x_H2 = streams_in[0].x_H2

streams_out[1].T = T_cw_out
streams_out[1].P = streams_in[1].P
streams_out[1].N = streams_in[1].N
streams_out[1].x_H2O_l = streams_in[1].x_H2O_l

# Compile results of interest
parameter_work.append(Wdot)
parameter_heat_head.append(Qdot_cool)