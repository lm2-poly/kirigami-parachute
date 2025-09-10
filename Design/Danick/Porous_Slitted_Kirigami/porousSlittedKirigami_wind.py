#Design space representation for the porous slit design
#Author: Danick Lamoureux

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def radialSlits(d_int, dx1, N_r):
    x = d_int + dx1
    dx = dx1
    for i in range(N_r-1):
        x += dx
    return x

if __name__ == '__main__':
    
    #Size parameters

    R_ext=60          #outer radius in mm
    R_wind=2          #little hole in the center for the wind tunnel, radius in mm
    
    #Geometric parameters
    
    N_r = 40          #number of slits in radial direction
    N_theta = 8      #number of slits in angular direction
    d_int = 0.1       #linear Inner spacing
    x_theta = 0.1     #linear spacing in angular direction
    #---------------------------------------

    
    R_inch=R_ext/25.4 
    dxi=R_wind/R_ext
    
    
    #Granularity for the graphs
    N = 100
    
    #Solve for dependent parameters
    #Angular parameters
    func = lambda thetaL: 2*np.pi - N_theta*thetaL*(1+x_theta) #x_theta = thetad/thetaL
    thetaL = fsolve(func, 0.2)[0]
    thetaD = x_theta*thetaL
    
    #Radial parameters
    func = lambda dx1: radialSlits(d_int, dx1, N_r) - 1
    dx = fsolve(func, 0.1)[0]
    
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling
 
    R = d_int
    x = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    for i in range(N_r):
        for j in range(N_theta):
            xs = []
            ys = []
            theta = j*2*np.pi/N_theta
            theta = theta- thetaL/2
            dtheta = thetaL/(N-1)
            for k in range(N):
                theta_new = theta + k*dtheta
                newx = x(R, theta_new)
                xs.append(newx[0])
                ys.append(newx[1])
            plt.plot(xs, ys, c='b')
            
        R += dx
        
    for j in range(N_theta):
        theta = (j+0.5)*2*np.pi/N_theta            
        
        xs = np.array([x(d_int, theta)[0], x(1, theta)[0]])
        ys = np.array([x(d_int, theta)[1], x(1, theta)[1]])
        plt.plot(xs, ys, 'b')
    
    xs = []
    ys = []
    dtheta = 2*np.pi/(N-1)
    for k in range(N):
        theta_new = k*dtheta
        newx = x(1, theta_new)
        xs.append(newx[0])
        ys.append(newx[1])
    plt.plot(xs, ys, c='r')
    
    #little hole in the center for wind tunnel
    theta = np.linspace(0, 2*np.pi, N)
    x = dxi*np.cos(theta)
    y = dxi*np.sin(theta)
    plt.plot(x, y, '-r')
    
    plt.axis([-1,1,-1,1])
    plt.axis("off")
    plt.tight_layout(pad=0)
    #plt.savefig('PO1_wind.pdf')
    plt.show()
