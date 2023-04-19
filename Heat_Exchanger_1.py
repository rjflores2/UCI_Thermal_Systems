import numpy as np

def heat_exchanger(m_dot_hot, m_dot_cold, cp_hot, cp_cold, T_hot_in, T_cold_in, A, U, epsilon):
    """
    Calculates the performance of a counter-flow heat exchanger.
    
    Parameters:
    -----------
    m_dot_hot : float
        Mass flow rate of hot fluid (kg/s).
    m_dot_cold : float
        Mass flow rate of cold fluid (kg/s).
    cp_hot : float
        Specific heat capacity of hot fluid (J/(kg*K)).
    cp_cold : float
        Specific heat capacity of cold fluid (J/(kg*K)).
    T_hot_in : float
        Inlet temperature of hot fluid (degC).
    T_cold_in : float
        Inlet temperature of cold fluid (degC).
    A : float
        Heat transfer area (m^2).
    U : float
        Overall heat transfer coefficient (W/(m^2*K)).
    epsilon : float
        Effectiveness of heat exchanger.
        
    Returns:
    --------
    T_hot_out : float
        Outlet temperature of hot fluid (degC).
    T_cold_out : float
        Outlet temperature of cold fluid (degC).
    Q_net : float
        Net heat transfer rate (W).
    delta_T_lm : float
        Log mean temperature difference (K).
    R : float
        Thermal resistance of heat exchanger (m^2*K/W).
    """
    
    # Define convergence criteria
    tol = 1e-6  # tolerance for convergence
    maxiter = 1000  # maximum number of iterations
    
    # Initialize variables
    T_hot_out = T_hot_in
    T_cold_out = T_cold_in
    Q = 0  # heat transfer rate
    
    # Iterate until convergence
    for i in range(maxiter):
        # Calculate temperatures at midpoint of heat exchanger
        T_hot = (T_hot_in + T_hot_out) / 2
        T_cold = (T_cold_in + T_cold_out) / 2

        # Calculate heat transfer rate
        Q_max = m_dot_cold * cp_cold * (T_cold_in - T_cold)
        Q = epsilon * Q_max

        # Calculate outlet temperatures
        T_hot_out = T_hot - Q / (m_dot_hot * cp_hot)
        T_cold_out = T_cold + Q / (m_dot_cold * cp_cold)

        # Check for convergence
        if abs(T_hot_out - T_hot) < tol and abs(T_cold_out - T_cold) < tol:
            break
    
    # Calculate net heat transfer rate and log mean temperature difference
    Q_net = Q * 2  # factor of 2 for counter-flow heat exchanger
    delta_T_lm = (T_hot_in - T_cold_out - (T_hot_out - T_cold_in)) / np.log((T_hot_in - T_cold_out) / (T_hot_out - T_cold_in))
    
    # Calculate overall heat transfer coefficient and heat transfer area
    R = 1 / U
    A = Q_net / (R * delta_T_lm)
    
    return T_hot_out, T_cold_out, Q_net, delta_T_lm, R, A
