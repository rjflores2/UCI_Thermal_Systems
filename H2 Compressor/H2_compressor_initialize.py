# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:11:41 2023

@author: rhl
"""

#---------------------------------------
# Loops to run chosen components
# Runs models at only 1 value of chosen physical parameter
if len(chosen_parameter_range) == 1: # checks to see if you are solving for only 1 current density
    # Defining storage matrices for 1 currenty densitiy
    sheets = len(components_list); rows_in = np.sum(streams[0]); rows_out = np.sum(streams[1]); columns = len(array_in[0]); # defining dimensions for 3D matrices for storage
    array_in_master = np.zeros((sheets, rows_in, columns)) # Indexes: component #, row #, column value (row # is total amount of inlet streams) 
    array_out_master = np.zeros((sheets, rows_out, columns)) # Indexes: component #, row #, column value (row # is total amount of outlet streams)
    # Initial solving of first component to populate storage arrays and input/output streams
    parameter_value = chosen_parameter_range[0]; #print(parameter_value)
    component = components_list[0]
    streams_out = []
    for z in range(len(streams[3,0])):
        streams_out.append(Stream(streams[3,0][z],0,0,0,0,0,0,0,0,0,0))
    os.chdir(components_folders_list[0]) # changing current working directory (folder) for the relevant component being solved
    exec(open(component).read())
    os.chdir(path_subsystem) # changing current working directory (folder) back to AEZ folder to execute other components, path is defined in AEZ_input
    print(component+ ' has finished running.'); print(' ')
    array_in = class2array((streams_in[0]), (streams_in))
    array_in_master[0, 0:streams[0,0], :] = array_in; #print(array_in_master[0, x:(x+components_list[1][0]), :])
    array_out = class2array(streams_out[0], streams_out)
    array_out_master[0, 0:streams[1,0], :] = array_out
    if len(components_list) > 1: # conditional statement to check if multiple components are to be solved
        # Loop iteration for each component of components_list after first component
        for y in range(1,len(components_list)): # starting index 1 of components_list because first component of components_list was already solved
            streams_in =[]; # redefining streams_in list to be empty to store the outputs from previous component
            component = components_list[y]; c = y; 
            for z in range(len(streams[2,y])):
                streams_in.append(Stream(streams[2,y][z],c,0,0,0,0,0,0,0,0,0))
            for index_s_out in range(len(streams_out)): # for each outlet stream (starting at first component) 
                stream = streams_out[index_s_out]
                if stream.s in streams[2,y]: # conditional statement checking to see if any outlet stream tags from first component are the same as inlet stream tags in next component
                    stream_in = streams_out[index_s_out]
                    stream_in.c = c
                    for stream_index in range(len(streams_in)):
                        stream = streams_in[stream_index]
                        if stream_in.s == stream.s:
                            streams_in[stream_index] = stream_in
                    array_in = class2array(streams_in[0], streams_in)
                    array_in_master[y, 0:streams[0,y], :] = array_in;
                else:
                    print('Stream ' + str(stream.s) + ' is not an input into ' + str(component)); print('')
            streams_in_temporary = streams_in
            component = components_list[y]
            for b in range(len(streams_in)):
                stream = streams_in[b]
                if stream.T==0 and stream.P==0 and stream.N==0:
                    streams_in = component_inputs('empty', component)['Inlet streams']
                    stream = streams_in[b]
                    streams_in = streams_in_temporary
                    streams_in[b] = stream
            array_in = class2array(streams_in[0], streams_in); #print(array_in)
            array_in_master[y, 0:streams[0,y], :] = array_in;
            streams_out = [] # redefining empty list to store the outputs of the next component
            for z in range(len(streams[3,y])):
                streams_out.append(Stream(streams[3,y][z],c,0,0,0,0,0,0,0,0,0))
            os.chdir(components_folders_list[y]); #print(os.getcwd()) # changing current working directory (folder) for the relevant component being solved
            exec(open(component, encoding='utf-8').read()) 
            os.chdir(path_subsystem); #print(os.getcwd()) # changing current working directory (folder) back to AEZ folder to execute other components, path is defined in AEZ_input
            print(component+ ' has finished running.'); print('')
            array_out = class2array(streams_out[0], streams_out)
            array_out_master[y,0:(streams[1][y]),:] = array_out; #print(array_out_master) # storing output of current component
            
# Run models over a range of chosen physical parameter
elif len(chosen_parameter_range) > 1 :
    # Defining storage matrices for a range of chosen parameter values
    sheets = len(components_list)+1; rows_in = len(chosen_parameter_range)*np.sum(streams[0]); rows_out = len(chosen_parameter_range)*np.sum(streams[1]); columns = len(array_in[0]); # defining dimensions for 3D matrices for storage
    array_in_master = np.zeros((sheets, rows_in, columns)) # Indexes: component #, row #, column value (row # is total amount of inlet streams) 
    array_out_master = np.zeros((sheets, rows_out, columns)) # Indexes: component #, row #, column value (row # is total amount of outlet streams)
    # Solving over a range of current densities
    for x in range(len(chosen_parameter_range)): # runs if you are solving over a range of current densities
        parameter_value = chosen_parameter_range[x]; 
        streams_in = streams_in_start # redefines starting streams to be starting values (defined in input file)
        # Solving over a range of components
        for y in range(len(components_list)):
            component = components_list[y]; c = y;
            for stream in streams_in:
                stream.c = c
            streams_out = []
            for z in range(len(streams[3,y])):
                streams_out.append(Stream(streams[3,y][z],c,0,0,0,0,0,0,0,0,0))
            os.chdir(components_folders_list[y]); #print(os.getcwd()) # changing current working directory (folder) for the relevant component being solved
            exec(open(component, encoding='utf-8').read()); 
            os.chdir(path_subsystem); #print(os.getcwd()) # changing current working directory (folder) back to AEZ folder to execute other components, path is defined in AEZ_input
            print(component+ ' has finished running.'); print('')
            array_in = class2array(streams_in[0], streams_in); #print(array_in)
            if len(array_in) == streams[0,y]: 
                array_in_master[y, (x*streams[0,y]):(x*streams[0,y]+streams[0,y]), :] = array_in; 
            array_out = class2array(streams_out[0], streams_out)
            array_out_master[y, (x*streams[1,y]):(x*streams[1,y]+streams[1,y]), :] = array_out
            if y+1 == len(components_list): # checks to see if last component has been solved
                break 
            streams_in =[]
            for z in range(len(streams[2,y+1])):
                streams_in.append(Stream(streams[2,y+1][z],c,0,0,0,0,0,0,0,0,0))
            for index_s_out in range(len(streams_out)): # for each outlet stream (starting at first component) 
                stream = streams_out[index_s_out]
                if stream.s in streams[2,y+1]:
                    stream_in = streams_out[index_s_out]
                    stream_in.c = c+1
                    for stream_index in range(len(streams_in)):
                        stream = streams_in[stream_index]
                        if stream_in.s == stream.s:
                            streams_in[stream_index] = stream_in
                else:
                    print('Stream ' + str(stream.s) + ' is not an input into ' + str(components_list[y+1])); print('')
            streams_in_temporary = streams_in
            component = components_list[y+1]
            for b in range(len(streams_in)):
                stream = streams_in[b]
                if stream.T==0 and stream.P==0 and stream.N==0:
                    streams_in = component_inputs('empty', component)['Inlet streams']
                    stream = streams_in[b]
                    streams_in = streams_in_temporary
                    streams_in[b] = stream
            array_in = class2array(streams_in[0], streams_in); #print(array_in)
else: 
    raise Exception('Invalid physical parameter range/value selected. Length of chosen_parameter_range must be equal to or greater than 1. Please check temp_in_range.')

#---------------------------------------
print('H2_compressor_initialize.py has finished running.'); print('')