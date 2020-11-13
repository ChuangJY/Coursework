import inquirer
from os import *
import db
from linkbudget import *
import utilities


def decode_designation_emission(code):
    tmp = []
    unit = ''
    bandwidth = code[0:4]
    type_of_mod = code[4]
    tran_info = code[5]
    info = code[6]

    for i in bandwidth:
        if i.isdigit():
            tmp.append(i)
        else:
            unit = i
            tmp.append('.')

    s = float(('').join(tmp))

    if unit == 'H':
        pass
    elif unit == 'k':
        s = s*1000
    elif unit == 'M':
        s = s*1000000
    elif unit == 'G':
        s = s*1000000000

    if  type_of_mod == 'A':
        tmod = "DSB-AM"
    elif  type_of_mod == 'B':
        tmod = "Independent sideband"
    elif type_of_mod == 'C':
        tmod = "Vestigial sideband"
    elif  type_of_mod == 'D':
        tmod = "Mix AM & FM/PM"
    elif  type_of_mod == 'F':
        tmod = "FM"
    elif  type_of_mod == 'G':
        tmod = "PM"
    elif  type_of_mod == 'H':
        tmod = "SSB"
    elif type_of_mod == 'J':
        tmod = "SSB-SC"
    elif type_of_mod == 'K':
        tmod = "PAM"
    elif type_of_mod == 'L':
        tmod = "PWM"
    elif type_of_mod == 'M':
        tmod = "PPM"
    elif type_of_mod == 'N':
        tmod = "N"
    elif type_of_mod == 'P':
        tmod = "Sequence of pulses w/o mod"
    elif type_of_mod == 'Q':
        tmod = "Sequence of pulsees, with PM/FM"
    elif type_of_mod == 'R':
        tmod = "SSB, reduced carrier"
    elif type_of_mod == 'V':
        tmod = "Mixed of pulse mod"
    elif type_of_mod == 'W':
        tmod = "Mixed"
    elif type_of_mod == 'X':
        tmod = "N/A"

    if tran_info == '0':
        tinfo = "No mod"
    elif tran_info == '1':
        tinfo = "One channel, digital, no subcarrier"
    elif tran_info == '2':
        tinfo = "One channel, digital, subcarrier"
    elif tran_info == '3':
        tinfo = "ONe channel, analog"
    elif tran_info == '7':
        tinfo = "More than one channel, digital"
    elif tran_info == '8':
        tinfo = "More than one channel, analog"
    elif tran_info == '9':
        tinfo = "Mix"
    else:
        tinfo = "N/A"
    
    if info == 'A':
        info = "Telegraphy"
    elif info == 'B':
        info = "Electronic telegraphy"
    elif info == 'C':
        info = "Facsimile"
    elif info == 'D':
        info = "Telemetry/telecommand"
    elif info == 'E':
        info = "Telephony"
    elif info == 'F':
        info = "Video"
    elif info == 'N':
        info = "No trans info"
    elif info == 'W':
        info = "Mixed"
    else:
        info = "N/A"

    return s, tmod, tinfo, info


utils = utilities.Utilities()

