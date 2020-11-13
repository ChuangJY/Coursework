clc;
%clear;

EARTH_RADIUS_KM = 6378;
GEO_ALTITUDE = 35768;
BOLTZMANNS_CONSTANT_dB_Hz_K = -228.6;

up_or_down = input("Uplink or downlink (U/d)?: ", 's');
if up_or_down == 'U' || up_or_down == 'u'
    bit_rate = input("Bit rate: ");
    tx_long = input("Earth station longitude: ");
    tx_lat = input("Earth station latitude: ");
    tx_al = input("Earth station altitude: "); 
    tx_freq = input("Transmitting frequency (MHz): ");
    tx_power = input("Transmitter power (dB): ");
    tx_antenna_gain = input("Transmitter antenna gain (dBi): ");
    tx_cable_loss = input("Transmitter cable loss (dB): ");
    
    rain = input("Rain attenuation (dB): ");
    back_off = input("Transmitter back off power (dB): ");
    additional = input("Additional path loss (dB): ");
    
    rx_long = input("Satellite longitude: ");
    rx_gain = input("Receiver antenna gain (dBi): ");
    rx_noise = input("Receiver noise temperature (K): ");
    rx_bw = input("Receiver bandwidth (Hz): ");
    rx_noise_figure = input("Receiver noise figure: ");
    rx_cable_loss = input("Receiver cable loss (dB): ");
    safe_margin = input("S/R additional margin (dB): ");
    rx_required_s_to_n = input("Required S/N: ");
else
    bit_rate = input("Bit rate: ");
    tx_freq = input("Transmitting frequency (MHz): ");
    tx_power = input("Transmitter power (dB): ");
    tx_antenna_gain = input("Transmitter antenna gain (dBi): ");
    tx_cable_loss = input("Transmitter cable loss (dB): ");
    
    rain = input("Rain attenuation (dB): ");
    back_off = input("Transmitter back off power (dB): ");
    additional = input("Additional path loss (dB): ");
    
    tx_long = input("Earth station longitude: ");
    tx_lat = input("Earth station latitude: ");
    rx_long = input("Earth station altitude: ");
    rx_gain = input("Receiver antenna gain (dBi): ");
    rx_noise = input("Receiver noise temperature (K): ");
    rx_bw = input("Receiver bandwidth (Hz): ");
    rx_noise_figure = input("Receiver noise figure: ");
    rx_cable_loss = input("Receiver cable loss (dB): ");
    safe_margin = input("S/R additional margin (dB): ");
    rx_required_s_to_n = input("Required S/N: ");
end

tx_eirp = tx_power + tx_antenna_gain - tx_cable_loss - back_off;

a = (EARTH_RADIUS_KM + tx_al);
b = (EARTH_RADIUS_KM + GEO_ALTITUDE);
delta = abs(rx_long - tx_long);
slant_range = sqrt(a^2 + b^2 - 2*a*b*cos(delta)*cos(tx_lat));
fspl = 20*log10(slant_range) + 20*log10(tx_freq) + 32.4;

received_signal_power = tx_eirp + rx_gain - fspl - rain - additional;
receiver_noise_power = 10*log10(rx_bw*rx_noise*physconst('Boltzmann'));
receiver_s_to_n = received_signal_power - receiver_noise_power;

%3 bit per symbol, how many bit per second? 3 bit/symbol * freq symbol/s
% = 3*freq bit/s
required_eb_to_n0 = (10^(rx_required_s_to_n/10)/(bit_rate*tx_freq*10^6))*rx_bw;
receiver_eb_to_n0 = (10^(receiver_s_to_n/10)/(bit_rate*tx_freq*10^6))*rx_bw;

theoritical_BER = (1/bit_rate)*erfc(sqrt(required_eb_to_n0*bit_rate)*sin(pi/(2^bit_rate)));
receiver_BER = (10^(receiver_s_to_n/10)/(bit_rate*tx_freq*10^6))*rx_bw;