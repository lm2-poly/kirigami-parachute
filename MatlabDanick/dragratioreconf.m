%Function to interpolate the drag ratio
%Author: Danick Lamoureux

function R = dragratioreconf(CYCDs, Ds, CYCD)
    minCYCD = min(CYCDs);
    maxCYCD = max(CYCDs);
    R = zeros(length(CYCD), 1);
    for i = 1:length(CYCD)
        if CYCD(i) > maxCYCD
            m = log10(Ds(end)/Ds(end-1))/log10(CYCDs(end)/CYCDs(end-1));
            a = Ds(end)/CYCDs(end)^m;
            D = a*CYCD(i)^m;
        elseif CYCD(i) < minCYCD
            D = 0.5*CYCD(i);        
        else
            D = interp1(CYCDs, Ds, CYCD(i));
        end
        if CYCD(i) == 0
            R(i) = 1;
        else
            R(i) = D/(0.5*CYCD(i));
        end
    end
end