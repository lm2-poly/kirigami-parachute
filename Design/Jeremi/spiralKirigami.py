#Design space representation for the spiral kirigami
#Author: Danick Lamoureux
#Modification by Jérémi Fillion

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

if __name__ == '__main__':
    
    #Size parameters
    ro=100          #Outer radius (mm)
    r_int=3          #Inner radius for payload (mm)
    sp_int = 0.1       #Inner spacing (0=none)
    sp_o = 0.9       #Outer spacing (1=none)
    
    #Geometric parameters
    N_theta = 12      #Number of spirals
    N_r = 0.25        #Number of loops of each spiral (1=360deg)
    
    #-----------------------

    R_inch=ro/25.4 
    dxi=r_int/ro
    
    #Rate of growth
    Rf = lambda b: sp_int + b*N_r*(2*np.pi)
    func = lambda b: Rf(b) - sp_o
    b = fsolve(func, 1/N_r)[0]
    
    #Angular spacing    
    dtheta = 2*np.pi/N_theta
    
    #Radial position
    R = lambda theta: sp_int + b*theta
    xpos = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    
    #Granularity for the graphs
    N = 100
        
    #Plot
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling
    theta = np.linspace(0, N_r*2*np.pi, N)
    
    for i in range(N_theta):
        Ri = R(theta)
        x = Ri*np.cos(theta + i*dtheta)
        y = Ri*np.sin(theta + i*dtheta)
        plt.plot(x, y, '-b')
        
            
    
    theta = np.linspace(0, 2*np.pi, N)
    x = np.cos(theta)
    y = np.sin(theta)
    plt.plot(x, y, '-r')
    
    #little hole in the center for wind tunnel
    theta = np.linspace(0, 2*np.pi, N)
    x = dxi*np.cos(theta)
    y = dxi*np.sin(theta)
    plt.plot(x, y, '-r')
    
    plt.axis([-1,1,-1,1])
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('Spiral2.pdf')
    plt.show()
        