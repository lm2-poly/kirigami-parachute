#Design space representation for the spiral-slit kirigami
#Author: Danick Lamoureux

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

if __name__ == '__main__':
    #Dimensions
    d0 = 0.2 #Inner spacing
    df = 0.9 #Outer spacing
    
    #Parameters
    Ntheta = 4 #Number of spirals
    Nr = 0.25 #Number of loops of each spiral
    rtheta = 0.4 #Ratio of angular spacing between spiral and angular slits to slits length
    Nslits = 40 #Number of radial slits

    
    #-----------------------

    #parameters for printing
    R_mm=60          #outer radius in mm
    dri=2            #little hole in the center for the wind tunnel, radius in mm
    R_inch=R_mm/25.4 
    dxi=dri/R_mm
    
    #Calculations
    #Rate of growth
    Rf = lambda b: d0 + b*Nr*(2*np.pi)
    func = lambda b: Rf(b) - df
    b = fsolve(func, 1/Nr)[0]
    
    #Angular spacing    
    dtheta = 2*np.pi/Ntheta
    
    #Angular slit spacing
    dspacing = rtheta*dtheta
    dslit = dtheta - dspacing
    rspacing = (df-d0)/(Nslits)
    
    #Radial position
    R = lambda theta: d0 + b*theta
    xpos = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    
    #Granularity for the graphs
    N = 100
        
    #Plot
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling
    theta = np.linspace(0, Nr*2*np.pi, N)
    
    for i in range(Ntheta):
        Ri = R(theta)
        x = Ri*np.cos(theta + i*dtheta)
        y = Ri*np.sin(theta + i*dtheta)
        plt.plot(x, y, '-b')
        
       
        Rslit = d0
        for j in range(Nslits):
            current_theta = i*dtheta + (Rslit - d0)/b
            start = current_theta + dspacing/2
            end = start + dslit
            
            slittheta = np.linspace(start, end, N)
            x = Rslit*np.cos(slittheta)
            y = Rslit*np.sin(slittheta)
            plt.plot(x,y, '-b')
            Rslit += rspacing
      
            
    
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
    plt.savefig('SS2_wind.pdf')
    plt.show()
        