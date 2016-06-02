close all

tscale=.5;
N=64;
H=N/4;

fs=44100;
f=440;
t=0:1/fs:3/f;

y=sin(2*pi*f*t);

plot(t,y);

x1=y(1:N);
x1d(H+1:H+N+1)=y(H*tscale:H*tscale+N)
figure
hold on
plot(t,y);
plot(t(1:length(x1)),x1,'g')
plot(t(1:length(x2)),x2,'r')

