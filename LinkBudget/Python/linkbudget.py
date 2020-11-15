import math
from prettytable import PrettyTable
from constant import *

table = PrettyTable()
table.field_names = ['Direction', 'Description', 'Unit', 'G(+)/L(-)', 'Value']
table.align['Description'] = "l"
table.align['Unit'] = "c"
table.align['G(+)/L(-)'] = "c"
table.align['Value'] = "c"

def link_budget_calculation(
    direction,
    transmitter_maximum_input_power,
    transmitter_minimum_input_power,
    transmitter_antenna_gain,
    system_cable_loss,
    transmitter_freq_min,
    transmitter_freq_max,
    transmitter_back_off_power,
    rain_attenuation,
    es_longitude,
    es_latitude,
    es_altitude,
    sat_longitude,
    sat_beam_gain,
    receiver_bandwidth,
    system_noise_temperature,
    implementation_margin,
    system_c_to_n,
    bit_per_second
):
    table.add_row([direction,' ', '', '', ''])
    table.add_row(['','Transmitter power', 'dBW', '+', transmitter_minimum_input_power])
    table.add_row(['','Transmitter antenna gain', 'dBi', '+', transmitter_antenna_gain])
    table.add_row(['','Transmitter cable loss', 'dBW', '-', system_cable_loss])
    table.add_row(['','Transmitter back-off power', 'dB', '-', transmitter_back_off_power])
    transmitted_power = transmitter_minimum_input_power + transmitter_antenna_gain - system_cable_loss - transmitter_back_off_power
    table.add_row(['','Transmitter eirp', 'dBW', '', transmitted_power])  # derived
    table.add_row(['','', '', '', ''])

    d = slant_range(EARTH_RADIUS_KM + es_altitude/1000, EARTH_RADIUS_KM + SAT_ALTITUDE_KM, es_longitude-sat_longitude, es_latitude)
    table.add_row(['','Slant range', 'km', '', d])
    fspl = FSPL(d, transmitter_freq_max, transmitter_freq_min)
    table.add_row(['','Free-space path loss', 'dBW', '-', fspl])
    table.add_row(['','Rain fade loss', 'dBW', '-', rain_attenuation])
    table.add_row(['','', '', '', ''])
    transmitted_power = transmitted_power  - rain_attenuation - fspl

    table.add_row(['','Receiver antenna gain', 'dBi', '+', sat_beam_gain])
    table.add_row(['','Receiver bandwidth', 'dB/Hz', '', 10*math.log10(receiver_bandwidth*1000)])
    table.add_row(['','Receiver cable loss', 'dBW', '-', system_cable_loss])
    received_power = transmitted_power + sat_beam_gain - system_cable_loss
    table.add_row(['','Received signal power', 'dBW', '+', received_power])
    receiver_noise_power = BOLTZMANNS_CONSTANT_dB_Hz_K + 10*math.log10(receiver_bandwidth*math.pow(10,3)*system_noise_temperature)
    noise_spectral_density = BOLTZMANNS_CONSTANT_dB_Hz_K + 10*math.log10(system_noise_temperature)
    table.add_row(['','Receiver noise spectral density (No)', 'dBW', '', noise_spectral_density])
    table.add_row(['','Receiver noise power', 'dBW', '', receiver_noise_power])  # derived
    table.add_row(['','', '', '', ''])

    result_c_to_n = received_power - receiver_noise_power
    result_eb_no = result_c_to_n - 10*math.log10((bit_per_second)/(receiver_bandwidth*math.pow(10,3))) #convert to Hz
    table.add_row(['','Receiver S/N', 'dB', '', result_c_to_n])  # derived
    table.add_row(['','Receiver Eb/No', 'dB', '', result_eb_no])  # derived
    table.add_row(['','Implementation S/N margin', 'dB', '', implementation_margin])
    table.add_row(['','', '', '', ''])

    required_eb_no = system_c_to_n - 10*math.log10((bit_per_second)/(receiver_bandwidth*math.pow(10,3)))
    table.add_row(['','Required S/N', 'dB', '', system_c_to_n])
    table.add_row(['','Required Eb/No', 'dB', '', required_eb_no])
    table.add_row(['','Excess margin', 'dB', '', result_c_to_n - system_c_to_n])
    table.add_row(['','', '', '', ''])
    print(table)


def slant_range(a, b, delta, latitude):
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2) - 2*a*b*math.cos(delta)*math.cos(latitude))

def FSPL(d, transmitter_freq_max, transmitter_freq_min):
    return 20*math.log10(d) + 20*math.log10((transmitter_freq_max+transmitter_freq_min)/2) + 32.4 #mega hertz