# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:16:59 2023

@author: rhl
"""
plt.close('all'); plt.rcParams['font.size'] = '14'; 

# Configure sub-system data collection for excel file. Update array_in/out labels based on species that can be added/removed to the Stream class.
array_labels = ['stream #', 'model #', 'T [K]', 'P [Pa]','N [mol/s]', 'x_KOH', 'x_H2O_l', 'x_H2O_v', 'x_H2', 'x_O2','x_N2']

# Create input/output dataframes to easier access data then write to csv/excel
df_in =[]; df_out = []
for x in range(len(chosen_parameter_range)):
    for y in range(loop_count):
        for z in range(len(components_list)):
            array_in = array_in_master[x][y][z]; #print(array_in)
            array_in = pd.DataFrame(array_in, columns = array_labels); 
            df_in.append(array_in)
            array_out = array_out_master[x][y][z]; #print(array_out)
            array_out = pd.DataFrame(array_out, columns = array_labels)
            df_out.append(array_out)
df_in = pd.concat(df_in, ignore_index = True); #print(df_in)
df_out = pd.concat(df_out, ignore_index = True); #print(df_out)
with pd.ExcelWriter('H2 Compressor Data.xlsx') as writer:
    df_in.to_excel(writer, sheet_name='Arrays In', index =False)
    df_out.to_excel(writer, sheet_name='Arrays Out', index =False)
    
# Compile component specific data collection for desired outputs
all_parameter_work = []
all_parameter_head_heat = []
all_parameter_HX_heat = []
total_scenarios = len(chosen_parameter_range)*loop_count; #print(total_scenarios)
for scenario in range(total_scenarios)[::loop_count]: 
    total_work_scenario = sum(parameter_work[scenario:(scenario+loop_count)]) # [W] summing the theoretical work of each each stage for each inputted parameter
    all_parameter_work.append(total_work_scenario)
    total_heat_head_scenario = sum(parameter_heat_head[scenario:(scenario+loop_count)])
    all_parameter_head_heat.append(total_heat_head_scenario)
    # total_heat_HX_scenario = sum(parameter_heat_HX[scenario:(scenario+loop_count)])
    # all_parameter_HX_heat.append(total_heat_HX_scenario)

#---------------------------------------
# Format plots of desired outputs
# Compressor work
fig, (ax1) = plt.subplots(1)
ax1.set_title('Theoretical Compressor Work')
ax1.set_xlabel(chosen_parameter_name)
ax1.set_ylabel('Work [W]')
ax1.plot(chosen_parameter_range,all_parameter_work)

# Compressor heat rejection
fig, (ax1) = plt.subplots(1)
ax1.set_title('Theoretical Compressor Heat Rejection')
ax1.set_xlabel(chosen_parameter_name)
ax1.set_ylabel('Heat Rejection Rate [W]')
ax1.plot(chosen_parameter_range,all_parameter_head_heat)

#---------------------------------------
print('H2_compressor_data.py has finished running.'); print('')