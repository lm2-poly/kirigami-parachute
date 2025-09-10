%Find the vertices of a polygon of N sides

clear all; close all; clc;

R = 1; %Distance from the origin to the vertices of the polygon
Ns = [4,5,6,7,8]; %Number of sides = number of vertices


figure();
for j = 1:length(Ns)
    N = Ns(j);
    [xs, ys] = getvertices(R, N);
    plot([xs, xs(1)], [ys, ys(1)], 'k');
    axis equal;
    pause(3);
end

function [xs, ys] = getvertices(R, N)
    xs = [];
    ys = [];
    for i = 1:N
        theta_i = i*2*pi/N;
        xs(end+1) = R*cos(theta_i);
        ys(end+1) = R*sin(theta_i);
    end
end