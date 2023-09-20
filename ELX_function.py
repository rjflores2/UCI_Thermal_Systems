import numpy as np
import CoolProp.CoolProp as CP
import math

R = 8314.47
F = 96484600

def P_H2O_Calc(T):
    T = T-298.15
    a = -2.1794+0.02953*T-9.1837*10**(-5)*T**2+1.4454*10**(-7)*T**3
    result = 10**a
    return result

def P_H2_Calc(T,P_H2):
    P_H2O = P_H2O_Calc(T)
    result = 0.5 * P_H2O*(math.exp(-4.192/T**1.334)*P_H2/P_H2O-1)
    return result


def P_O2_Calc(T,P_O2):
    P_H2O = P_H2O_Calc(T)
    result = P_H2O*(math.exp(-4.192/T**1.334)*P_O2/P_H2O-1)
    return result



def Enernst_Calc(T, PH2, PO2):
    pH2O = P_H2O_Calc(T)
    pH2 = P_H2_Calc(T,PH2)
    pO2 = P_O2_Calc(T,PO2)
    print(pH2O,pH2,pO2)
    result = 1.229 + (R * (T-298.15) / (2 * F)) *math.log((pH2 * math.sqrt(pO2)) / pH2O)
    return result

def VStack_Calc(N, Vcell):
    
    try:
        result = N * (Vcell)
        return result
    except TypeError:
        print(
            "[Error] VStack Calculation Error (N:%s, Vcell:%s)" %
            (str(N), str(Vcell)))

##fluid dynamic model
#lumped mass conservation equations

def Production_Calc(N,i_useful,A):
    #calculates the molar flow rate
    result = i_useful/2/F * A * N * 10**(-3) * 2
    m_dot_H2_prod = result
    m_dot_H2O_cons = result
    m_dot_O2_prod = result/2
    return (m_dot_H2,m_dot_H2O,m_dot_O2)

# molar balance
# H2 only on cathode side
# H2_in + H2_prod = H2_out
# O2 on anode side
# O2_in + O2_prod = O2_out
# H2O consumption on anode side
# H2O_in = H2O_out + H2O_cons
# H2O_cons = H2_prod = 2 * O2_prod

# molar balance for anode


# change the mass flow rate into molar flow rate, then do all the calculation in molar flow rate and then change them back to mass flow rate



def Electro_Osmotic_Drag_Calc(lamda):
    try:
        result = 0.0029*landa**2+0.05*lamda-3.4*10**(-19)
        return result
    except TypeError:
        print(
            "[Error] Electro Osmotic Drag Calculation Error (lamda)" %
            (str(lamda)))
        
# diffusion driven transport
#equation 8 & 9
def Dif_Coeff_Calc(binary):
    results = binary * 0.3 * ((0.3-0.11)/(1-0.11))**0.785
    return results

#equation 10
def Dif_a_b (p,T,Tca,Tcb,Pca,Pcb,MMa,MMb):
    results = 3.64*10**(-4) / p * (T/(Tca*Tcb)**0.5)**2.334 * (Pca*Pcb)**(1/3) * (Tca*Tcb)**(5/12) * (1/MMa+1/MMb)**0.5
    return results

#equation 11
#pressure driven transport:
def Press_Trans_Calc(pa,pb,A,tm):
    results = (1.58*10**(-16) * A * 1 * (pa-pb))/(tm*1.1*10**(-2))
    return results

# equation 12
# energy balance equaiton(last piece of the puzzle)
# P_stack(p=vi) + H_dot_in - H_dot_out - Q_dot_loss = C_stack (dT_stack/dt)
#def ener_bal_calc(T,PO2,PH2,i,A,t_el_c,t_el_a,resis_c,resis_a,t_mem,i_L,n):
#    voltage = Enernst_Calc(T,PO2,PH2) - Eta_Act_Calc(T,PO2,PH2,i,A) - Concentration_Calc(T,i_L,n) - Ohmic_Calc(i,A,T,t_el_c,t_el_a,resis_c,resis_a,t_mem)
#    V_stack = N * voltage
#    P_stack = V_stack*i
#    results = 

