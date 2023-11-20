import os
from math import exp, floor, log, sqrt, tanh  

# Define parameters and constants
H2_den = CP.PropsSI('D','T', streamsIn[0].T,'P',streamsIn[0].P,'H2'); #print('H2 density = ', H2_den) # [kg/m^3] density at normal operating conditions to determine mass flow rate
H2_mm = CP.PropsSI('molarmass', 'H2') # [kg/mol]
H2O_mm = CP.PropsSI('molarmass', 'H2O') # [kg/mol]
mdot_hot = streams_in[0].N*H2_mm # [kg/s] hot stream mass flow rate
mdot_cold = streams_in[1].N*H2O_mm # [kg/s] cold stream mass flow rate
Cp_hot = Cp_mass('H2', streams_in[0].P, streams_in[0].T) # [J/kg/K] constant pressure specifc heat 
Cp_cold = Cp_mass('H2O_L', streams_in[1].P, streams_in[1].T) # [J/kg/K] constant pressure specifc heat 
C_hot = Cp_hot*mdot_hot # [W/K] heat capacity rate
C_cold = Cp_cold*mdot_cold # [W/K] heat capacity rate
C_min = min(C_hot,C_cold) # [W/K] heat capacity rate of "smaller" fluid
C_max = max(C_hot,C_cold) # [W/K] heat capacity rate "larger" fluid
Cr = C_min/C_max # The heat capacity rate ratio, of the smaller fluid to the larger

def effectiveness_from_NTU(NTU, Cr, subtype):
    '''
    Supports Counterflow, parallel flow,boiler and condenser
    Equation table on P.725 of the book
    
    NTU : float
        Thermal Number of Transfer Units [-]
    Cr : float
        The heat capacity rate ratio, of the smaller fluid to the larger
        fluid, [-]
    subtype : str, optional
        The subtype of exchanger; one of 'counterflow', 'parallel', 'boiler', 'condenser'
    effectiveness (epsilon) : float
        The thermal effectiveness of the heat exchanger, [-]
    '''
    if Cr > 1:
        raise ValueError('Heat capacity rate must be less than 1 by definition.')

    if subtype == 'counterflow':
        if Cr < 1:
            epsilon = (1 - exp(-NTU*(1 - Cr)))/(1 - Cr*exp(-NTU*(1 - Cr))) # eq 11.29a
        elif Cr == 1:
            epsilon = NTU/(1. + NTU) # eq 11.29a
    elif subtype == 'parallel':
            epsilon = (1 - exp(-NTU*(1 + Cr)))/(1 + Cr) # eq 11.28a
    elif subtype == 'boiler' or subtype == 'condenser':
        epsilon = 1 - exp(-NTU) # eq 11.35a
    else:
        raise ValueError('Input heat exchanger type not recognized')
        
    return epsilon
        
def NTU_from_effectiveness(effectiveness, Cr, subtype):
    '''
    Supports Counterflow, parallel flow,boiler and condenser
    Equation table on P.725 of the book
    
    effectiveness : float
        The thermal effectiveness of the heat exchanger, [-]
    Cr : float
        The heat capacity rate ratio, of the smaller fluid to the larger
        fluid, [-]
    subtype : str, optional
        The subtype of exchanger; one of 'counterflow', 'parallel', 'boiler', 'condenser'.
    NTU : float
        Thermal Number of Transfer Units [-]
    '''
    if Cr > 1:
        raise ValueError('Heat capacity rate must be less than 1 by definition.')

    if subtype == 'counterflow':
        if Cr < 1:
            return 1./(Cr - 1.)*log((effectiveness - 1.)/(effectiveness*Cr - 1.)) # eq 11.29b
        elif Cr == 1:
            return effectiveness/(1. - effectiveness) # eq 11.29b
    elif subtype == 'parallel':
        if effectiveness*(1. + Cr) > 1:
            raise ValueError('The specified effectiveness is not physically '
                             'possible for this configuration; the maximum effectiveness '
                             'possible is %s.' % (1./(Cr + 1.)))
        return -log(1. - effectiveness*(1. + Cr))/(1. + Cr)
    elif subtype in ['boiler', 'condenser']:
        return -log(1. - effectiveness)
    else:
        raise ValueError('Input heat exchanger type not recognized')

def UA_from_NTU(NTU, C_min):
    '''
    UA = NTU C_{min}
    NTU : float
        Thermal Number of Transfer Units [-]
    C_min : float
        The heat capacity rate of the smaller fluid, [W/K]
    UA : float
        Combined area-heat transfer coefficient term, [W/K]
    '''
    return NTU*C_min
        
