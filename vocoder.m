function [ sigout ] = vocoder( signalin, tscale )

    N=2048;
    H=N/4;
    L=length(signalin);
    
    phi=zeros(N,1);
    sigout=zeros(round(L/tscale+N)+1,1);
    
    win=hann(N);
    p=1;
    pp=1;
    
    while p< L-(N+H) +1
        p1=round(p);
        spec1=fft(win.*signalin(p1:p1+N-1));
        spec2=fft(win.*signalin(p1+H:p1+N+H-1));
        
        dif=(angle(spec2)-angle(spec1));
        phi=phi+dif;
        out=cos(phi) + 1i*sin(phi);
        
        sigout(pp:pp+N-1) = sigout(pp:pp+N-1) + win.*ifft(abs(spec2).*out);
        pp = pp+H;
        p= p+H*tscale;
    end
    sigout=max(signalin)*sigout/max(sigout);
    sigout=real(sigout);

end