#Actvation loss
def Eta_Act_Calc(T, i):
    i_0 = Exchange_i_Calc(T)
    result = R*T/F * (np.arcsinh(i/2/i_0*np.pi/180))
    return result
#equation 17
def Exchange_i_Calc (T):
    result = 2.16*10**(-6) * math.exp(-76000 / R / T)
    return result

#equation 18
#ohmic loss
def Ohmic_Calc(i,A,T,t_el_c,t_el_a,resis_c,resis_a,t_mem):
    proton_cond_mem = (0.005139*22-0.00326)*math.exp(1268*(1/303-1/T))
    r_el_a = r_el_calc(t_el_a,A,resis_a)
    r_el_c = r_el_calc(t_el_c,A,resis_c)
    r_mem = r_mem_calc(t_mem,proton_cond_mem,A)
    result = (r_el_a+r_el_c+r_mem) * i * A
    return result

def r_el_calc(t_el,a,resis):
    result = t_el*resis/a
    return result

def r_mem_calc(t_mem,proton_cond,a):
    result = t_mem/a/proton_cond
    return result

def Concentration_Calc(T,i_L,n,i):
    result = R*T/0.5/F/n*math.log(i_L/(i_L-i))
    return result

#def new_Ohmic_calc(i,A,T):
#    v_ohm_a = 
#    v_ohm_c = 
#    v_ohm_m = 
#    result = v_ohm_a + v_ohm_c + v_ohm_m
#    return result

#%% Static Analysis
def Static_Analysis(T,PH2,PO2,i_start,i_stop,i_step,A):
    I_List = []
    Vstack_List = []
    Eta_Ohmic_List = []
    Eta_Conc_List = []
    Eta_Active_List = []
    Curr_Density_List = []
    I = i_start
    t_el_c=0.01
    t_el_a=0.01
    resis_c=0.0075
    resis_a=0.0075
    t_mem=0.0322
    i_L=6
    n=2
    
    while I < i_stop:
        i = I
        Curr_Density = i/A
        Curr_Density_List.append(Curr_Density)
        
        Act_Loss = Eta_Act_Calc(T, Curr_Density)
        Eta_Active_List.append(Act_Loss)
        
        Ohmic_Loss = Ohmic_Calc(Curr_Density,A,T,t_el_c,t_el_a,resis_c,resis_a,t_mem)
        Eta_Ohmic_List.append(Ohmic_Loss)
        
        Conc_Loss = Concentration_Calc(T,i_L,n,Curr_Density)
        Eta_Conc_List.append(Conc_Loss)
        
        
        
        Nernst_V = Enernst_Calc(T, PH2, PO2)
        V = Nernst_V + Conc_Loss + Ohmic_Loss + Act_Loss
        Vstack_List.append(V)
        
        I = I+i_step
        
    return {"Act":Eta_Active_List,"Ohmic":Eta_Ohmic_List,"Conc":Eta_Conc_List,"Curr":Curr_Density_List,"V":Vstack_List}

#%% Mass Balance
#Mass balance
def H2_Calc(N,i_useful,A):
    #N: number of cells
    #A: area of cell
    #calculates the molar flow rate
    result = i_useful/2/F * A * N 
    return (result)

def O2_Calc(N,i_useful,A):
    #calculates the molar flow rate
    result = i_useful/2/F * A * N /2
    return (result)

#testing: N = 65
#         A = 214 cm^2
#         i = 1 A/cm^2
def mass_balance(N,I,A):
#Anode balance
    ndot_O2_prod = O2_Calc(N,I,A)

#Cathode balance
    ndot_H2_prod = H2_Calc(N,I,A)
    ndot_H2O_cons = H2_Calc(N,I,A)
    
    mdot_O2_prod = ndot_O2_prod * 31 *3600
    mdot_H2_prod = ndot_H2_prod * 2.016 *3600
    mdot_H2O_cons = ndot_H2O_cons * 18 *3600
    
    return(mdot_O2_prod,mdot_H2_prod,mdot_H2O_cons)

print(O2_Calc(65,1,214)*31*3600)

