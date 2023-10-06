# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 16:21:21 2023

@author: rhl
"""
from math import pi
# Specs of AEZ chiller
pump_power = 3 # [hp] 
qdot = 30; qdot = qdot*0.00006309019640343866 # [gpm], [m^3/s] flow rate
p = 55; p = p*6894.76 # [psi], [Pa] pressure
mdot_air = 8000 # [CFM] condenser air flow
pipe_size = 1; pipe_ID = 1.049; pipe_ID = pipe_ID*0.0254 # [N/A], [inches], [m] pipe size and inner diameter
pipe_area = pi*(pipe_ID/2)**2

# Calcs
total_p = p + 0.5*999*(qdot/pipe_area)**2; print(total_p
                                                 )