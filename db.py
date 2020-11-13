import pyodbc

# establish database connection


class DatabaseConnection:
    def __init__(self, rx, tx, updown="Down"):
        self.updown = updown
        self.beam_name = ''
        if updown == "Up":
            self.sat = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jinye\work\fyp\LinkBudget\%s;' % rx)
            self.es = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jinye\work\fyp\LinkBudget\%s;' % tx)
            self.sat_cursor = self.sat.cursor()
            self.es_cursor = self.es.cursor()
        else:
            self.sat = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jinye\work\fyp\LinkBudget\%s;' % tx)
            self.es = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jinye\work\fyp\LinkBudget\%s;' % rx)
            self.sat_cursor = self.sat.cursor()
            self.es_cursor = self.es.cursor()

    def get_earth_station_basic_info(self):
        '''Earth station information extrated from database'''
        sql = 'select \
            ntc_id, \
            stn_name, \
            ctry, \
            long_deg, \
            long_min, \
            long_sec, \
            long_ew, \
            lat_deg, \
            lat_min, \
            lat_sec, \
            lat_ns, \
            ant_alt \
            from e_stn'
        [(
            notice_id,
            station_name,
            administrative,
            long_deg,
            long_min,
            long_sec,
            long_ew,
            lat_deg,
            lat_min,
            lat_sec,
            lat_ns,
            ant_altitude
        )] = self.es_cursor.execute(sql).fetchall()

        longitude = long_deg + (long_min/60) + (long_sec/3600)
        latitude = lat_deg + (lat_min/60) + (lat_sec/3600)
        return notice_id, station_name, administrative, str(longitude)+long_ew, str(latitude)+lat_ns, ant_altitude

    def get_earth_station_beam_list(self, beam=""):
        # Beam and its corresponding antenna info
        if self.updown == "Up":
            sql = "select \
                    emiss.grp_id,\
                    emiss.pep_max,\
                    emiss.pep_min,\
                    grp.beam_name, \
                    grp.freq_min,\
                    grp.freq_max, \
                    grp.bdwdth, \
                    grp.polar_type, \
                    e_ant.gain \
                    from (emiss \
                    inner join grp on\
                        emiss.grp_id = grp.grp_id)\
                    inner join e_ant on\
                        e_ant.beam_name = grp.beam_name\
                    where \
                        grp.emi_rcp = 'E'"
        else:
            sql = "select \
                    emiss.grp_id,\
                    emiss.c_to_n,\
                    grp.beam_name, \
                    grp.noise_t, \
                    grp.freq_min,\
                    grp.freq_max, \
                    grp.bdwdth, \
                    grp.polar_type, \
                    e_ant.gain \
                    from (emiss \
                    inner join grp on\
                        emiss.grp_id = grp.grp_id)\
                    inner join e_ant on\
                        e_ant.beam_name = grp.beam_name\
                    where \
                        grp.beam_name = '%s' and\
                        grp.emi_rcp = 'R'" % beam
        rows = self.es_cursor.execute(sql).fetchall()

        return rows

    def get_satellite_basic_info(self):
        sql = 'select geo.ntc_id,\
                    sat_name,\
                    long_nom,\
                    notice.adm \
                    from geo \
                    inner join notice on notice.ntc_id = geo.ntc_id'

        rows = self.sat_cursor.execute(sql).fetchall()

        for row in rows:
            index = 0
            for i in row:
                if index == 0:
                    notice_id = i if i else -101
                elif index == 1:
                    sat_name = i if i else 'N/A'
                elif index == 2:
                    satellite_longitude = i if i else -101
                elif index == 3:
                    administrative = i if i else 'N/A'
                index = index + 1

        return notice_id, administrative, sat_name, satellite_longitude,

    def get_satellite_beam_group_list(self, beam="Down"):
        if self.updown == "Up":
            sql = "select\
                s_beam.beam_name,\
                s_beam.gain,\
                emiss.grp_id,\
                emiss.design_emi,\
                emiss.pep_max,\
                emiss.pep_min,\
                emiss.c_to_n,\
                grp.noise_t,\
                grp.bdwdth,\
                grp.freq_min,\
                grp.freq_max,\
                grp.polar_type\
                from (emiss\
                inner join grp on \
                    grp.grp_id = emiss.grp_id)\
                inner join s_beam on\
                    grp.beam_name = s_beam.beam_name\
                where \
                    emiss.c_to_n is not NULL and \
                    grp.noise_t is not NULL and \
                    grp.beam_name = '%s' and\
                    grp.emi_rcp = 'R'\
                order by emiss.grp_id" % beam
        else:
            sql = "select\
                s_beam.beam_name,\
                s_beam.gain,\
                emiss.grp_id,\
                emiss.design_emi,\
                emiss.pep_max,\
                emiss.pep_min,\
                emiss.c_to_n,\
                grp.bdwdth,\
                grp.freq_min,\
                grp.freq_max,\
                grp.polar_type\
                from (emiss \
                inner join grp on \
                    grp.grp_id = emiss.grp_id)\
                inner join s_beam on\
                    grp.beam_name = s_beam.beam_name\
                where \
                    grp.noise_t is NULL and \
                    grp.emi_rcp = 'E'\
                order by emiss.grp_id"

        rows = self.sat_cursor.execute(sql).fetchall()

        return rows
