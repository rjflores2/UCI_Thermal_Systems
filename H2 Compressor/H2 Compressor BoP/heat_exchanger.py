# Defining heat exchanger related functions
def effectiveness_from_NTU(NTU, Cr, subtype, n=None):
    """ (float, float, string, int) -> float
    Return the effectiveness (epsilon) of a specified type of HX based on inputted 
    number of thermal transfer units (NTU),
    the heat capacity rate ratio (Cr) of the smaller fluid to larger fluid ,
    the subtype of the heat exchanger ('counterflow','parallel','shell-and-tube','boiler','condenser'), 
    and the number of shell passes (n) if subtypes if 'shell-and-tube'.
    The thermal effectiveness of the heat exchanger is ratio of the actual heat transfer 
    rate for a HX to the max possible heat transfer rate.
    
    Source: Author’s initials. Author’s Surname, “CHAPTER 11 Heat Exchangers,” in Fundamentals of Heat and Mass Transfer, 
    7th edition, L. Ratts, Ed. Jefferson City: John Wiley and Sons, 2011, pp. 724
    """
    if Cr > 1:
        raise ValueError('Heat capacity rate must be less than 1 by definition.')
        
    if subtype == 'counterflow':
        if Cr < 1:
            epsilon = (1 - exp(-NTU*(1 - Cr)))/(1 - Cr*exp(-NTU*(1 - Cr))) # eq 11.29a
        elif Cr == 1:
            epsilon = NTU/(1 + NTU) # eq 11.29a
    elif subtype == 'parallel':
        epsilon = (1 - exp(-NTU*(1 + Cr)))/(1 + Cr) # eq 11.28a
    elif subtype == 'shell-and-tube':
        epsilon =  2*(1+Cr+((1+Cr**2)**0.5)*((1 + exp(-NTU*(1 + Cr**2)**0.5))/(1 - exp(-NTU*(1 + Cr**2)**0.5))))**-1 # eq 11.30a
        if n > 1:
            epsilon = (((((1-epsilon*Cr)/(1-epsilon))**n)-1)*((((1-epsilon*Cr)/(1-epsilon))**n)-Cr))**-1 # eq 11.31a
    elif subtype == 'boiler' or subtype == 'condenser':
        epsilon = 1 - exp(-NTU) # eq 11.35a
    else:
        raise ValueError('Input heat exchanger type not recognized')
        
    return epsilon
        
def NTU_from_effectiveness(epsilon, Cr, subtype, n=None):
    """ (float, float, string, int) -> float
    Return number of thermal transfer units (NTU) of a specified type of HX based on inputted 
    HX effectiveness (epsilon),
    the heat capacity rate ratio (Cr) of the smaller fluid to larger fluid ,
    the subtype of the heat exchanger ('counterflow','parallel','shell-and-tube','boiler','condenser'), 
    and the number of shell passes (n) if subtypes if 'shell-and-tube'.
    The thermal effectiveness of the heat exchanger is ratio of the actual heat transfer 
    rate for a HX to the max possible heat transfer rate.
    
    Source: Author’s initials. Author’s Surname, “CHAPTER 11 Heat Exchangers,” in Fundamentals of Heat and Mass Transfer, 
    7th edition, L. Ratts, Ed. Jefferson City: John Wiley and Sons, 2011, pp. 725
    """
    if Cr > 1:
        raise ValueError('Heat capacity rate must be less than 1 by definition.')

    if subtype == 'counterflow':
        if Cr < 1:
            NTU = 1/(Cr - 1)*ln((epsilon - 1)/(epsilon*Cr - 1)) # eq 11.29b
        elif Cr == 1:
            NTU = epsilon/(1 - epsilon) # eq 11.29b
    elif subtype == 'parallel':
        if epsilon*(1 + Cr) > 1:
            raise ValueError('The specified effectiveness is not physically '
                             'possible for this configuration; the maximum effectiveness '
                             'possible is %s.' % (1./(Cr + 1.)))
        NTU =  -ln(1 - epsilon*(1 + Cr))/(1 + Cr)
    elif subtype == 'shell-and-tube':
        F = ((epsilon*Cr - 1)/(epsilon-1))**(1/n)  # eq 11.31c
        epsilon1 = (F-1)/(F-Cr) # eq 11.31b
        E = ((2/epsilon1)-(1+Cr))/((1+Cr**2)**(0.5)) # eq 11.30c
        NTU = -((1+Cr**2)**-0.5)*ln((E-1)/(E+1)) # eq 11.30b
        if n > 1:
            NTU = n*NTU # eq 11.31d
    elif subtype == 'boiler' or subtype == 'condenser':
        NTU = -ln(1. - epsilon)
    else:
        raise ValueError('Input heat exchanger type not recognized')
        
    return NTU
    
