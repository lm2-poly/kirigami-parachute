%Function to calculate the theoretical stiffness of a beam
%Author: Danick Lamoureux

function [Kbar, ell, epsKC, beta, slitLength, Nr] = getKirigamiValues(Re, Ri, drmin, dx, n, Ntheta, rtheta)
    dxmin = drmin/Re;
    beta = Ri/Re;
    thetaL = 2*pi/(Ntheta*(1+rtheta));
    thetaD = rtheta*thetaL;

    %Calculating drs
    dxi = dx;
    x = beta + dxi;
    dxis = [dxi];

    Nr = 0;
    while x < 1
        dxi = (1+dxi)^n - 1;
        if 1 - x > dxmin
            x = x + dxi;
            dxis(end+1) = dxi;
            Nr = Nr + 1;
        else
            x = 1;
            dxis(end+1) = dxi;
        end
    end
            
    x = beta;
    
    eps = 0;
    
    invKbar = 0;
    beta_num = 0;
    beta_denum = 0;
    Le = 0;
    slitLength = 0;
    
    for m = 1:1:Nr
        xjbar = x + dxis(m)/2;
        
        eps = eps + dxis(m)*xjbar.^5;
        invKbar = invKbar + xjbar^3/dxis(m);
        Le = Le+xjbar;
        
        beta_num = beta_num + xjbar.^2*dxis(m);
        beta_denum = beta_denum + dxis(m)./xjbar;
        
        slitLength = slitLength + xjbar;
        x = x + dxis(m);
        
    
    end
    epsKC = eps*((1-rtheta)/(1+rtheta))^5/Ntheta^4;
    Kbar = ((24*Ntheta^4)/(pi^3*invKbar))*((1+rtheta)/(1-rtheta))^3;
    ell = pi*Le*(1-rtheta)/(Ntheta*(1+rtheta));
    slitLength = Re*slitLength*2*pi*(1-rtheta);
    beta = (beta_num/beta_denum)*((1-rtheta)/(1+rtheta))^3/Ntheta^3;
end