mdot_O2_prod,mdot_H2_prod,mdot_H2O_cons = mass_balance(65,2,214)
print(mdot_O2_prod)


#%% Energy Balance
def energy_balance(T,PH2,PO2,PH2O,I,N,Q_dot_loss):
    #energy balance
    #voltage = Enernst_Calc(T,PO2,PH2) - Eta_Act_Calc(T,PO2,PH2,i,A) - Concentration_Calc(T,i_L,n) - Ohmic_Calc(i,A,T,t_el_c,t_el_a,resis_c,resis_a,t_mem)
    i = I/900
    a55 = Static_Analysis(T,PH2,PO2,I,I+0.5,1,900);
    V_stack = N * a55["V"][0]     #[V]
    P_stack = V_stack*I/10000           #[W]

    #choose an operating temperature
    #testing 55C

    #preset: H2_in, O2_in, H2O_in
    #determined: H2_out = H2_in + H2_prod
    # O2_out = O2_in + O2_prod
    #H2O_out = H2O_in - H2O_cons

    #flow in = H2_in,O2_in,H2O_in
    m_H2_in = 0/3600 #kg/s
    m_O2_in = 0/3600 #kg/s
    m_H2O_in = 5000/3600 #kg/s
    #m_H2_in + m_O2_in + m_H2O_in
    H_H2_in = CP.PropsSI('H','T',T,'P',PH2,'H2');     #[J/kg]
    H_H2O_in = CP.PropsSI('H','T',T,'P',PH2O,'H2O'); 
    H_O2_in = CP.PropsSI('H','T',T,'P',PO2,'O2'); 
    MixH_dot_in = (H_H2_in * m_H2_in + H_H2O_in * m_H2O_in + H_O2_in * m_O2_in)
    #print('P_stack',P_stack,'MixH_dot_in',MixH_dot_in)
    #flow out = H2_out,O2_out,H2O_out
    mdot_O2_prod,mdot_H2_prod,mdot_H2O_cons = mass_balance(N,I/900,900);
    m_H2_out = m_H2_in + mdot_H2_prod/3600
    m_O2_out = m_O2_in + mdot_O2_prod/3600
    m_H2O_out = m_H2O_in - mdot_H2O_cons/3600
    print('h_in',H_H2_in,H_O2_in,H_H2O_in)
    print('m_out',m_H2_out,m_O2_out,m_H2O_out)
    #m_H2_out + m_O2_out + m_H2O_out

    #write a function that calculates the Q_dot_loss

    MixH_dot_out = P_stack + MixH_dot_in - Q_dot_loss
    print("P_stack",P_stack,"MixH_dot_in",MixH_dot_in,"MixH_dot_out",MixH_dot_out)

    #fsolve
    #MixH_dot_out - P_stack - MixH_dot_in + Q_dotloss = 0

    #solve for the MixH_dot_out
    # mixH_dot_out = sum of three H multiply by their individual mass out
    # mass out is known, temperature is unknown, but will be the same for all three
    # use a guess method to figure out all three.
    # use a for loop to add temperature until the H is more 

    T_out = T
    while T_out < T+800:
        H_test_H2 = CP.PropsSI('H','T',T_out,'P',31,'H2')
        H_test_H2O = CP.PropsSI('H','T',T_out,'P',1,'H2O')
        H_test_O2 = CP.PropsSI('H','T',T_out,'P',1,'O2')
        H_test_sum = H_test_H2*m_H2_out+H_test_H2O*m_H2O_out+H_test_O2*m_O2_out
        #print(H_test_sum)
        if H_test_sum > MixH_dot_out:
            print(H_test_H2,H_test_O2,H_test_H2O)
            #print(T_out)
            break
        else:
            T_out = T_out+0.1

    return (m_H2_out,T_out)
def q_loss(a):
    return 0


    #P_stack(p=vi) + H_dot_in - H_dot_out - Q_dot_loss = C_stack (dT_stack/dt)
    #H_dot_in depends on the temperature and concentration species of the inlet
    #H_dot_out depends on the 
    #fsolve with function for temperature
    
    