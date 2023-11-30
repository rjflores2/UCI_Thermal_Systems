# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:16:59 2023

@author: rhl
"""
plt.close('all'); plt.rcParams['font.size'] = '14'; 

# Configure sub-system data collection for excel file. Update array_in/out labels based on species that can be added/removed to the Stream class.
array_in_labels = ['stream #', 'model #', 'T_in [K]', 'P_in [Pa]','N_in [mol/s]', 'molar fraction KOH', 'molar fraction H2O_l', 'molar fraction H2O_v', 'molar fraction H2', 'molar fraction O2','molar fraction N2']
array_out_labels = ['stream #', 'model #', 'T_out [K]', 'P_out [Pa]','N_out [mol/s]', 'molar fraction KOH', 'molar fraction H2O_l', 'molar fraction H2O_v', 'molar fraction H2', 'molar fraction O2','molar fraction N2']
H2_compressor_data = xlsxwriter.Workbook('H2_compressor_data'+str(s)+'.xlsx')
cell_format_header = H2_compressor_data.add_format(); cell_format_header.set_text_wrap()
array_format = H2_compressor_data.add_format(); array_format.set_bottom(5)
cell_format_in = H2_compressor_data.add_format({'bg_color': 'red', 'bottom': True})
cell_format_out = H2_compressor_data.add_format({'bg_color': 'green', 'bottom': True})

# # Removing zeros from storage arrays before writing to Excel
# for y in range(len(components_list)):
#     rows_zeros_in =[]; rows_zeros_out =[]
#     for rows in range(rows_in):
#         check_zeros = np.all(array_in_master[y,rows] == 0); 
#         if check_zeros == True:
#             rows_zeros_in.append(rows); 
#     nz = np.delete(array_in_master[y], np.s_[rows_zeros_in[0]:(rows_zeros_in[-1]+1)],0); #print(len(nz))
#     for rows in range(rows_out):
#         check_zeros = np.all(array_out_master[y,rows] == 0); 
#         if check_zeros == True:
#             rows_zeros_out.append(rows)
#     nz = np.delete(array_out_master[y], np.s_[rows_zeros_out[0]:(rows_zeros_out[-1]+1)],0); #print(len(nz))

# Iteration through nonzero values to write excel file
for y in range(len(components_list)):
    component = components_list[y]
    sheet = H2_compressor_data.add_worksheet(component)
    for labels in range(len(array_in_labels)):
        sheet.write(0, labels, array_in_labels[labels], cell_format_header)
        sheet.write(0, labels+len(array_in_labels), array_out_labels[labels], cell_format_header)
    for rows in range(len(array_in_master[y])):
        sheet.write_row((rows+1), 0, array_in_master[y,rows,:], cell_format_in) # writing input array to sheet for respective component
    for rows in range(len(array_out_master[y])):
        sheet.write_row((rows+1), len(array_in_labels), array_out_master[y,rows,:], cell_format_out) # writing input array to sheet for respective component

H2_compressor_data.close()

#---------------------------------------
# Compile component specific data collection for desired outputs (polarization curves, H2 production, etc.)

# # 1) AEZ_stack  
# # A) Polarization curve to look at overpotentials at one specifc steady-state temperature:
# if len(current_range) == 1: # checks to see if you are solving for only 1 current density
#     fig, ax1 = plt.subplots(); #fig.tight_layout(pad=1.5)
#     labels = ['U_cell', 'U_rev', 'U_act', 'U_ohm', 'theta']
#     T_op_range = T_list_stack; #print('T_list = ', T_list) # [K] steady state operating temperature range
#     i_start_pol = 0.001; i_end_pol = 0.6; i_step_pol = 0.001; i_range_pol = np.arange(i_start_pol, (i_end_pol + i_step_pol), i_step_pol) #[A/cm^2] current density range
#     U_cell_master = np.empty((0,len(i_range_pol),len(labels)))
#     U_cell_store = np.empty((0,len(labels)))
#     T_op = T_op_range[0]
#     T_op_C = T_op - 273.15; T_op_C = round(T_op_C,2)
#     for z in range(len(i_range_pol)):
#         i = i_range_pol[z]
#         U_cell_array = U_cell(w, P_op_bar, component_inputs(components_list[0], components_list[0])[0].T, T_op, i, model); #print(U_cell_array)
#         U_cell_store = np.append(U_cell_store, np.array([U_cell_array]), axis =0)
#     U_cell_master = np.append(U_cell_master, np.array([U_cell_store]), axis =0)
#     ax1.set_title('Unit Cell Polarization Curve'); 
#     ax1.set_xlabel('Current Density [A/cm^2]'); ax1.set_ylabel('Cell Voltage [V]')
#     ax1.plot(i_range_pol, U_cell_master[0,:,0], color = 'red', label = labels[0])
#     ax1.plot(i_range_pol, U_cell_master[0,:,1], color ='blue', label = labels[1])
#     ax1.tick_params(axis='y'); plt.legend(loc='upper left')
#     ax2 = ax1.twinx(); ax2.set_ylabel('Overpotentials [V]')
#     ax2.plot(i_range_pol, U_cell_master[0,:,2], color ='green', label = labels[2])
#     ax2.plot(i_range_pol, U_cell_master[0,:,3], color = 'orange', label = labels[3])
#     ax2.tick_params(axis='y'); plt.legend(loc='upper right')
# # B) Polarization curve to look at all steady-state temperature for a range of current densities:
# elif len(current_range) > 1 :
#     fig, ax1 = plt.subplots();
#     labels = ['U_cell', 'U_rev', 'U_act', 'U_ohm', 'theta']
#     T_op_range = T_list_stack; #print('T_list = ', T_list_stack) # [K] steady state operating temperature range
#     i_start_pol = 0.001; i_end_pol = 0.6; i_step_pol = 0.001; i_range_pol = np.arange(i_start_pol, (i_end_pol + i_step_pol), i_step_pol) #[A/cm^2] current density range
#     U_cell_master = np.empty((0,len(i_range_pol),len(labels)))
#     for y in range(len(T_op_range)):
#         U_cell_store = np.empty((0,len(labels)))
#         T_op = T_op_range[y]
#         T_op_C = T_op - 273.15; T_op_C = round(T_op_C,2)
#         for z in range(len(i_range_pol)):
#             i = i_range_pol[z]
#             U_cell_array = U_cell(w, P_op_bar, component_inputs(components_list[0], components_list[0])[0].T, T_op, i, model); #print(U_cell_array)
#             U_cell_store = np.append(U_cell_store, np.array([U_cell_array]), axis =0)
#         U_cell_master = np.append(U_cell_master, np.array([U_cell_store]), axis =0)
#         ax1.set_title('Unit Cell Polarization Curve'); 
#         ax1.set_xlabel('Current Density [A/cm^2]'); ax1.set_ylabel('Cell Voltage [V]')
#         ax1.plot(i_range_pol, U_cell_master[y,:,0], color = (np.random.random(), np.random.random(), np.random.random()), label = (str(T_op_C) + 'deg C'))
#         plt.legend(loc='lower right')

#---------------------------------------
print('H2_compressor_data.py has finished running.'); print('')