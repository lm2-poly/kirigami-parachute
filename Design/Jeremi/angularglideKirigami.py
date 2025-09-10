#Design space representation for the angular glide kirigami
#Author: Danick Lamoureux
#Modification by Jérémi Fillion

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

if __name__ == '__main__':
    
    # Size parameters
    r_int = 21           #Inner radius for payload (mm)
    ro = 200            #Outer radius (mm)
    delta_r1 = 10        #Distance between center hole and first slit (mm)

    #Geometric parameters of side 1
    Theta1 = 0.4         #Material/slit ratio
    N_theta1 = 3         #Number of angular slits
    N_r1 = 11            #Number of radial slits
    ratio = 0.33          #Percentage of full circle

    #Geometric parameters of side 2
    Theta2 = 0.1        #Material/slit ratio
    N_theta2 = 3         #Number of angular slits
    N_r2 = 11            #Number of radial slits
    #------------------------------------------------------
    
    r1 = r_int + delta_r1
    dx0 = r1/ro
    
    R_inch=ro/25.4 
    dxi=r_int/ro
  
    #Granularity for the graphs
    N = 100
    plt.figure(figsize=(2*R_inch,2*R_inch)) #scaling
    
    #Solve for side 1
    #Angular parameters
    ratio1 = ratio
    N_theta1 = round(N_theta1*ratio1)
    func = lambda thetaL: ratio1*2*np.pi - N_theta1*thetaL*(1+Theta1)
    thetaL = fsolve(func, 0.2)[0]
    
    #Radial parameters
    func = lambda dx1: dx0 + dx1 * N_r1 - 1
    dx1 = fsolve(func, 0.1)[0]
     
    R = dx0
    x = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    
    for i in range(N_r1):
        for j in range(N_theta1):
            xs = []
            ys = []
            if i%2 == 0:
                theta = j*ratio1*2*np.pi/N_theta1
            else:
                theta = (j+0.5)*ratio1*2*np.pi/N_theta1
            theta = theta
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
            dx = (1+dx) - 1
        R += dx

    #Solve for side 2
    #Angular parameters
    ratio2 = 1- ratio1
    N_theta2 = round(N_theta2*ratio2)
    func = lambda thetaL: ratio2*2*np.pi - N_theta2*thetaL*(1+Theta2)
    thetaL = fsolve(func, 0.2)[0]
    
    #Radial parameters
    func = lambda dx1: dx0 + dx1 * N_r2 - 1
    dx1 = fsolve(func, 0.1)[0]
    
    R = dx0
    x = lambda R, theta: np.array([R*np.sin(theta),
                                   R*np.cos(theta)])
    

    R = dx0
    for i in range(N_r2):
        for j in range(N_theta2):
            xs = []
            ys = []
            if i%2 == 0:
                theta = j*ratio2*2*np.pi/N_theta2
            else:
                theta = (j+0.5)*ratio2*2*np.pi/N_theta2
            theta = theta + ratio1 * 2 * np.pi
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
            dx = (1+dx) - 1
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
    
    xs = []                     #inner hole
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
    plt.savefig('glide14.pdf')
    plt.show()