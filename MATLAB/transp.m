function [ transp_ft ] = transp( ft, factor )

transp_ft=zeros(1,length(ft));
if factor>=1;
    for i=round( length(ft)/2*(1/factor) ):-1:1
        transp_ft(round(i*factor))=ft(i);
    end

   
end

if factor<1
    for i=round(length(ft)/2):-1:1
        transp_ft(round(i*factor))=ft(i);
    end  
end

for i=1:length(ft)/2
        transp_ft(length(ft)-(i-1))=transp_ft(i+1)*exp(-1i*2*(angle(transp_ft(i+1))));
end