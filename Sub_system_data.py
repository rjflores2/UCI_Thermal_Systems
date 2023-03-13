# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:27:14 2023

@author: rhl
"""

# Import directories, functions, toolboxes etc.
import os,sys
import math; import numpy as np; from numpy import log as ln; import matplotlib.pyplot as plt;

# Configure sub-system data collection for excel file. Update array_in/out labels based on species that can be added/removed to the Stream class.
array_in_labels = ['stream #', 'i [A/cm^2]', 'model #', 'T_in [K]', 'P_in [Pa]','N_in [mol/s]', 'molar fraction KOH', 'molar fraction H2O_l', 'molar fraction H2O_v', 'molar fraction H2', 'molar fraction O2']
array_out_labels = ['stream #','i [A/cm^2]', 'model #', 'T_out [K]', 'P_out [Pa]','N_out [mol/s]', 'molar fraction KOH', 'molar fraction H2O_l', 'molar fraction H2O_v', 'molar fraction H2', 'molar fraction O2']
AEZ_data = xlsxwriter.Workbook('AEZ_data.xlsx')
cell_format_header = AEZ_data.add_format(); cell_format_header.set_text_wrap()
array_format = AEZ_data.add_format(); array_format.set_bottom(5)
cell_format_in = AEZ_data.add_format({'bg_color': 'red', 'bottom': True})
cell_format_out = AEZ_data.add_format({'bg_color': 'green', 'bottom': True})

# Iteration through nonzero values to write excel file
for y in range(len(components_list)):
    component = components_list[y]
    sheet = sub_system_data.add_worksheet(component)
    for labels in range(len(array_in_labels)):
        sheet.write(0, labels, array_in_labels[labels], cell_format_header)
        sheet.write(0, labels+len(array_in_labels), array_out_labels[labels], cell_format_header)
    for rows in range(len(array_in_master[y])):
        sheet.write_row((rows+1), 0, array_in_master[y,rows,:], cell_format_in) # writing input array to sheet for respective component
    for rows in range(len(array_out_master[y])):
        sheet.write_row((rows+1), len(array_in_labels), array_out_master[y,rows,:], cell_format_out) # writing input array to sheet for respective component

AEZ_data.close()

#---------------------------------------
# Compile component specific data collection for desired outputs (polarization curves, H2 production, etc.)