def effectiveness_NTU_method(mh, mc, Cph, Cpc, subtype='counterflow', Thi=None,
                             Tho=None, Tci=None, Tco=None, UA=None,
                             n_shell_tube=None):
    '''
    Parameters
    mh : float
        Mass flow rate of hot stream [kg/s]
    mc : float
        Mass flow rate of cold stream [kg/s]
    Cph : float
        Averaged heat capacity of hot stream [J/kg/K]
    Cpc : float
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
        * effectiveness : The thermal effectiveness of the heat exchanger [-]
        * NTU : Thermal Number of Transfer Units [-]
        * Thi : Inlet temperature of hot fluid [K]
        * Tho : Outlet temperature of hot fluid [K]
        * Tci : Inlet temperature of cold fluid [K]
        * Tco : Outlet temperature of cold fluid [K]
    '''
    C_min = calc_C_min(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    C_max = calc_C_max(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    Cr = calc_Cr(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    Cc = mc*Cpc
    Ch = mh*Cph
    if UA is not None:
        NTU = NTU_from_UA(UA=UA, C_min=C_min)
        effectiveness = eff = effectiveness_from_NTU(NTU=NTU, Cr=Cr, n_shell_tube=n_shell_tube, subtype=subtype)

        possible_inputs = [(Tci, Thi), (Tci, Tho), (Tco, Thi), (Tco, Tho)]
        if not any(i for i in possible_inputs if None not in i):
            raise ValueError('One set of (Tci, Thi), (Tci, Tho), (Tco, Thi), or (Tco, Tho) are required along with UA.')

        if Thi is not None and Tci is not None:
            Q = eff*C_min*(Thi - Tci)
        elif Tho is not None and Tco is not None:
            Q = eff*C_min*Cc*Ch*(Tco - Tho)/(eff*C_min*(Cc+Ch) - Ch*Cc)
        elif Thi is not None and Tco is not None:
            Q = C_min*Cc*eff*(Tco-Thi)/(eff*C_min - Cc)
        elif Tho is not None and Tci is not None:
            Q = C_min*Ch*eff*(Tci-Tho)/(eff*C_min - Ch)
        if Tci is not None and Tco is None:
            Tco = Tci + Q/(Cc)
        else:
            Tci = Tco - Q/(Cc)
        if Thi is not None and Tho is None:
            Tho = Thi - Q/(Ch)
        else:
            Thi = Tho + Q/(Ch)

    elif UA is None:
        # Case where we're solving for UA
        # Three temperatures are required
        # Ensures all four temperatures are set and Q is calculated
        if Thi is not None and Tho is not None:
            Q = mh*Cph*(Thi-Tho)
            if Tci is not None and Tco is None:
                Tco = Tci + Q/(mc*Cpc)
            elif Tco is not None and Tci is None:
                Tci = Tco - Q/(mc*Cpc)
            elif Tco is not None and Tci is not None:
                Q2 = mc*Cpc*(Tco-Tci)
                if abs((Q-Q2)/Q) > 0.01:
                    raise ValueError('The specified heat capacities, mass flows, and temperatures are inconsistent')
            else:
                raise ValueError('At least one temperature is required to be specified on the cold side.')

        elif Tci is not None and Tco is not None:
            Q = mc*Cpc*(Tco-Tci)
            if Thi is not None and Tho is None:
                Tho = Thi - Q/(mh*Cph)
            elif Tho is not None and Thi is None:
                Thi = Tho + Q/(mh*Cph)
            else:
                raise ValueError('At least one temperature is required to be specified on the cold side.')
        else:
            raise ValueError('Three temperatures are required to be specified when solving for UA')

        effectiveness = Q/C_min/(Thi-Tci)
        NTU = NTU_from_effectiveness(effectiveness, Cr, n_shell_tube=n_shell_tube, subtype=subtype)
        UA = UA_from_NTU(NTU, C_min)
    return {'Q': Q, 'UA': UA, 'Cr':Cr, 'C_min': C_min, 'C_max':C_max,
            'effectiveness': effectiveness, 'NTU': NTU, 'Thi': Thi, 'Tho': Tho,
            'Tci': Tci, 'Tco': Tco}



print(effectiveness_NTU_method(mh=2.4, mc=14.5, Cph=14000., Cpc=1061, subtype='counterflow', Tci=20, Tco=85, Thi=330))