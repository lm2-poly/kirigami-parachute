#Design space representation
#Author: Danick Lamoureux

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def radialSlits(dx0, dx1, n, N_r):
    x = dx0 + dx1
    dx = dx1
    for i in range(N_r-1):
        dx = (1+dx)**n - 1
        x += dx
    return x

if __name__ == '__main__':
    
    #Size parameters
             
    R_ext=215           #outer radius in mm
    R_int=31           #inner radius in mm
    R_wind=21             #little hole in the center for the wind tunnel, radius in mm
  
    #Geometric parameters
 
    N_r = 30            #number of slits in radial direction
    N_theta = 5         #number of slits in angular direction
    n = 1             #exponential spacing in radial direction
    x_theta = 0.3       #linear spacing in angular direction
    #------------------------------------------------------
    
    
    dx0 = R_int/R_ext
    
    R_inch=R_ext/25.4 
    dxi=R_wind/R_ext
  

    #Granularity for the graphs
    N = 100
    
    #Solve for dependent parameters
    #Angular parameters
    func = lambda thetaL: 2*np.pi - N_theta*thetaL*(1+x_theta)
    thetaL = fsolve(func, 0.2)[0]
    thetaD = x_theta*thetaL
    
    #Radial parameters
    func = lambda dx1: radialSlits(dx0, dx1, n, N_r) - 1
    dx1 = fsolve(func, 0.1)[0]
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling 
    
    R = dx0
    x = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    
    for i in range(N_r):
        for j in range(N_theta):
            xs = []
            ys = []
            if i%2 == 0:
                theta = j*2*np.pi/N_theta
            else:
                theta = (j+0.5)*2*np.pi/N_theta
            theta = theta- thetaL/2
            dtheta = thetaL/(N-1)
            for k in range(N):
                theta_new = theta + k*dtheta
                newx = x(R, theta_new)
                xs.append(newx[0])
                ys.append(newx[1])
            plt.plot(xs, ys, c='b')
        if i == 0:
            dx = dx1
        else:
            dx = (1+dx)**n - 1
        R += dx
    
    xs = []                     #outer circle
    ys = []
    dtheta = 2*np.pi/(N-1)
    for k in range(N):          
        theta_new = k*dtheta
        newx = x(R, theta_new)
        xs.append(newx[0])
        ys.append(newx[1])
    plt.plot(xs, ys, c='r')
    
    xs = []                     #little hole in the center for wind tunnel
    ys = []
    dtheta = 2*np.pi/(N-1)
    R=dxi
    for k in range(N):
        theta_new = k*dtheta
        newx = x(R, theta_new)
        xs.append(newx[0])
        ys.append(newx[1])
    plt.plot(xs, ys, c='r') 

    plt.axis([-1,1,-1,1])
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('noir1.pdf')
    plt.show()