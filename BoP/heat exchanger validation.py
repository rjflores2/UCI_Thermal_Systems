# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:30:14 2023

@author: labuser-fc
"""
#latent heat of condensation as a function of temperature

#initialize a hot temperature
import CoolProp.CoolProp as CP;

def heat_ex(Th1,Tc1,Th2,Tc2,Ph1,Pc1,Ph2,Pc2,m2):
# MR1 MR2, H2
#Enthalpy [J/kg]
#Enthalpy of Vap for Hydrogen 446.4 J/g = 446400J/kg

    H_H2_vap = 446400

#hot stream enthalpy    
    Hh_Hy = CP.PropsSI('H', 'T', Th1, 'P', Ph1, 'Hydrogen')
#mr2    
    Hh_Ni_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Nitrogen')   #11.8       15.9
    Hh_Me_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Methane')    #6.6        6.2
    Hh_Et_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Ethane')   #19.4       17.2
    Hh_Pr_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Propane')  #11.8       11
    
#cold stream enthalpy    
    Hc_Hy = CP.PropsSI('H', 'T', Tc1, 'P', Pc1, 'Hydrogen')
#mr2    
    Hc_Ni_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Nitrogen')   #11.8       15.9
    Hc_Me_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Methane')    #6.6        6.2
    Hc_Et_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Ethane')   #19.4       17.2
    Hc_Pr_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Propane')  #11.8       11   
    
    '''
    print('Hi1',Hi1)
    # for solving mr2
    # assume x = 1 mol out of 100, 7.2 would be N2, 24.8 would be CH4 and so on
    # multiplier y will be applied to the mr2
    eff = 1
    
    #m1*(Hi1-He1) = 7.2 * x * Hi2 + 24.8 * x * Hi3 + 32.4 * x * Hi4 + 18.5 * x * Hi5 + 17.1 * x * Hi6
    if Te1 > 20:
        x = m1*(Hi1-He1)
    else:
        x = m1*(Hi1-He1+H_H2_vap) 
# boiling point:
# N2 77.36  Propane: 85.52 Isopentane: 113.25        
    if Te2 > 77.36:
        n2 = (7.2 * He2 * 28 + 24.8 * He3 * 16 + 32.4 * He4 * 28 + 18.5 * He5 * 44 + 17.1 * He6 * 72 -
                          (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72))
    elif Te2>30:
        n2 = (7.2 * He2 * 28 + 24.8 * He3 * 16 + 32.4 * He4 * 28 + 18.5 * He5 * 44 + 17.1 * He6 * 72 -
                          (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72))
        
    x = Q1/n2
    '''
    # calculate the each individual heat exchange from streams using temperature/enthalpy change and mass flow change
    # Figure out how much mass flow is in each stream.
    # solving for individual mass flow rate percentage for the mix refrigerant
    
    total = 0.2*14 + 94.4*16 + 3.9*30 + 1*44.1
    # Nitrogen
    pmnitrogen = 0.2*14 / total
    pmmethane = 94.4*16 / total
    pmethne = 3.9*30 / total
    pmpropane = 44.1 / total
    #print('%%%%%',pmpentane,pmb,pmpropane,pmethylene,pmethane,pmm,pmnitrogen,pmneon,pmr)
    #testing
    h2 = pmnitrogen * (Hh_Ni_2-Hc_Ni_2)+ pmmethane * (Hh_Me_2-Hc_Me_2) + pmethne * (Hh_Et_2-Hc_Et_2) + pmpropane * (Hh_Pr_2-Hc_Pr_2) 
    print('h2h343434343',h2)
    #print(pmpentane * (Hh_Pe_2-Hc_Pe_2)+ pmb * (Hh_Bu_2-Hc_Bu_2) + pmpropane * (Hh_Pr_2-Hc_Pr_2) + pmethylene * (Hh_Ethy_2-Hc_Ethy_2),'\n 4',
    #      pmpentane * (Hh_Pe_4-Hc_Pe_4)+ pmb * (Hh_Bu_4-Hc_Bu_4) + pmpropane * (Hh_Pr_4-Hc_Pr_4) + pmethylene * (Hh_Ethy_4-Hc_Ethy_4))
    
    
    
    
    
    
    Q2 = m2 * h2
    #x =  m1*(Hi1-He1)/(11.8 * Hh_Pe_3 * 72.15 + 6.6 * He3 * 52.18 + 19.4 * He4 * 44.097 + 11.8 * He5 * 28.05 + 8.6 * He6 * 30.07 + 16.6 * He7 * 16.04 + 15.6 * He8 * 14 + 2.4 * He9 * 20.18 + 7.2 * He10 * 88 -
    #                  (11.8 * Hi2 * 72.15 + 6.6 * Hi3 * 52.18 + 19.4 * Hi4 * 44.097 + 11.8 * Hi5 * 28.05 + 8.6 * Hi6 * 30.07 + 16.6 * Hi7 * 16.04 + 15.6 * Hi8 * 14 + 2.4 * Hi9 * 20.18 + 7.2 * Hi10 * 88))
    print('Q2Q3Q4:',Q2)
    m1 = (Q2)/(Hh_Hy-Hc_Hy)        
    #m2 = 7.2 * x * 28 + 24.8 * x * 16 + 32.4 * x * 28 + 18.5 * x * 44 + 17.1 * x * 72
    return(m1)

#m2,ratio = heat_ex(101325,298,120,140,139,18.78)
#def heat_ex(amb_pres,Th1,Tc1,Th2,Tc2,Th3,Tc3,Th4,Tc4,m2,m3,m4):
#m1 =  heat_ex(310,255,310,255,310,255,304,235.7,8000000,7870000,2480000,2440000,2480000,2440000,110000,110000,20.05,9.32,29.37)

#m2 =  heat_ex(255,235,255,235,255,235,235.7,224.7,7870000,7750000,2440000,2400000,2440000,2400000,110000,120000,12.81,7.24,29.37)
m1 = heat_ex(300,131,299,110,2000000,1970000,1900000,1870000,40640)
print('results for 1!!!!!!',m1,'results for 2!!!!!!!!')




### heat exchanger for the subcooled systems, using neon and helium
def heat_ex_cyro(Th1,Tc1,Th2,Tc2,Ph1,Pc1,Ph2,Pc2,m2):
# MR1 MR2, H2
#Enthalpy [J/kg]
#Enthalpy of Vap for Hydrogen 446.4 J/g = 446400J/kg

#    H_H2_vap = 446400

#hot stream enthalpy    
    Hh_Hy = CP.PropsSI('H', 'T', Th1, 'P', Ph1, 'Hydrogen')
#mr2    
    Hh_Hy_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Hydrogen')   #11.8       15.9
    Hh_He_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Helium')    #6.6        6.2
    Hh_Ne_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Neon')   #19.4       17.2
    
#cold stream enthalpy    
    Hc_Hy = CP.PropsSI('H', 'T', Tc1, 'P', Pc1, 'Hydrogen')
#mr2    
    Hc_Hy_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Hydrogen')   #11.8       15.9
    Hc_He_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Helium')    #6.6        6.2
    Hc_Ne_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Neon')   #19.4       17.2  
    
    '''
    print('Hi1',Hi1)
    # for solving mr2
    # assume x = 1 mol out of 100, 7.2 would be N2, 24.8 would be CH4 and so on
    # multiplier y will be applied to the mr2
    eff = 1
    
    #m1*(Hi1-He1) = 7.2 * x * Hi2 + 24.8 * x * Hi3 + 32.4 * x * Hi4 + 18.5 * x * Hi5 + 17.1 * x * Hi6
    if Te1 > 20:
        x = m1*(Hi1-He1)
    else:
        x = m1*(Hi1-He1+H_H2_vap) 
# boiling point:
# N2 77.36  Propane: 85.52 Isopentane: 113.25        
    if Te2 > 77.36:
        n2 = (7.2 * He2 * 28 + 24.8 * He3 * 16 + 32.4 * He4 * 28 + 18.5 * He5 * 44 + 17.1 * He6 * 72 -
                          (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72))
    elif Te2>30:
        n2 = (7.2 * He2 * 28 + 24.8 * He3 * 16 + 32.4 * He4 * 28 + 18.5 * He5 * 44 + 17.1 * He6 * 72 -
                          (7.2 * Hi2 * 28 + 24.8 * Hi3 * 16 + 32.4 * Hi4 * 28 + 18.5 * Hi5 * 44 + 17.1 * Hi6 * 72))
        
    x = Q1/n2
    '''
    # calculate the each individual heat exchange from streams using temperature/enthalpy change and mass flow change
    # Figure out how much mass flow is in each stream.
    # solving for individual mass flow rate percentage for the mix refrigerant
    
    total = 2.5*1 + 63.3*4 + 33.2*20
    # Nitrogen
    pmhydrogen = 2.5 / total
    pmhelium = 63.3*4 / total
    pmneon = 33.2*20 / total
    #print('%%%%%',pmpentane,pmb,pmpropane,pmethylene,pmethane,pmm,pmnitrogen,pmneon,pmr)
    #testing
    h2 = pmhydrogen * (Hh_Hy_2-Hc_Hy_2)+ pmhelium * (Hh_He_2-Hc_He_2) + pmneon * (Hh_Ne_2-Hc_Ne_2)
    print('h2h343434343',h2)
    #print(pmpentane * (Hh_Pe_2-Hc_Pe_2)+ pmb * (Hh_Bu_2-Hc_Bu_2) + pmpropane * (Hh_Pr_2-Hc_Pr_2) + pmethylene * (Hh_Ethy_2-Hc_Ethy_2),'\n 4',
    #      pmpentane * (Hh_Pe_4-Hc_Pe_4)+ pmb * (Hh_Bu_4-Hc_Bu_4) + pmpropane * (Hh_Pr_4-Hc_Pr_4) + pmethylene * (Hh_Ethy_4-Hc_Ethy_4))
    
    
    
    
    
    
    Q2 = m2 * h2
    #x =  m1*(Hi1-He1)/(11.8 * Hh_Pe_3 * 72.15 + 6.6 * He3 * 52.18 + 19.4 * He4 * 44.097 + 11.8 * He5 * 28.05 + 8.6 * He6 * 30.07 + 16.6 * He7 * 16.04 + 15.6 * He8 * 14 + 2.4 * He9 * 20.18 + 7.2 * He10 * 88 -
    #                  (11.8 * Hi2 * 72.15 + 6.6 * Hi3 * 52.18 + 19.4 * Hi4 * 44.097 + 11.8 * Hi5 * 28.05 + 8.6 * Hi6 * 30.07 + 16.6 * Hi7 * 16.04 + 15.6 * Hi8 * 14 + 2.4 * Hi9 * 20.18 + 7.2 * Hi10 * 88))
    print('Q2Q3Q4:',Q2)
    m1 = (Q2)/(Hh_Hy-Hc_Hy)        
    #m2 = 7.2 * x * 28 + 24.8 * x * 16 + 32.4 * x * 28 + 18.5 * x * 44 + 17.1 * x * 72
    return(m1)

he2 = heat_ex_cyro(133,67,132,64,1970000,1940000,130000,160000,45883)
he3 = heat_ex_cyro(77,43,75,37,1940000,1910000,130000,160000,45526)
he4 = heat_ex_cyro(55,36,53,26,1910000,1880000,130000,160000,59061)
he5 = heat_ex_cyro(77,43,75,37,1940000,1910000,130000,160000,59061)
print('results for 2!!!!!!',he2,'results for 3!!!!!!!!',he3,'results for4!!!!!!!!',he4)