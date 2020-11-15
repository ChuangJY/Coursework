function ber_log10 = BER_CAL(mod, ebno_dB)
    ebno = 10^(ebno_dB/10);
    if mod == 'BPSk' || mod == 'QPSK'
        BER = 0.4*erfc(sqrt(ebno));
    elseif mod == '8-PSK' || mod == '16-PSK' || mod == '32-PSK' || mod == '64-PSK'
        M = sscanf(mod, '%d-PSK');
        m = log2(M);
        BER = (1/m)*erfc(sqrt(m*ebno)*sin(pi/M));
    elseif mod == '4-QAM' || mod == '16-QAM' || mod == '64-QAM'
        M = sscanf(mod, '%d-QAM');
        m = log2(M);
        BER = (2/m)*(1-1/sqrt(M))*erfc(sqrt(1.5*EbNo*k/(j1-1)));
    elseif mod == 'D-BPSK'
        BER = 0.5*exp(-1.*EbNo);
    end
    ber_log10 = log10(BER);
end