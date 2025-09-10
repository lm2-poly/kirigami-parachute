%General template to save figures
%Author: Danick Lamoureux

function figureSaver(fig, filename)
    grid off;
    %fig.Position = [50 150 450 300];
    
    %https://www.mathworks.com/matlabcentral/answers/554344-how-to-remove-the-margins-of-a-plot
%     ax = gca;
%     outerpos = ax.OuterPosition;
%     ti = ax.TightInset; 
%     left = outerpos(1) + ti(1);
%     bottom = outerpos(2) + ti(2);
%     ax_width = outerpos(3) - ti(1) - ti(3);
%     ax_height = outerpos(4) - ti(2) - ti(4);
%     ax.Position = [left bottom ax_width ax_height];

    set(gca,'FontSize',12)
    set(fig, 'color', 'white');    
    exportgraphics(gcf, filename,...
        'ContentType','vector',...
        'BackgroundColor','none', ...
        'Resolution',600)
end