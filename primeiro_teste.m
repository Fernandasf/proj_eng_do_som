close all

fs=8000;

rec= audiorecorder;
disp('fale')
recordblocking(rec,10);
disp('ok')
y=getaudiodata(rec);

t=0:1/fs:1;

%y=sin(2*pi*80*t)+0.5*sin(2*pi*160*t);
%y=tri(2*pi*220*t);
n=2;
fact=1*2^(n/12);


ft=fft(y);
freqs=0:length(ft)-1;
freqs=freqs*fs/length(ft);

plot(freqs,abs(ft))

transp_ft=transp(ft,fact);
figure
plot(freqs,abs(transp_ft));

transp_y=ifft(transp_ft);

%plot(t,transp_y);

%sound(y,fs)
sound(real(transp_y),fs)