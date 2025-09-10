%Function to interpolate the drag ratio
%Author: Danick Lamoureux

function D = dragratio(CYCDs, Ds, CYCD)
    minCYCD = min(CYCDs);
    maxCYCD = max(CYCDs);
    if CYCD > maxCYCD
        m = log10(Ds(end)/Ds(end-1))/log10(CYCDs(end)/CYCDs(end-1));
        a = Ds(end)/CYCDs(end)^m;
        D = a*CYCD^m;
    elseif CYCD < minCYCD
        D = 0.5*CYCD;        
    else
        D = interp1(CYCDs, Ds, CYCD);
    end
end