def effectiveness_NTU_method(mdot_hot, mdot_cold, Cp_hot, Cp_cold, subtype, Thi=None,
                              Tho=None, Tci=None, Tco=None, UA=None,
                              n=None):
    '''
    Parameters
    mdot_hot : float
        Mass flow rate of hot stream [kg/s]
    mdot_cold : float
        Mass flow rate of cold stream [kg/s]
    Cp_hot : float
        Averaged heat capacity of hot stream [J/kg/K]
    Cp_cold : float
        Averaged heat capacity of cold stream [J/kg/K]
    subtype : str optional
        The subtype of exchanger; one of 'counterflow', 'parallel', 'crossflow'
        'crossflow, mixed C_min', 'crossflow, mixed C_max', 'boiler', 'condenser',
        'S&T', or 'nS&T' where n is the number of shell and tube exchangers in
        a row
    Thi : float optional
        Inlet temperature of hot fluid [K]
    Tho : float optional
        Outlet temperature of hot fluid [K]
    Tci : float optional
        Inlet temperature of cold fluid [K]
    Tco : float optional
        Outlet temperature of cold fluid [K]
    UA : float optional
        Combined Area-heat transfer coefficient term [W/K]
    n_shell_tube : None or int optional
        The number of shell and tube exchangers in a row [-]

    Returns
        * Q : Heat exchanged in the heat exchanger [W]
        * UA : Combined area-heat transfer coefficient term [W/K]
        * Cr : The heat capacity rate ratio of the smaller fluid to the larger fluid [W/K]
        * C_min : The heat capacity rate of the smaller fluid [W/K]
        * C_max : The heat capacity rate of the larger fluid [W/K]
        * epsilon : The thermal effectiveness of the heat exchanger [-]
        * NTU : Thermal Number of Transfer Units [-]
        * Thi : Inlet temperature of hot fluid [K]
        * Tho : Outlet temperature of hot fluid [K]
        * Tci : Inlet temperature of cold fluid [K]
        * Tco : Outlet temperature of cold fluid [K]
    '''
    C_hot = Cp_hot*mdot_hot # [W/K] heat capacity rate
    C_cold = Cp_cold*mdot_cold # [W/K] heat capacity rate
    C_min = min(C_hot,C_cold) # [W/K] heat capacity rate of "smaller" fluid
    C_max = max(C_hot,C_cold) # [W/K] heat capacity rate "larger" fluid
    Cr = C_min/C_max # The heat capacity rate ratio, of the smaller fluid to the larger
    
    if UA is not None:
        NTU = C_min*UA
        epsilon = effectiveness_from_NTU(NTU, Cr, subtype, n)

        possible_inputs = [(Tci, Thi), (Tci, Tho), (Tco, Thi), (Tco, Tho)]
        if not any(i for i in possible_inputs if None not in i):
            raise ValueError('One set of (Tci, Thi), (Tci, Tho), (Tco, Thi), or (Tco, Tho) are required along with UA.')
            
        if Thi is not None and Tci is not None:
            Q = epsilon*C_min*(Thi - Tci)
        elif Tho is not None and Tco is not None:
            Q = epsilon*C_min*C_cold*C_hot*(Tco - Tho)/(epsilon*C_min*(C_cold+C_hot) - C_hot*C_cold)
        elif Thi is not None and Tco is not None:
            Q = C_min*C_cold*epsilon*(Tco-Thi)/(epsilon*C_min - C_cold)
        elif Tho is not None and Tci is not None:
            Q = C_min*C_hot*epsilon*(Tci-Tho)/(epsilon*C_min - C_hot)
        if Tci is not None and Tco is None:
            Tco = Tci + Q/(C_cold)
        else:
            Tci = Tco - Q/(C_cold)
        if Thi is not None and Tho is None:
            Tho = Thi - Q/(C_hot)
        else:
            Thi = Tho + Q/(C_hot)

    elif UA is None:
        # Case where we're solving for UA
        # Three temperatures are required
        # Ensures all four temperatures are set and Q is calculated
        if Thi is not None and Tho is not None:
            Q = mdot_hot*Cp_hot*(Thi-Tho); print(Q)
            if Tci is not None and Tco is None:
                Tco = Tci + Q/(mdot_cold*Cp_cold)
            elif Tco is not None and Tci is None:
                Tci = Tco - Q/(mdot_cold*Cp_cold)
            elif Tco is not None and Tci is not None:
                Q2 = mdot_cold*Cp_cold*(Tco-Tci)
                if abs((Q-Q2)/Q) > 0.01:
                    raise ValueError('The specified heat capacities, mass flows, and temperatures are inconsistent')
            else:
                raise ValueError('At least one temperature is required to be specified on the cold side.')

        elif Tci is not None and Tco is not None:
            Q = mdot_cold*Cp_cold*(Tco-Tci); 
            if Thi is not None and Tho is None:
                Tho = Thi - Q/(mdot_hot*Cp_hot)
            elif Tho is not None and Thi is None:
                Thi = Tho + Q/(mdot_hot*Cp_hot)
            else:
                raise ValueError('At least one temperature is required to be specified on the cold side.')
        else:
            raise ValueError('Three temperatures are required to be specified when solving for UA')

        epsilon = Q/C_min/(Thi-Tci)
        NTU = NTU_from_effectiveness(epsilon, Cr, n= n , subtype=subtype)
        UA = NTU*C_min # [W/K] Combined area-heat transfer coefficient term (eq 11.24)
        HX_summary = {'Q': Q, 'UA': UA, 'Cr':Cr, 'C_min': C_min, 'C_max':C_max,
                'effectiveness': epsilon, 'NTU': NTU, 'Thi': Thi, 'Tho': Tho,
                'Tci': Tci, 'Tco': Tco}
    return HX_summary

