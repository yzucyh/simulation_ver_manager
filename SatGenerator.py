from NetworkSettings import NetworkSettings, SystemInfo
from EventManager import Event
import os
import csv
import math
import time

class SatGenerator:
    def __init__(self, event_manager, from_time):
        self.event_manager = event_manager
        self.ini_sat_pos(from_time)
        
    def ini_sat_pos(self, from_time):
        for orbit_num in range(1, NetworkSettings.num_of_sat_orbit+1):
            orbit_file_dir = './data/satellite/Orbit_'+str(orbit_num)
            orbit_file_list = []
            allList = os.walk(orbit_file_dir)
            sat_index = 1
            for _, _, txt in allList:
                allList_index = txt
            for index in allList_index:
                orbit_file_list.append(orbit_file_dir+'/'+index)
            for fname in orbit_file_list:
                with open(fname, 'r', encoding='UTF-8') as csvfile:
                    reader = csv.reader(csvfile)

                    # 跳過%from_time行
                    for _ in range(from_time): 
                        next(reader)

                    for index, rows in enumerate(reader):
                        if index == from_time:
                            ini_lat = float(rows[0])
                            ini_long = float(rows[1])

                    orbit_with_sat = "{}-{}".format(orbit_num, sat_index)
                    coverage = self.compute_coverage(ini_lat, ini_long)

                    sat_obj = Satellite(orbit_with_sat, (ini_lat, ini_long), coverage)

                    NetworkSettings.sat_id_list.append(orbit_with_sat)
                    NetworkSettings.object_info_dict[orbit_with_sat] = sat_obj
                    csvfile.close()
                sat_index = sat_index + 1

        new = Event(0, 0, "Initial all satellite")
        self.event_manager.add_new_event(new)
        
        self.update_sat_pos()

    def update_sat_pos(self):
        for j in range(1, NetworkSettings.simulation_time, NetworkSettings.time_interval):
            new = Event(j, 0, "update all satellite")
            self.event_manager.add_new_event(new)

    def compute_coverage(self, lat, long):
        R = 6373 * 1000 # 單位: m
        distance = 580 * 1000 
        azimuth = 45
        coverage = []

        for index in range(0, 4): # + -
            if index == 0:
                lat2 = lat + distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                lon2 = long + distance * math.sin(math.radians(azimuth)) / (R * math.cos(math.radians(lat)) * 2 * math.pi/ 360)

            elif index == 1:
                lat2 = lat + distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                lon2 = long - distance * math.sin(math.radians(azimuth)) / (R * math.cos(math.radians(lat)) * 2 * math.pi/ 360)

            elif index == 2:
                lat2 = lat - distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                lon2 = long + distance * math.sin(math.radians(azimuth)) / (R * math.cos(math.radians(lat)) * 2 * math.pi/ 360)
            else:
                lat2 = lat - distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                lon2 = long - distance * math.sin(math.radians(azimuth)) / (R *  math.cos(math.radians(lat)) * 2 * math.pi/ 360)

            coverage.append((lat2, lon2))
        return coverage

class Satellite:
    def __init__(self, number, pos, coverage):
        self.next = None
        self.number = number
        self.pos = pos
        self.coverage = coverage
        self.used = 0
        self.freq = 28
        self.bandwidth = 500
        self.tx_gain = 10
        self.rx_gain = 10
        self.numChannel = 100
        self.ISL_link = 2
        self.ISL_state = {0, 1}
