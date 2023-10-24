# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:30:14 2023

@author: labuser-fc
"""
#latent heat of condensation as a function of temperature

#initialize a hot temperature
import CoolProp.CoolProp as CP;

def heat_ex(amb_pres,f1,f2,f3,f4,f5,f6,Ti1,Ti2,Te1,Te2,m1):
# MR1 MR2, H2
#MR1 is composed of 7.2% N2, 24.8% CH4, 32.4% C2H4(Ethylene), 18.5% C3H8(Propane) and 17.1% i-C5H12(Isopentane)

#MR2 consists of 10% H2 and 90% Ne

#MR3 is made up of 12.4% H2, 5.0% Ne and 82.6% He.


    Hi1 = CP.PropsSI('H', 'T', Ti1, 'P', amb_pres, f1)
    Hi2 = CP.PropsSI('H', 'T', Ti2, 'P', amb_pres, f2)
    Hi3 = CP.PropsSI('H', 'T', Ti2, 'P', amb_pres, f3)
    Hi4 = CP.PropsSI('H', 'T', Ti2, 'P', amb_pres, f4)
    Hi5 = CP.PropsSI('H', 'T', Ti2, 'P', amb_pres, f5)
    Hi6 = CP.PropsSI('H', 'T', Ti2, 'P', amb_pres, f6)
    He1 = CP.PropsSI('H', 'T', Te1, 'P', amb_pres, f1)
    He2 = CP.PropsSI('H', 'T', Te2, 'P', amb_pres, f2)
    He3 = CP.PropsSI('H', 'T', Te2, 'P', amb_pres, f3)
    He4 = CP.PropsSI('H', 'T', Te2, 'P', amb_pres, f4)
    He5 = CP.PropsSI('H', 'T', Te2, 'P', amb_pres, f5)
    He6 = CP.PropsSI('H', 'T', Te2, 'P', amb_pres, f6)
    
    print('m1',m1)
    # for solving mr2
    # assume x = 1 mol out of 100, 7.2 would be N2, 24.8 would be CH4 and so on
    # multiplier y will be applied to the mr2
    eff = 1
    
    #m1*(Hi1-He1) = 7.2 * x * Hi2 + 24.8 * x * Hi3 + 32.4 * x * Hi4 + 18.5 * x * Hi5 + 17.1 * x * Hi6
    x = m1*(Hi1-He1)/(7.2 * He2 * 28 + 24.8 * He3 * 16 + 32.4 * He4 * 28 + 18.5 * He5 * 44 + 17.1 * He6 * 72 -
        (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72))
    m2 = 7.2 * x * 28 + 24.8 * x * 16 + 32.4 * x * 28 + 18.5 * x * 44 + 17.1 * x * 72
    return(m2,m2/m1)

m2,ratio = heat_ex(101325,'Hydrogen','N2','Methane','Ethylene','Propane','Isopentane',338,113,130,129,0.00520833333)
print(m2,ratio)
print(m2*3600*24)

H2 = CP.PropsSI('C','T',113,'P',101325,'H2')
Hi2 = CP.PropsSI('C', 'T', 113, 'P', 101325, 'N2')
Hi3 = CP.PropsSI('C', 'T', 113, 'P', 101325, 'Methane')
Hi4 = CP.PropsSI('C', 'T', 113, 'P', 101325, 'Ethylene')
Hi5 = CP.PropsSI('C', 'T', 113, 'P', 101325, 'Propane')
Hi6 = CP.PropsSI('C', 'T', 113, 'P', 101325, 'Isopentane')
print(Hi2,Hi3,Hi4,Hi5,Hi6)
mix = (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72)/(7.2 * 28 + 24.8 * 16 + 32.4 * 28 + 18.5 * 44 + 17.1 * 72)
print(H2,mix)