function ERR = getRegressionError(allx, ally, modelfun)
    ERR = 0;
    for i = 1:length(allx)
        ERR = ERR + (modelfun(allx(i)) - ally(i)).^2;
    end
end