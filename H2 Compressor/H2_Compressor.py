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

# Execute model logic 
exec(open('H2_compressor_initialize.py').read())

# Execute data post processing and plots
exec(open('H2_compressor_data.py').read())

#---------------------------------------
print('H2_compressor.py has finished running.'); print('')