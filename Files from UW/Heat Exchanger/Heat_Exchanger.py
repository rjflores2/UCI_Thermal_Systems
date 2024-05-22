# -*- coding: utf-8 -*-
"""
Created on Sun May  12 6:00:00 2024

@author: erich
"""

import numpy as np
from scipy.optimize import root
from math import log as mlog
from Stream_Object import Stream

"""
Governing Equations:
ṁhot(Ĥin,hot - Ĥout,hot) = ṁcold(Ĥout,cold - Ĥin,cold) = UAΔTlm
ΔTlm = ((Tin,hot - Tout,cold) - (Tout,hot - Tin,cold))/ ln((Tin,hot - Tout,cold)/ (Tout,hot - Tin,cold))
"""

def Heat_Exchanger(hot_stream_in,cold_stream_in,U,A):
    """
    Enthalpy-Based Two Flow Heat Exchanger

    Dependencies:
        Base Python Libraries:
            math
        Conda-forge Libraries:
            numpy
            scipy
        Custom Files:
            Stream_Object.py must be in the same directory as this file as of 5/22/24. Future updates will wrap these modules into a common package for distribution. For more information on the Stream object, see Stream_Object.py

    Parameters:
        hot_stream_in : Stream_Object.Stream
            specifies the input conditions of the hot stream
        cold_stream_in : Stream_Object.Stream
            specifies the input conditions of the cold stream
        U : float 
            heat exchanger effectiveness coefficient as of 5/22/24. In a future update, this will be calculated from the convective heat transfer coefficient of the two streams, and this parameter will instead become some heat exchanger geometry parameter, likely the wall thickness
        A : float
            heat exchange area

    Returns:
        hot_stream_out : Stream_Object.Stream
            output stream of the hot side
        cold_stream_out : Stream_Object.Stream
            output stream of the cold side
    """
    
    init_guess = [hot_stream_in.H*0.9,cold_stream_in.H*1.1]
    
    hot_stream_out = Stream(hot_stream_in.fluids,hot_stream_in.m,init_guess[0],hot_stream_in.P)
    cold_stream_out = Stream(cold_stream_in.fluids,cold_stream_in.m,init_guess[1],cold_stream_in.P)
    
    data = (hot_stream_in,cold_stream_in,hot_stream_out,cold_stream_out,U,A)
    
    sol = root(funcs,init_guess,args=data)
    
    #creates output stream objects
    hot_stream_out.H = sol.x[0]
    cold_stream_out.H = sol.x[1]
    
    return hot_stream_out, cold_stream_out

#function for log mean temp calculation
def dT_lm(hot_stream_in,hot_stream_out,cold_stream_in,cold_stream_out):
    #gets temperatures at the outlets from function above
    hot_stream_out.calc_temp()
    cold_stream_out.calc_temp()
     
    #sets numerator and denominator for log mean temp calculation
    numer = (hot_stream_in.T - cold_stream_out.T) - (hot_stream_out.T - cold_stream_in.T)
    denom = mlog((hot_stream_in.T - cold_stream_out.T)/(hot_stream_out.T - cold_stream_in.T))
    
    #returns log mean temp
    return numer/denom

def funcs(Houts,*data):
    #pulls variables to solve
    Hout_hot, Hout_cold = Houts
    #pulls input conditions and parameters
    hot_stream_in, cold_stream_in, hot_stream_out, cold_stream_out, U, A = data
    #creates output stream objects
    hot_stream_out.H = Hout_hot
    cold_stream_out.H = Hout_cold
    
    #defines equations. Each equals zero, as that is the necesarry format for a root finding solver
    eq1 = np.sum(hot_stream_in.m)*(hot_stream_in.H - hot_stream_out.H) - U*A*dT_lm(hot_stream_in,hot_stream_out,cold_stream_in,cold_stream_out)
    eq2 = np.sum(cold_stream_in.m)*(cold_stream_out.H - cold_stream_in.H) - U*A*dT_lm(hot_stream_in,hot_stream_out,cold_stream_in,cold_stream_out)
    
    #returns equations
    return [eq1, eq2]