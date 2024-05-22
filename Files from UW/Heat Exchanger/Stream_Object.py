# -*- coding: utf-8 -*-
"""
Created on Thur May  16 7:59:00 2024

@author: erich
"""

import numpy as np
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary
import os
from scipy.optimize import root

class Stream:
    """
    Stream object which organizes data handling and specifies mixing rules. This is meant for mixtures which REFPROP cannot recieve on its own, such as any mixtures with hydrogen. 
    As of 5/22/24, the mixing rules defined in this object are all ideal mixing with the properties of each species determined through REFPROP.

    Attributes:
        fluids : list{str}
            list of FluidIDs as defined by REFPROP documentation. The order must match the order of the next attribute, m
        m : np.array{float}
            numpy array of the molar flow rates of each species in the mixture in mol/s
        H : float
            enthalpy of the mixture in J/mol
        P : float
            pressure of the mixture in MPa
            
    Methods:
        calc_temp()
            internal method used for temperature calculation
        Standard_calc()
            internal method used for parameter calculations other than temperature
        __getattr__(attr)
            allows for the user to call the following list of thermodynamic properties:
                T : temperature
                CP : isobaric heat capacity
                CV : isochoric heat capacity
                CPCV : heat capacity ratio
                S : entropy
                E : internal energy
                Z : compressibility factor
                JT : isenthalpic joule-thomson coefficient
                G : gibbs energy
                R : gas constant
                VIS : viscosity
                MM : molar mass of the mixture
                MMi : numpy array of molar masses of each species in the mixture
            if the property called has not been called before, it will be calculated and returned. If it has been called before, it will be retrieved from memory.
        calc_[attribute here]()
            these functions force a recalculation of an attribute of the mixture. Useful when mutating the base attributes of a Stream object instead of creating a new object, which is commonly faster in numerical solvers
    """
    
    def __init__(self,fluids,m,H,P):
        self.fluids = fluids
        self.m = m
        self.H = H
        self.P = P
        
    def calc_temp(self):
        def temp_eq(T):
            #gets mole fractions, unitless
            molf = self.m/np.sum(self.m)
            
            #finds partial pressures
            pp = self.P*molf
            
            #instantiates refprop
            os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
            RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
            RP.SETPATHdll(os.environ['RPPREFIX'])
            unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
                
            index = list(range(len(self.fluids)))
            func = lambda fluid, i: molf[i]*RP.REFPROPdll(fluid,'TP','H',unit,1,0,T,pp[i],[1]).Output[0]
            Hs = np.fromiter(map(func, self.fluids, index),dtype=float)
            
            #defines equation for solver
            eq = np.sum(Hs) - self.H
            return eq

        def temp_calc():
            #runs solver for temperature calculation
            sol = root(temp_eq,500)
            return sol.x[0]
        
        self.T = temp_calc()
        return self.T
    
    def Standard_calc(self,Out):
        #gets mole fractions, unitless
        molf = self.m/np.sum(self.m)
        
        #finds partial pressures
        pp = self.P*molf
        
        try:
            T = self.T
        except:
            T = self.calc_temp()
        
        #instantiates refprop
        os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
        RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
        RP.SETPATHdll(os.environ['RPPREFIX'])
        unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
        
        #gets weighted individual species values
        index = list(range(len(self.fluids)))
        func = lambda fluid, i: molf[i]*RP.REFPROPdll(fluid,'TP',Out,unit,1,0,T,pp[i],[1]).Output[0]
        currs = np.fromiter(map(func, self.fluids, index),dtype=float)
        
        #returns mixture property
        return np.sum(currs)
    
    def __getattr__(self,attr):
        if attr == 'T':
            def temp_eq(T):
                #gets mole fractions, unitless
                molf = self.m/np.sum(self.m)
                
                #finds partial pressures
                pp = self.P*molf
                
                #instantiates refprop
                os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
                RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
                RP.SETPATHdll(os.environ['RPPREFIX'])
                unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
                    
                index = list(range(len(self.fluids)))
                func = lambda fluid, i: molf[i]*RP.REFPROPdll(fluid,'TP','H',unit,1,0,T,pp[i],[1]).Output[0]
                Hs = np.fromiter(map(func, self.fluids, index),dtype=float)
                
                #defines equation for solver
                eq = np.sum(Hs) - self.H
                return eq

            def temp_calc():
                #runs solver for temperature calculation
                sol = root(temp_eq,500)
                return sol.x[0]
            
            self.T = temp_calc()
        elif attr == 'CP':
            self.CP = self.Standard_calc('CP')
        elif attr == 'CV':
            self.CV = self.Standard_calc('CV')
        elif attr == 'CPCV':
            self.CPCV = self.CP/self.CV
        elif attr == 'S':
            self.S = self.Standard_calc('S')
        elif attr == 'E':
            self.E = self.Standard_calc('E')
        elif attr == 'Z':
            self.Z = self.Standard_calc('Z')
        elif attr == 'JT':
            self.JT = self.Standard_calc('JT')
        elif attr == 'G':
            self.G = self.Standard_calc('G')
        elif attr == 'R':
            self.R = self.Standard_calc('R')
        elif attr == 'VIS':
            self.VIS = self.Standard_calc('VIS')
        elif attr == 'MM':
            #gets mole fractions, unitless
            molf = self.m/np.sum(self.m)
            
            #instantiates refprop
            os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
            RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
            RP.SETPATHdll(os.environ['RPPREFIX'])
            unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
            
            #gets weighted individual species values
            index = list(range(len(self.fluids)))
            func = lambda fluid, i: molf[i]*RP.REFPROPdll(fluid,'TP','M',unit,1,0,300,0.1,[1]).Output[0]
            MM = np.fromiter(map(func, self.fluids, index),dtype=float)
            self.MM = np.sum(MM)
        elif attr == 'MMi':
            #instantiates refprop
            os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
            RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
            RP.SETPATHdll(os.environ['RPPREFIX'])
            unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
            
            #gets weighted individual species values
            index = list(range(len(self.fluids)))
            func = lambda fluid, i: RP.REFPROPdll(fluid,'TP','M',unit,1,0,300,0.1,[1]).Output[0]
            MMi = np.fromiter(map(func, self.fluids, index),dtype=float)
            self.MMi = MMi
        return super(Stream,self).__getattribute__(attr)
    
    def calc_CP(self):
        self.CP = self.Standard_calc('CP')
        return self.CP
        
    def calc_CV(self):
        self.CV = self.Standard_calc('CV')
        return self.CV
    
    def calc_CPCV(self):
        try:
            cp = self.CP
        except:
            cp = self.calc_CP()
        try:
            cv = self.CV
        except:
            cv = self.calc_CV()
        return cp/cv
    
    def calc_S(self):
        self.S = self.Standard_calc('S')
        return self.S
    
    def calc_E(self):
        self.E = self.Standard_calc('E')
        return self.E
    
    def calc_Z(self):
        self.Z = self.Standard_calc('Z')
        return self.Z
    
    def calc_JT(self):
        self.JT = self.Standard_calc('JT')
        return self.JT
    
    def calc_G(self):
        self.G = self.Standard_calc('G')
        return self.G
    
    def calc_R(self):
        self.R = self.Standard_calc('R')
        return self.R
    
    def calc_MM(self):
        #gets mole fractions, unitless
        molf = self.m/np.sum(self.m)
        
        #instantiates refprop
        os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
        RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
        RP.SETPATHdll(os.environ['RPPREFIX'])
        unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
        
        #gets weighted individual species values
        index = list(range(len(self.fluids)))
        func = lambda fluid, i: molf[i]*RP.REFPROPdll(fluid,'TP','M',unit,1,0,300,0.1,[1]).Output[0]
        MM = np.fromiter(map(func, self.fluids, index),dtype=float)
        self.MM = np.sum(MM)
        return self.MM
    
    def calc_MMi(self):
        #instantiates refprop
        os.environ['RPPREFIX'] = r'C:/Program Files (x86)/REFPROP'
        RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
        RP.SETPATHdll(os.environ['RPPREFIX'])
        unit = RP.GETENUMdll(0, 'MOLAR SI')[0]
        
        #gets weighted individual species values
        index = list(range(len(self.fluids)))
        func = lambda fluid, i: RP.REFPROPdll(fluid,'TP','M',unit,1,0,300,0.1,[1]).Output[0]
        MMi = np.fromiter(map(func, self.fluids, index),dtype=float)
        self.MMi = MMi
        return self.MMi
    