#Design space representation for the chiralf kirigami
#Author: Danick Lamoureux
#Modification by Jérémi Fillion

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

if __name__ == '__main__':
    
    #Size parameters
    ro=100              #Outer radius (mm)
    r_int=3             #Inner radius for payload (mm)
    sp_int = 0.35        #Inner spacing (0=none)
    sp_o = 0.96         #Outer spacing (1=none)
    
    #Geometric parameters
    N_theta = 8         #Number of spirals
    N_r = 0.75          #Number of loops of each spiral
    #-----------------------

    R_inch=ro/25.4 
    dxi=r_int/ro
    
    #Rate of growth
    Rf = lambda b: b*N_r*(2*np.pi)
    func = lambda b: Rf(b) - sp_o
    b = fsolve(func, 1/N_r)[0]
    
    #Angular spacing    
    dtheta = 2*np.pi/N_theta
    
    #Radial position
    R = lambda theta: b*theta
    xpos = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    
    #Granularity for the graphs
    N = 1000
        
    #Plot
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling
    theta = np.linspace(0, N_r*2*np.pi, N)
    Ri = R(theta)
    x=[]
    y=[]
    
    for i in range(N_theta):
        for j in range(len(Ri)):
            if Ri[j] >= sp_int:
                x.append(Ri[j]*np.cos(theta[j] + i*dtheta))
                y.append(Ri[j]*np.sin(theta[j] + i*dtheta))
        plt.plot(x, y, '-b')
        x.clear()
        y.clear()

    thetac = np.linspace(0, 2*np.pi, N)
    x = np.cos(thetac)
    y = np.sin(thetac)
    plt.plot(x, y, '-r')
    
    #Inner hole
    x = dxi*np.cos(thetac)
    y = dxi*np.sin(thetac)
    plt.plot(x, y, '-r')
    
    plt.axis([-1,1,-1,1])
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('Chiralf9.pdf')
    plt.show()
        