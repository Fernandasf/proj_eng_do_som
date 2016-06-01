
Fs=44100;

t=0:1/fs:3;
t=t';

y=sin(440*2*pi*t);

x=vocoder(y,1);
sound(x,Fs);
%