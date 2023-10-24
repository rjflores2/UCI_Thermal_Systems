import os
from math import exp, floor, log, sqrt, tanh  

def calc_Cmin(mh, mc, Cph, Cpc):
    '''
    mh : float
        Mass flow rate of hot stream, [kg/s]
    mc : float
        Mass flow rate of cold stream, [kg/s]
    Cph : float
        Averaged heat capacity of hot stream, [J/kg/K]
    Cpc : float
        Averaged heat capacity of cold stream, [J/kg/K]
    Cmin : float
        The heat capacity rate of the smaller fluid, [W/K]
    '''
   Ch = mh*Cph
   Cc = mc*Cpc
   return min(Ch, Cc)
def calc_Cmax(mh, mc, Cph, Cpc):
    '''
    mh : float
        Mass flow rate of hot stream, [kg/s]
    mc : float
        Mass flow rate of cold stream, [kg/s]
    Cph : float
        Averaged heat capacity of hot stream, [J/kg/K]
    Cpc : float
        Averaged heat capacity of cold stream, [J/kg/K]
    Cmax : float
        The heat capacity rate of the larger fluid, [W/K]
    '''
    Ch = mh*Cph
    Cc = mc*Cpc
    return max(Ch, Cc)
def calc_Cr(mh, mc, Cph, Cpc):
    '''
    mh : float
        Mass flow rate of hot stream, [kg/s]
    mc : float
        Mass flow rate of cold stream, [kg/s]
    Cph : float
        Averaged heat capacity of hot stream, [J/kg/K]
    Cpc : float
        Averaged heat capacity of cold stream, [J/kg/K]
    Cr : float
        The heat capacity rate ratio, of the smaller fluid to the larger
        fluid, [W/K]
    '''
    Ch = mh*Cph
    Cc = mc*Cpc
    Cmin = min(Ch, Cc)
    Cmax = max(Ch, Cc)
    return Cmin/Cmax
def effectiveness_from_NTU(NTU, Cr, subtype='counterflow', n_shell_tube=None):
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
    effectiveness : float
        The thermal effectiveness of the heat exchanger, [-]
    '''
    if Cr > 1:
        raise ValueError('Heat capacity rate must be less than 1 by definition.')

    if subtype == 'counterflow':
        if Cr < 1:
            return (1. - exp(-NTU*(1. - Cr)))/(1. - Cr*exp(-NTU*(1. - Cr)))
        elif Cr == 1:
            return NTU/(1. + NTU)
    elif subtype == 'parallel':
            return (1. - exp(-NTU*(1. + Cr)))/(1. + Cr)
    elif subtype == 'boiler' or subtype == 'condenser':
        return  1. - exp(-NTU)
    else:
        raise ValueError('Input heat exchanger type not recognized')
        
def NTU_from_effectiveness(effectiveness, Cr, subtype='counterflow', n_shell_tube=None):
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
            return 1./(Cr - 1.)*log((effectiveness - 1.)/(effectiveness*Cr - 1.))
        elif Cr == 1:
            return effectiveness/(1. - effectiveness)
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

def UA_from_NTU(NTU, Cmin):
    '''
    UA = NTU C_{min}
    NTU : float
        Thermal Number of Transfer Units [-]
    Cmin : float
        The heat capacity rate of the smaller fluid, [W/K]
    UA : float
        Combined area-heat transfer coefficient term, [W/K]
    '''
    return NTU*Cmin
        
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
        'crossflow, mixed Cmin', 'crossflow, mixed Cmax', 'boiler', 'condenser',
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
        * Cmin : The heat capacity rate of the smaller fluid [W/K]
        * Cmax : The heat capacity rate of the larger fluid [W/K]
        * effectiveness : The thermal effectiveness of the heat exchanger [-]
        * NTU : Thermal Number of Transfer Units [-]
        * Thi : Inlet temperature of hot fluid [K]
        * Tho : Outlet temperature of hot fluid [K]
        * Tci : Inlet temperature of cold fluid [K]
        * Tco : Outlet temperature of cold fluid [K]
    '''
    Cmin = calc_Cmin(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    Cmax = calc_Cmax(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    Cr = calc_Cr(mh=mh, mc=mc, Cph=Cph, Cpc=Cpc)
    Cc = mc*Cpc
    Ch = mh*Cph
    if UA is not None:
        NTU = NTU_from_UA(UA=UA, Cmin=Cmin)
        effectiveness = eff = effectiveness_from_NTU(NTU=NTU, Cr=Cr, n_shell_tube=n_shell_tube, subtype=subtype)

        possible_inputs = [(Tci, Thi), (Tci, Tho), (Tco, Thi), (Tco, Tho)]
        if not any(i for i in possible_inputs if None not in i):
            raise ValueError('One set of (Tci, Thi), (Tci, Tho), (Tco, Thi), or (Tco, Tho) are required along with UA.')

        if Thi is not None and Tci is not None:
            Q = eff*Cmin*(Thi - Tci)
        elif Tho is not None and Tco is not None:
            Q = eff*Cmin*Cc*Ch*(Tco - Tho)/(eff*Cmin*(Cc+Ch) - Ch*Cc)
        elif Thi is not None and Tco is not None:
            Q = Cmin*Cc*eff*(Tco-Thi)/(eff*Cmin - Cc)
        elif Tho is not None and Tci is not None:
            Q = Cmin*Ch*eff*(Tci-Tho)/(eff*Cmin - Ch)
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

        effectiveness = Q/Cmin/(Thi-Tci)
        NTU = NTU_from_effectiveness(effectiveness, Cr, n_shell_tube=n_shell_tube, subtype=subtype)
        UA = UA_from_NTU(NTU, Cmin)
    return {'Q': Q, 'UA': UA, 'Cr':Cr, 'Cmin': Cmin, 'Cmax':Cmax,
            'effectiveness': effectiveness, 'NTU': NTU, 'Thi': Thi, 'Tho': Tho,
            'Tci': Tci, 'Tco': Tco}



print(effectiveness_NTU_method(mh=2.4, mc=14.5, Cph=14000., Cpc=1061, subtype='counterflow', Tci=20, Tco=85, Thi=330))