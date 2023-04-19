import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

L = 60 # m, pipe Length
r1 = 0.1 #m, pipe radius
r2 = 0.15 #m, outer pipe radius
n = 100 # of nodes used

m1 = 3 #kg/s, mass flow rate
Cp1 = 4180 #J/kG*K, heat capacity of fluid (water)
rho1 = 1000 #kg/m^3, density of fluid (water)

m2 = 5 #kg/s, mass flow rate
Cp2 = 4180 #J/kG*K, heat capacity of fluid (water)
rho2 = 1000 #kg/m^3, density of fluid (water)
pi = 3.14159

Ac1 = pi*r1**2 #m^2, cross-sectional area of inner pipe
Ac2 = pi*(r2**2-r1**2) #m^2, cross-sectional area of outer pipe/annulus

T1i = 400 #K, inlet temperature
T2i = 600 #K, pipe inner surface temperature
Te = 300 #K, initial temperature of fluid throughout the pipe

U = 340 #W/m^2*K, overall heat transfer coefficient

dx = L/n #m, node width I
t_final = 1000 #s, simulation time
dt = 1 #s, time step

x = np. linspace (dx/2, L-dx/2, n)
T1 = np.ones(n)*Te
T2 = np.ones(n)*Te
dT1dt = np.zeros (n)
dT2dt = np.zeros (n)

t = np.arange(0, t_final, dt)

T1_list = []
T2_list = []
q1_list = []
q2_list = []
plt.axis([0, L, 298, 820])
plt.xlabel('Distance (m)')
plt.ylabel ('Temperature (k)')
plt.legend(loc = 'upper right')

for j in range(1,len(t)):

    dT1dt[1:n] = (m1*Cp1*(T1[0:n-1]-T1[1:n])+U*2*pi*r1*dx*(T2[1:n]-T1[1:n]))/(rho1*Cp1*dx*Ac1) 
    dT1dt[0] = (m1*Cp1*(T1i-T1[0])+U*2*pi*r1*dx*(T2[0]-T1[0]))/(rho1*Cp1*dx*Ac1)

    dT2dt[1:n] = (m2*Cp2*(T2[0:n-1]-T2[1:n])-U*2*pi*r1*dx*(T2[1:n]-T1[1:n]))/(rho2*Cp2*dx*Ac2)
    dT2dt [0] = (m2*Cp2*(T2i-T2[0])-U*2*pi*r1*dx*(T2[0]-T1[0]))/(rho2*Cp2*dx*Ac2)

    T1 = T1+dT1dt*dt
    T2 = T2+dT2dt*dt


    q1 = m1*Cp1*(T1[n-1]-T1i)
    q2 = m2*Cp2*(T2i-T2[n-1])
    
    plt.ion()
    fig=plt.figure(1)
    plt.plot(x, T1, color = 'blue', label = 'Inside')
    plt.plot(x, T2, color = 'red', label = 'Outside')
    plt.show()
    fig.canvas.flush_events()
"""
    fig, ax = plt.subplots()

    line, = ax.plot(x, T1, color = 'blue', label = 'Inside')


    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line,


    ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
"""

    

"""
    fig = plt.figure() 
    axis = plt.axes([0, L, 298, 820]) 
  
    line, = axis.plot([], [], lw = 2) 
    
    # what will our line dataset
    # contain?
    def init(): 
        line.set_data([], []) 
        return line, 
    
    # initializing empty values
    # for x and y co-ordinates
    xdata, ydata = [], [] 
    
    # animation function 
    def animate(i): 
        # t is a parameter which varies
        # with the frame number
        t = 0.1 * i 
        
        # x, y values to be plotted 
        x = t * np.sin(t) 
        y = t * np.cos(t) 
        
        # appending values to the previously 
        # empty x and y data holders 
        xdata.append(x) 
        ydata.append(y) 
        line.set_data(xdata, ydata) 
        
        return line,
    
    # calling the animation function     
    anim = animation.FuncAnimation(fig, animate, init_func = init, frames = 500, interval = 20, blit = True) 
    plt.show()

    # saves the animation in our desktop
    # anim.save('growingCoil.mp4', writer = 'ffmpeg', fps = 30)


fig, ax = plt.subplots()

line, = ax.plot(x, T1_list, color = 'blue', label = 'Inside')


def animate(i):
    line.set_ydata(np.sin(x + i / 50))  # update the data.
    return line,

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
"""

#print(T1_list,T2_list,q1_list,q2_list)
plt.figure(1)
plt.plot(x, T1, color = 'blue', label = 'Inside')
plt.plot(x, T2, color = 'red', label = 'Outside')
plt.show()
plt.close(all)

