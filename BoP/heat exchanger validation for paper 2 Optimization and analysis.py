# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:30:14 2023

@author: labuser-fc
"""
#latent heat of condensation as a function of temperature

#initialize a hot temperature
import CoolProp.CoolProp as CP;

def heat_ex(Th1,Tc1,Th2,Tc2,Th3,Tc3,Th4,Tc4,Th5,Tc5,Th6,Tc6,Ph1,Pc1,Ph2,Pc2,Ph3,Pc3,Ph4,Pc4,Ph5,Pc5,Ph6,Pc6,m2,m3,m4,m5,m6):
# MR1 MR2, H2
#Enthalpy [J/kg]
#Enthalpy of Vap for Hydrogen 446.4 J/g = 446400J/kg

 #   H_H2_vap = 446400

#hot stream enthalpy    
    Hh_Hy = CP.PropsSI('H', 'T', Th1, 'P', Ph1, 'Hydrogen')
#mr2    CH4.	C2H4.	C2H6	C3H8	n-C4H10	n-C5H12	H2	N2	R14
    Hh_Me_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Methane')
    Hh_Ethy_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Ethylene')
    Hh_Etha_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Ethane')
    Hh_Pr_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Propane')
    Hh_Bu_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Butane')
    Hh_Pe_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Pentane')
    Hh_Hy_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Hydrogen')
    Hh_Ni_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'Nitrogen')
    Hh_R_2 = CP.PropsSI('H', 'T', Th2, 'P', Ph2, 'R14')
#mr3    
    Hh_Me_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Methane')
    Hh_Ethy_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Ethylene')
    Hh_Etha_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Ethane')
    Hh_Pr_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Propane')
    Hh_Bu_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Butane')
    Hh_Pe_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Pentane')
    Hh_Hy_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Hydrogen')
    Hh_Ni_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'Nitrogen')
    Hh_R_3 = CP.PropsSI('H', 'T', Th3, 'P', Ph3, 'R14')
#mr4    
    Hh_Me_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Methane')
    Hh_Ethy_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Ethylene')
    Hh_Etha_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Ethane')
    Hh_Pr_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Propane')
    Hh_Bu_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Butane')
    Hh_Pe_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Pentane')
    Hh_Hy_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Hydrogen')
    Hh_Ni_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'Nitrogen')
    Hh_R_4 = CP.PropsSI('H', 'T', Th4, 'P', Ph4, 'R14')
    
#sr5
    Hh_He_5 = CP.PropsSI('H', 'T', Th5, 'P', Ph5, 'Helium')
    Hh_Ne_5 = CP.PropsSI('H', 'T', Th5, 'P', Ph5, 'Neon')
    Hh_Hy_5 = CP.PropsSI('H', 'T', Th5, 'P', Ph5, 'Hydrogen')

#sr6
    Hh_He_6 = CP.PropsSI('H', 'T', Th6, 'P', Ph6, 'Helium')
    Hh_Ne_6 = CP.PropsSI('H', 'T', Th6, 'P', Ph6, 'Neon')
    Hh_Hy_6 = CP.PropsSI('H', 'T', Th6, 'P', Ph6, 'Hydrogen')
    
#cold stream enthalpy    
    Hc_Hy = CP.PropsSI('H', 'T', Tc1, 'P', Pc1, 'Hydrogen')
#mr2    
    Hc_Me_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Methane')
    Hc_Ethy_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Ethylene')
    Hc_Etha_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Ethane')
    Hc_Pr_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Propane')
    Hc_Bu_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Butane')
    Hc_Pe_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Pentane')
    Hc_Hy_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Hydrogen')
    Hc_Ni_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'Nitrogen')
    Hc_R_2 = CP.PropsSI('H', 'T', Tc2, 'P', Pc2, 'R14')
#mr3    
    Hc_Me_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Methane')
    Hc_Ethy_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Ethylene')
    Hc_Etha_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Ethane')
    Hc_Pr_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Propane')
    Hc_Bu_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Butane')
    Hc_Pe_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Pentane')
    Hc_Hy_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Hydrogen')
    Hc_Ni_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'Nitrogen')
    Hc_R_3 = CP.PropsSI('H', 'T', Tc3, 'P', Pc3, 'R14')
#mr4    
    Hc_Me_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Methane')
    Hc_Ethy_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Ethylene')
    Hc_Etha_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Ethane')
    Hc_Pr_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Propane')
    Hc_Bu_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Butane')
    Hc_Pe_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Pentane')
    Hc_Hy_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Hydrogen')
    Hc_Ni_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'Nitrogen')
    Hc_R_4 = CP.PropsSI('H', 'T', Tc4, 'P', Pc4, 'R14')    
    
#sr5
    Hc_He_5 = CP.PropsSI('H', 'T', Tc5, 'P', Pc5, 'Helium')
    Hc_Ne_5 = CP.PropsSI('H', 'T', Tc5, 'P', Pc5, 'Neon') 
    Hc_Hy_5 = CP.PropsSI('H', 'T', Tc5, 'P', Pc5, 'Hydrogen') 
#sr6
    Hc_He_6 = CP.PropsSI('H', 'T', Tc6, 'P', Pc6, 'Helium')
    Hc_Ne_6 = CP.PropsSI('H', 'T', Tc6, 'P', Pc6, 'Neon') 
    Hc_Hy_6 = CP.PropsSI('H', 'T', Tc6, 'P', Pc6, 'Hydrogen') 
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
    # Pentane
    total = 17*16 + 16*28 + 7*30 + 18*44 + 2*52 + 15*72 + 1*2 + 16*28 + 8*88
    
    pmpentane = 15*72 / (total)
    #Butane
    pmb = 2*52 / (total)
    #Propane
    pmpropane = 18*44 / (total)
    #Ethylene
    pmethylene = 16*28 / (total) #
    #Ethane
    pmethane = 7*30 / (total)#
    #Methane
    pmm = 17*16 / (total)#
    #Nitrogen
    pmnitrogen = 16*28 / (total)
    #hydrogen
    pmhy = 1*2 / (total)
    #R14
    pmr = 8*88 / (total)
    
    totalsr = 6.5*2 + 83.5*4 + 10*20
    # Nitrogen
    pmhydrogen = 6.5*2 / totalsr
    pmhelium = 83.5*4 / totalsr
    pmneon = 10*20 / totalsr
    
    #print('%%%%%',pmpentane,pmb,pmpropane,pmethylene,pmethane,pmm,pmnitrogen,pmneon,pmr)
    #testing
    h2 = (pmpentane * (Hh_Pe_2-Hc_Pe_2)+ pmb * (Hh_Bu_2-Hc_Bu_2) + pmpropane * (Hh_Pr_2-Hc_Pr_2) + pmethylene * (Hh_Ethy_2-Hc_Ethy_2) +
              pmethane * (Hh_Etha_2-Hc_Etha_2) + pmm * (Hh_Me_2-Hc_Me_2) + pmnitrogen * (Hh_Ni_2-Hc_Ni_2) + pmhy * (Hh_Hy_2-Hc_Hy_2) + pmr * (Hh_R_2-Hc_R_2))
    h3 = (pmpentane * (Hh_Pe_3-Hc_Pe_3)+ pmb * (Hh_Bu_3-Hc_Bu_3) + pmpropane * (Hh_Pr_3-Hc_Pr_3) + pmethylene * (Hh_Ethy_3-Hc_Ethy_3) +
              pmethane * (Hh_Etha_3-Hc_Etha_3) + pmm * (Hh_Me_3-Hc_Me_3) + pmnitrogen * (Hh_Ni_3-Hc_Ni_3) + pmhy * (Hh_Hy_3-Hc_Hy_3) + pmr * (Hh_R_3-Hc_R_3))
    h4 = (pmpentane * (Hh_Pe_4-Hc_Pe_4)+ pmb * (Hh_Bu_4-Hc_Bu_4) + pmpropane * (Hh_Pr_4-Hc_Pr_4) + pmethylene * (Hh_Ethy_4-Hc_Ethy_4) +
              pmethane * (Hh_Etha_4-Hc_Etha_4) + pmm * (Hh_Me_4-Hc_Me_4) + pmnitrogen * (Hh_Ni_4-Hc_Ni_4) + pmhy * (Hh_Hy_4-Hc_Hy_4) + pmr * (Hh_R_4-Hc_R_4))
    h5 = pmhydrogen * (Hh_Hy_5-Hc_Hy_5)+ pmhelium * (Hh_He_5-Hc_He_5) + pmneon * (Hh_Ne_5-Hc_Ne_5)
    h6 = pmhydrogen * (Hh_Hy_6-Hc_Hy_6)+ pmhelium * (Hh_He_6-Hc_He_6) + pmneon * (Hh_Ne_6-Hc_Ne_6)
    #print('h2h3h4',h2,h3,h4)
    #print(pmpentane * (Hh_Pe_2-Hc_Pe_2)+ pmb * (Hh_Bu_2-Hc_Bu_2) + pmpropane * (Hh_Pr_2-Hc_Pr_2) + pmethylene * (Hh_Ethy_2-Hc_Ethy_2),'\n 4',
    #      pmpentane * (Hh_Pe_4-Hc_Pe_4)+ pmb * (Hh_Bu_4-Hc_Bu_4) + pmpropane * (Hh_Pr_4-Hc_Pr_4) + pmethylene * (Hh_Ethy_4-Hc_Ethy_4))
    
    
    
    
    
    
    Q2 = m2 * h2
    Q3 = m3 * h3
    Q4 = m4 * h4
    Q5 = m5 * h5
    Q6 = m6 * h6
    print(Hh_Hy,Hc_Hy)
    #x =  m1*(Hi1-He1)/(11.8 * Hh_Pe_3 * 72.15 + 6.6 * He3 * 52.18 + 19.4 * He4 * 44.097 + 11.8 * He5 * 28.05 + 8.6 * He6 * 30.07 + 16.6 * He7 * 16.04 + 15.6 * He8 * 14 + 2.4 * He9 * 20.18 + 7.2 * He10 * 88 -
    #                  (11.8 * Hi2 * 72.15 + 6.6 * Hi3 * 52.18 + 19.4 * Hi4 * 44.097 + 11.8 * Hi5 * 28.05 + 8.6 * Hi6 * 30.07 + 16.6 * Hi7 * 16.04 + 15.6 * Hi8 * 14 + 2.4 * Hi9 * 20.18 + 7.2 * Hi10 * 88))
    #print('Q2Q3Q4:',Q2,Q3,Q4)
    #print(Q4-Q3-Q2,Hh_Hy-Hc_Hy)
    m1 = (Q4-Q6+Q5-Q3-Q2)/(Hh_Hy-Hc_Hy)        
    #m2 = 7.2 * x * 28 + 24.8 * x * 16 + 32.4 * x * 28 + 18.5 * x * 44 + 17.1 * x * 72
    return(m1)

#m2,ratio = heat_ex(101325,298,120,140,139,18.78)
#def heat_ex(amb_pres,Th1,Tc1,Th2,Tc2,Th3,Tc3,Th4,Tc4,m2,m3,m4):
m1 =  heat_ex(298.15,226.54,300.7,228.15,300.7,228.15,298.15,227.57,292.64,224.47,25+273.15,273.15-45,2100000,2100000,1924000,1924000,1924000,1924000,320500,320500,102300,102300,746400,746400,63.75,31.07,94.82,19.87,16.52)

#m2 =  heat_ex(255,235,255,235,255,235,235.7,224.7,7870000,7750000,2440000,2400000,2440000,2400000,110000,120000,12.81,7.24,29.37)
print('results for 1!!!!!!',m1,'results for 2!!!!!!!!')



# latent heat, enthalpy of vaporization/ phase change

'''
for hydrogen the enthalpy of phase change will happen at 20K when hydrogen starts to condense, and at 14K when hydrogen turns into solid.
H_vap = 446.4  kJ/kg 

delta_H = H_in - H_out +
'''