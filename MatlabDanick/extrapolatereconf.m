%Function to interpolate the drag ratio
%Author: Danick Lamoureux

function R = extrapolatereconf(CYCDs, Rs, CYCD)
    minCYCD = min(CYCDs);
    maxCYCD = max(CYCDs);
    R = zeros(length(CYCD),1);
    for i = 1:length(CYCD)
        CYCDi = CYCD(i);
        if CYCDi > maxCYCD
            m = log10(Rs(end)/Rs(end-1))/log10(CYCDs(end)/CYCDs(end-1));
            a = Rs(end)/CYCDs(end)^m;
            R(i) = a*CYCDi^m;
        elseif CYCDi < minCYCD
            R(i) = 1;        
        else
            R(i) = interp1(CYCDs, Rs, CYCDi);
        end
    end
end