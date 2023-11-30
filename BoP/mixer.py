""" 
n -> 1 mixer
sum(mi)=mo
variables input: temperature for inlet, mass flow rate for inlet
variables output: temperature for outlet, mass flow rate for outlet
assumptions: pressure is the universal for inlet and outlet, change in kenetic energy is zero
energy balance equation: mo(ho+(vo^2)/2)=sum (mi(hi+(vi^2)/2))
"""

"""
approach the problem: always solving for the temperature of the outlet
take in a list of parameters for the inlet, such as the temperature and the mass flow for each streams then do the energy 
balance to solve for the temperature at the outlet.
variable such as Ti and mi are lists and have to be in the right order
"""
def mixer(Ti,mi,type,h,c):
