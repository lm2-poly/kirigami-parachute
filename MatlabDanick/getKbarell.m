function Kbarell = getKbarell(Re, beta, dxmin, dx, n, rtheta, Ntheta)
    [Kbar, ell, epsKC] = getKirigamiValues(Re, Re*beta, dxmin*Re, dx, n, Ntheta, rtheta);
    Kbarell = Kbar*ell;
% if rtheta ~= 0 && dx > dxmin
%     drmin = dxmin*Re;
% 
%     thetaL = 2*pi/(Ntheta*(1+rtheta));
%     thetaD = rtheta*thetaL;
% 
%     %Calculating drs
%     dxi = dx;
%     x = beta + dxi;
%     dxis = [dxi];
% 
%     Nr = 0;
%     while x < 1
%         dxi = (1+dxi)^1 - 1;
%         if 1 - x > dxmin
%             x = x + dxi;
%             dxis(end+1) = dxi;
%             Nr = Nr + 1;
%         else
%             x = 1;
%             dxis(end+1) = dxi;
%         end
%     end
%             
%     x = beta;
%     
%     eps = 0;
%     
%     invKbar = 0;
%     Le = 0;
%     
%     for m = 1:1:Nr
%         xjbar = x + dxis(m)/2;
%         
%         eps = eps + dxis(m)*xjbar;
%         invKbar = invKbar + xjbar^3/dxis(m);
%         Le = Le+xjbar;
%         
%         x = x + dxis(m);
%     
%     end
%     
%         Kbar = ((3*Ntheta^4)/(2*pi^3*invKbar))*((1+rtheta)/(1-rtheta))^3;
%         ell = pi*Le*(1-rtheta)/(Ntheta*(1+rtheta));
%         Kbarell = Kbar*ell;
%     else
%         Kbarell = NaN;
%     end
%     fprintf("dx = %f\t rtheta = %f\t Kbarell = %f\n", dx, rtheta, Kbarell);
end