if __name__ == "__main__":
    flag = True
    cal_time = 1
    while(flag):
        questions = [inquirer.List(
            'Uplink_downlink', message="Uplink or Downlink: ", choices=['Downlink', 'Uplink']), ]
        answer = inquirer.prompt(questions)

        db_files = []
        for f in listdir('./'):
            if f.endswith('.' + 'mdb'):
                db_files.append(f)

        Up_or_Down = ""
        if answer['Uplink_downlink'] == "Uplink":
            Up_or_Down = "Uplink"
            questions = [
                inquirer.List(
                    'tr_db_file_name',
                    message="Select earth station db file from ITU SNS: ",
                    choices=db_files
                ),
            ]

            answer = inquirer.prompt(questions)
            db_files.remove(answer['tr_db_file_name'])
            tx = answer['tr_db_file_name']

            questions = [
                inquirer.List(
                    'rx_db_file_name',
                    message="Select satellite db file from ITU SNS: ",
                    choices=db_files
                ),
            ]

            answer = inquirer.prompt(questions)
            db_files.remove(answer['rx_db_file_name'])
            rx = answer['rx_db_file_name']

            print("Transmitting earth station: ", tx)
            print("Receiving satellite: ", rx)

            # Initialize database
            database = db.DatabaseConnection(rx, tx, updown="Up")

            es_info = database.get_earth_station_basic_info()
            print("\n******************************")
            print("**Transmitting Earth Station**")
            print("******************************\n")
            print("\
                Notice id: %s\n\
                Sation adminitration: %s\n\
                Earth station name: %s\n\
                Earth station longitude: %s\n\
                Earth station latitude: %s\n\
                Earth station altitude (km): %s\n " % es_info)
            es_longitude = es_info[3]
            es_longitude = abs(float(es_longitude[:-2]))
            es_latitude = es_info[4]
            es_latitude = abs(float(es_latitude[:-2]))
            es_altitude = float(es_info[5])

            questions = [
                inquirer.List(
                    'earth_station_beam',
                    message="Select a transmitting beam: ",
                    choices=database.get_earth_station_beam_list()
                ),
            ]

            answer = inquirer.prompt(questions)
            [
                group_id,
                transmitter_maximum_input_power,
                transmitter_minimum_input_power,
                transmitter_beam_name,
                transmitter_freq_min,
                transmitter_freq_max,
                bandwidth,
                polarization,
                transmitter_antenna_gain
            ] = answer['earth_station_beam']
            print("\
                Earth station transmitting beam name: %s\n\
                Earth station transmitting beam group id: %s\n\
                Earth station transmitter antenna min input power (dBW): %s\n\
                Earth station transmitter antenna max input power (dBW): %s\n\
                Earth station transmitter antenna gain (dBi): %s\n\
                Earth station transmitting beam min frequency (MHz): %s\n\
                Earth station transmitting beam max frequency (MHz): %s\n\
                Earth station transmitting beam bandwidth (kHz): %s\n\
                Earth station transmitting beam polarization type: %s\n" %
                  (
                      transmitter_beam_name,
                      group_id,
                      transmitter_maximum_input_power,
                      transmitter_minimum_input_power,
                      transmitter_antenna_gain,
                      transmitter_freq_min,
                      transmitter_freq_max,
                      bandwidth,
                      polarization,
                  )
                  )

            print("\n******************************")
            print("*****Receiving Satellite******")
            print("******************************\n")
            sat_info = database.get_satellite_basic_info()
            print("\
                Notice id: %s \n\
                Satellite adminitration: %s\n\
                Satellite name: %s \n\
                Satellite longitude: %s \n" % database.get_satellite_basic_info())
            sat_longitude = sat_info[3]

            questions = [
                inquirer.List(
                    'satellite_beam',
                    message="Select a satellite beam: ",
                    choices=database.get_satellite_beam_group_list(
                        transmitter_beam_name)
                ),
            ]

            answer = inquirer.prompt(questions)
            [
                receiver_beam_name,
                receiver_antenna_gain,
                receiver_beam_grp_id,
                receiver_beam_designation_of_emi,
                receiver_antenna_input_power_max,
                receiver_antenna_input_power_min,
                receiver_c_to_n,
                receiver_noise_temperature,
                receiver_bandwidth,
                receiver_frequency_min,
                receiver_frequency_max,
                receiver_polarization
            ] = answer['satellite_beam']
            print("\
                Satellite receiving beam name: %s\n\
                Satellite receiving antenna gain (dBi): %s\n\
                Satellite receiving beam group id: %s\n\
                Satellite designation of emission: %s\n\
                Satellite receiver antenna max input power (dBW): %s\n\
                Satellite receiver antenna min input power (dBW): %s\n\
                Satellite receiver S/N (dB): %s\n\
                Satellite receiver noise temperature (K): %s\n\
                Satellite receiver bandwidth (kHz): %s\n\
                Satellite receiver minimum frequency (MHz): %s\n\
                Satellite receiver maximum frequency (MHz): %s\n\
                Satellite receiver polarization type: %s\n" %
                  (
                      receiver_beam_name,
                      receiver_antenna_gain,
                      receiver_beam_grp_id,
                      receiver_beam_designation_of_emi,
                      receiver_antenna_input_power_max,
                      receiver_antenna_input_power_min,
                      receiver_c_to_n,
                      receiver_noise_temperature,
                      receiver_bandwidth,
                      receiver_frequency_min,
                      receiver_frequency_max,
                      receiver_polarization
                  ))
            print("Emission details: ", decode_designation_emission(receiver_beam_designation_of_emi))
        else:
            Up_or_Down = "Downlink"
            questions = [
                inquirer.List(
                    'tr_db_file_name',
                    message="Select satellite db file from ITU SNS: ",
                    choices=db_files
                ),
            ]

            answer = inquirer.prompt(questions)
            db_files.remove(answer['tr_db_file_name'])
            tx = answer['tr_db_file_name']

            questions = [
                inquirer.List(
                    'rx_db_file_name',
                    message="Select earth station db file from ITU SNS: ",
                    choices=db_files
                ),
            ]

            answer = inquirer.prompt(questions)
            rx = answer['rx_db_file_name']

            print("Transmitting satellite: ", tx)
            print("Receiving earth station: ", rx)

            # Initialize database
            database = db.DatabaseConnection(rx, tx)

            print("\n******************************")
            print("****Transmitting Satellite****")
            print("******************************\n")
            sat_info = database.get_satellite_basic_info()
            print("\
                Notice id: %s \n\
                Satellite adminitration: %s\n\
                Satellite name: %s \n\
                Satellite longitude: %s \n" % database.get_satellite_basic_info())
            sat_longitude = sat_info[3]

            questions = [
                inquirer.List(
                    'satellite_beam',
                    message="Select a transmitting beam: ",
                    choices=database.get_satellite_beam_group_list()
                ),
            ]

            answer = inquirer.prompt(questions)
            [
                transmitter_beam_name,
                transmitter_antenna_gain,
                transmitter_emission_group_id,
                transmitter_beam_design_emi,
                transmitter_maximum_input_power,
                transmitter_minimum_input_power,
                _,
                transmitter_bandwidth,
                transmitter_freq_min,
                transmitter_freq_max,
                transmitter_polarization,
            ] = answer['satellite_beam']
            print("\
                Satellite transmitting beam name: %s\n\
                Satellite transmitter antenna gain: %s\n\
                Satellite transmitting beam group id: %s\n\
                Satellite designation of emission: %s\n\
                Satellite transmitter antenna max input power: %s\n\
                Satellite transmitter antenna min input power: %s\n\
                Satellite transmitting beam bandwidth: %s\n\
                Satellite transmitting beam min frequency: %s\n\
                Satellite transmitting beam max frequency: %s\n\
                Satellite transmitting beam polarization type: %s\n" %
                  (
                      transmitter_beam_name,
                      transmitter_antenna_gain,
                      transmitter_emission_group_id,
                      transmitter_beam_design_emi,
                      transmitter_maximum_input_power,
                      transmitter_minimum_input_power,
                      transmitter_bandwidth,
                      transmitter_freq_min,
                      transmitter_freq_max,
                      transmitter_polarization,
                  )
                  )

            print("Emission details: ", decode_designation_emission(transmitter_beam_design_emi))

            es_info = database.get_earth_station_basic_info()
            print("\n******************************")
            print("****Receiving Earth Station***")
            print("******************************\n")
            print("\
                Notice id: %s\n\
                Sation adminitration: %s\n\
                Earth station name: %s\n\
                Earth station longitude: %s\n\
                Earth station latitude: %s\n\
                Earth station altitude: %s\n " % es_info)
            es_longitude = es_info[3]
            es_longitude = abs(float(es_longitude[:-2]))
            es_latitude = es_info[4]
            es_latitude = abs(float(es_latitude[:-2]))
            es_altitude = float(es_info[5])

            questions = [
                inquirer.List(
                    'earth_station_beam',
                    message="Select a earth station beam to analyse: ",
                    choices=database.get_earth_station_beam_list(
                        beam=transmitter_beam_name)
                ),
            ]

            answer = inquirer.prompt(questions)
            [
                receiver_beam_grp_id,
                receiver_c_to_n,
                receiver_beam_name,
                receiver_noise_temperature,
                receiver_frequency_min,
                receiver_frequency_max,
                receiver_bandwidth,
                receiver_polarization,
                receiver_antenna_gain,
            ] = answer['earth_station_beam']
            print("\
                Earth station receiving beam group id: %s\n\
                Earth station receiver required S/N: %s\n\
                Earth station receiving beam name: %s\n\
                Earth station receiver noise temperature: %s\n\
                Earth station receiver minimum frequency: %s\n\
                Earth station receiver maximum frequency: %s\n\
                Earth station receiver bandwidth: %s\n\
                Earth station receiver polarization type: %s\n\
                Earth station antenna gain: %s\n" %
                  (
                      receiver_beam_grp_id,
                      receiver_c_to_n,
                      receiver_beam_name,
                      receiver_noise_temperature,
                      receiver_frequency_min,
                      receiver_frequency_max,
                      receiver_bandwidth,
                      receiver_polarization,
                      receiver_antenna_gain,
                  ))

        system_cable_loss, transmitter_back_off_power, rain_attenuation, implementation_margin, bit_per_symbol = utils.prompt_miscelleneous_loss()

        print("\n******************************")
        print("************Result************")
        print("******************************\n")

        link_budget_calculation(
            Up_or_Down + '\n(' + str(cal_time) + ')',
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
            receiver_antenna_gain,
            receiver_bandwidth,
            receiver_noise_temperature,
            implementation_margin,
            receiver_c_to_n,
            bit_per_symbol
        )

        con = input("\nContinue? (y/N): ")
        if con == 'y' or con == 'Y':
            flag = True
            cal_time = cal_time + 1
        else:
            flag = False