# Define parameters and constants
H2_den = CP.PropsSI('D','T', streams_in[0].T,'P',streams_in[0].P,'H2'); #print('H2 density = ', H2_den) # [kg/m^3] density at normal operating conditions to determine mass flow rate
H2_mm = CP.PropsSI('molarmass', 'H2') # [kg/mol]
H2O_mm = CP.PropsSI('molarmass', 'H2O') # [kg/mol]
mdot_hot = streams_in[0].N*H2_mm; #print('Hot mass flow rate = ', mdot_hot, '[kg/s]') # [kg/s] hot stream mass flow rate
mdot_cold = streams_in[1].N*H2O_mm; #print('Cold mass flow rate = ', mdot_cold, '[kg/s]') # [kg/s] cold stream mass flow rate
Cp_hot = Cp_mass('H2', streams_in[0].P, streams_in[0].T); #print('Hot stream Cp = ', Cp_hot, '[J/kg/K]') # [J/kg/K] constant pressure specifc heat 
Cp_cold = Cp_mass('H2O_L', streams_in[1].P, streams_in[1].T); #print('Cold stream Cp = ', Cp_cold, '[J/kg/K]') # [J/kg/K] constant pressure specifc heat 
C_hot = Cp_hot*mdot_hot # [W/K] heat capacity rate
C_cold = Cp_cold*mdot_cold # [W/K] heat capacity rate
C_min = min(C_hot,C_cold) # [W/K] heat capacity rate of "smaller" fluid
C_max = max(C_hot,C_cold) # [W/K] heat capacity rate "larger" fluid
Cr = C_min/C_max # The heat capacity rate ratio, of the smaller fluid to the larger

HX = effectiveness_NTU_method(mdot_hot, mdot_cold, Cp_hot, Cp_cold, subtype = compressor_main_props['HX type'], Tci= streams_in[1].T, Thi = streams_in[0].T, Tco = 330)

streams_out[0].T = HX['Tho']
streams_out[0].P = streams_in[0].P
streams_out[0].N = streams_in[0].N
streams_out[0].x_H2 = streams_in[0].x_H2

streams_out[1].T = HX['Tco']
streams_out[1].P = streams_in[1].P
streams_out[1].N = streams_in[1].N
streams_out[1].x_H2O_l = streams_in[1].x_H2O_l