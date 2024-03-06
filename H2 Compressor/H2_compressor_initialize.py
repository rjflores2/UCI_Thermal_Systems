# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:11:41 2023

@author: rhl
"""

# Input checks
if component_loops is False:
    loop_count = 1
elif component_loops is True:
    try: loop_parameter
    except NameError: loop_parameter = None
    if loop_parameter is None:
        raise Exception('Input variable loop_parameter is not defined while component_loops is True. Please set component_loops to false or define loop_parameter.')
    else:
        loop_count = all_component_inputs[loop_parameter]
if len(chosen_parameter_range) < 1:
    raise Exception('Invalid physical parameter range/value selected. Length of chosen_parameter_range must be equal to or greater than 1. Please check chosen_parameter_range.')       

#---------------------------------------
# Defining storage lists for a range of chosen parameter values
array_in_components = []; array_out_components = []
array_in_loops = []; array_out_loops = []
array_in_parameters = []; array_out_parameters = []

# Solving over a range of chosen parameter values
for x in range(len(chosen_parameter_range)): # runs if you are solving over a range of chosen parameter values
    parameter_value = chosen_parameter_range[x]; 
    streams_in = streams_in_start # redefines starting streams to be starting values (defined in input file)
    array_in_loops.clear(); array_out_loops.clear()
    for loop in range(1,loop_count+1):
        loop_props = all_component_inputs['Properties'][loop]
        l = loop -1
        if loop > 1:
            parameter_value = streams_out[0].T
            streams_in = streams_in_start
        array_in_components.clear(); array_out_components.clear()
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
                array_in_components.append(array_in); #print(array_in_components)
            else:
                raise Exception('Mismatch between expected amount of inlet streams and actual amount of inlet streams. Check array_in')
            array_out = class2array(streams_out[0], streams_out)
            array_out_components.append(array_out)
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
        array_in_loops.append(array_in_components.copy())
        array_out_loops.append(array_out_components.copy())
        if loop_parameter is not None:
            print(str(loop_parameter)+ ' '+ str(loop)+ ' has finished running.'); print('')
    array_in_parameters.append(array_in_loops.copy())
    array_out_parameters.append(array_out_loops.copy())
array_in_master = array_in_parameters; #print('in = ', array_in_master)
array_out_master = array_out_parameters; #print('out = ', array_out_master)  

#---------------------------------------
print('H2_compressor_initialize.py has finished running.'); print('')