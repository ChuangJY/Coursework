import re

class Utilities:
    def __init__(self):
        pass

    def decode_polarization_code(self, code):
        if code == 'H':
            return "Horizontal (E field w.r.t equatorial plane)"
        elif code == 'V':
            return "Vertical (E field w.r.t equatorial plane)"
        elif code == 'SR':
            return "Right-hand Slant (CW 45 Degree)"
        elif code == 'SL':
            return "Left-hand Slant (CCW 45 Degree)"
        elif code == 'CR':
            return "Right-hand circular"
        elif code == 'CL':
            return "Left-hand circular"
        elif code == 'D':
            return "Dual"
        elif code == 'M':
            return "Mixed"
        elif code == 'L':
            return "Linear"

    def prompt_miscelleneous_loss(self):
        system_cable_loss = input('System_cable_loss (dB): ')
        while re.match(r'^-?\d+(?:\.\d+)?$', system_cable_loss) is None:
            system_cable_loss = input('System_cable_loss (dB) again: ')
        system_cable_loss = float(system_cable_loss)

        transmitter_back_off_power = input(
            'Earth station back off power (dB): ')
        while re.match(r'^-?\d+(?:\.\d+)?$', transmitter_back_off_power) is None:
            transmitter_back_off_power = input(
                'Earth station back off power (dB) again: ')
        transmitter_back_off_power = float(transmitter_back_off_power)

        rain_attenuation = 0
        rain_attenuation = input('Rain attenuation (dB): ')
        while re.match(r'^-?\d+(?:\.\d+)?$', rain_attenuation) is None:
            rain_attenuation = input('Rain attenuation (dB): ')
        rain_attenuation = float(rain_attenuation)

        implementation_margin = 0
        implementation_margin = input('Implementation margin (dB): ')
        while re.match(r'^-?\d+(?:\.\d+)?$', implementation_margin) is None:
            implementation_margin = input('Implementation margin (dB): ')
        implementation_margin = float(implementation_margin)

        bit_rate = 0
        bit_rate = input('Bit per symbol: ')
        while re.match(r'^-?\d+(?:\.\d+)?$', bit_rate) is None:
            bit_rate = input('Bit per symbol again (integer): ')
        bit_rate = float(bit_rate)

        return system_cable_loss, transmitter_back_off_power, rain_attenuation, implementation_margin, bit_rate