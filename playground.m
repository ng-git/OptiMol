close all; clear ll; clc;

a = [1 0;
    2 0;
    3 3];

b = [1 0;
    3 3;
    2 0];

c = [a;b];

[s,d] = eig(c*c')