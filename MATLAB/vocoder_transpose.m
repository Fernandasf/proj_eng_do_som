function [ x ] = vocoder_transpose( y, fscale )
    x1=vocoder(y,1/fscale);
    
    x=zeros(round(length(x1)/fscale)+1,1);
    
    for i=2:length(x)+1
       j=i*fscale;
       jnext=ceil(j);
       jprev=floor(j);
       if(jnext<=length(x1))
           if(jnext~=jprev)
              x(i)=x1(jprev) + (j-jprev)*(x1(jnext)-x1(jprev))/(jnext-jprev);
           else
              x(i)=x1(j); 
           end
       end
    end

end

