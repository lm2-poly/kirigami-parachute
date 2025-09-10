%Function to calculate the theoretical stiffness of a beam
%Author: Danick Lamoureux

function [K, Kflu, L, perimeter] = getStiffness(Re, Ri, t, E, dr, n, Ntheta, rtheta)
    %Get beam properties from kirigami
    %Solve for dependent parameters
    %Angular parameters
    thetaL = 2*pi/(Ntheta*(1+rtheta));
    thetaD = rtheta*thetaL;

    %Calculating drs
    dxmin = dr/Re;
    dx = dxmin;
    x = Ri/Re + dx;
    dr = [dxmin*Re];

    Nr = 0;
    while x < 1
        dx = (1+dx)^n - 1;
        if 1 - x > dxmin
            x = x + dx;
            dr(end+1) = (dx*Re);
            Nr = Nr + 1;
        else
            x = 1;
            dr(end+1) = (dx*Re);
        end
    end
            
    r = Ri;
    B = E*t^3/12;
    
    invK = 0;
    invKflu = 0;
    L = 0;
    perimeter = 2*pi*Re;
    
    for j = 1:1:Nr
        
        perimeter = perimeter + thetaL*r;
        
        rjbar = r + dr(j)/2;
        
        invKflu = invKflu + rjbar^4;

        invK = invK + rjbar^3/dr(j);
        L = L + pi*rjbar*(1-rtheta)/(Ntheta*(1+rtheta));
        r = r + dr(j);
    
    end
    Kflu = (Ntheta^5*E*t^3/(40*pi^4))*((1+rtheta)/(1-rtheta))^4/invKflu;
    K = (Ntheta^4*E*t^3/(8*pi^3))*((1+rtheta)/(1-rtheta))^3/invK;
end

