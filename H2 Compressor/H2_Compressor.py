# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:00:14 2023

@author: rhl
"""

#---------------------------------------
# Configurations
import warnings
warnings.simplefilter('default', RuntimeWarning)

#---------------------------------------
# Loading inputs and components to solve
exec(open('H2_compressor_input.py').read())

# Execute model logic for n amount of stages

for s in range(1,all_component_inputs['Stages']+1):
    compressor_main_props = all_component_inputs['Properties'][0]
    stage_props = all_component_inputs['Properties'][s]
    # if s > 1:
    #     parameter_value = 
    exec(open('H2_compressor_initialize.py').read())
    print('Compressor stage ', s, ' has finished running.'); print('')
    
    # Execute data collection and plots
    exec(open('H2_compressor_data.py').read())


#---------------------------------------
print('H2_compressor.py has finished running.'); print('')