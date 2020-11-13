clc                       %for clearing the command window
close all                 %for closing all the window except command window
clear all                 %for deleting all the variables from the memory
nPSK=3;                   %8PSK 
nSymbol=100000;           %Number of Input Symbol
nbit=nSymbol*nPSK;        %Number of Input Bit 
Eb=1;                     %Energy Bit
itr=20;                   %Number of Iteration 
BER=1:itr;                %Bit Error Rate
real=0;                   %real part
img=0;                    %imag part 
for SNRdb=1:1:itr         % SNR in dB
    counter=0;  
    SNR=10.^(SNRdb/10);
    No=1/SNR;
    v=(No/Eb)/(2*nPSK);   % Noise Equation
for n=1:1:nSymbol
    u1=rand(1);           %random first bit generation 
    u2=rand(1);           %random second bit generation
    u3=rand(1);           %random third bit generation 
    
    u1=round(u1);         %round first bit to(1 or 0)
    u2=round(u2);         %round second bit to(1 or 0)
    u3=round(u3);         %round third bit to(1 or 0) 
    
   %Modulation Process
    if(u1==0 && u2==0 && u3==0)
        real=cosd(0);
        img=sind(0);
 
    elseif(u1==0 && u2==0 && u3==1)
        real=cosd(45);
        img=sind(45);
        
       
     elseif(u1==0 && u2==1 && u3==0)
        real=cosd(90);
        img=sind(90);
            
     elseif(u1==0 && u2==1 && u3==1)
        real=cosd(135);
        img=sind(135);
               
     elseif(u1==1 && u2==0 && u3==0)
        real=cosd(180);
        img=sind(180);
                
     elseif(u1==1 && u2==0 && u3==1)
        real=cosd(225);
        img=sind(225);
                
     elseif(u1==1 && u2==1 && u3==0)
        real=cosd(270);
        img=sind(270);
                
     elseif(u1==1 && u2==1 && u3==1)
        real=cosd(315);
        img=sind(315);
               
    end
    
   %Transmition Process
    AWGN1=sqrt(v)*randn(1);
    AWGN2=sqrt(v)*randn(1);
    
   %Channel
    realn=real+AWGN1;          
    imgn=img+AWGN2;
    
   %RX
    phin=mod(atan2d(imgn,realn)+360,360);
    
   if((phin>=0&&phin<=22.5)||(phin>337.5))
        uu1=0;
        uu2=0;
        uu3=0;
    elseif(phin>22.5&&phin<=67.5)
        uu1=0;
        uu2=0;
        uu3=1;
        
    elseif(phin>67.5&&phin<=112.5)
        uu1=0;
        uu2=1;
        uu3=0;
                  
    elseif(phin>112.5&&phin<=157.5)
        uu1=0;
        uu2=1;
        uu3=1;
               
       elseif(phin>157.5&&phin<=202.5)
        uu1=1;
        uu2=0;
        uu3=0;
                
        elseif(phin>202.5&&phin<=247.5)
        uu1=1;
        uu2=0;
        uu3=1;
               
        elseif(phin>247.5&&phin<=292.5)
        uu1=1;
        uu2=1;
        uu3=0;
                
        elseif(phin>292.5&&phin<=337.5)
        uu1=1;
        uu2=1;
        uu3=1;
                
    end
    %Detection Process
    if(u1~=uu1)          %logic according to 8PSK
        counter=counter+1;
    end
    if(u2~=uu2)          %logic according to 8PSK
        counter=counter+1;
    end
    if(u3~=uu3)        %logic according to 8PSK
        counter=counter+1;
    end
 
end
BER(SNRdb)=(counter/nbit);  %Calculate error/bit
end
SNRdb=1:1:itr;
th=(1/nPSK)*erfc(sqrt((10.^(SNRdb/10))*nPSK)*sin(pi/(2^nPSK)));                  %theoretical Eq.of BER for 8psk                  
figure('name','BER_8PSK','numbertitle','off');
 
%plot start
semilogy(SNRdb,BER,'--g*','linewidth',1.5,'markersize',8);
axis([1 itr 10^(-4) 1]);
xlabel('SNR(dB)');
ylabel('BER');
hold on;
semilogy(SNRdb,th,'--bs','linewidth',1.5,'markersize',6);
axis([1 itr 10^(-4) 1]);
title(' curve for Bit Error Rate VS. SNR for 8PSK modulation');
xlabel(' SNR(dB)');
ylabel('BER');
legend('simulation','theoretical');
hold on;
grid on;
