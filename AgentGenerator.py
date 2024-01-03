from NetworkSettings import NetworkSettings, SystemInfo
from EventManager import Event
from geopy.distance import geodesic
import math

R = 6373.0
H = 610
Airplane_H = 10
diff_H = H - Airplane_H

class Agent:
    def __init__(self, agent_id, src_dst, curr_pos, host_sat):
        self.agent_id = agent_id
        self.src_dst = src_dst
        self.curr_pos= curr_pos
        self.candidate_sat = {}
        self.host_sat = host_sat
        self.min_ele_angle = 10
    
class AgentHandover:
    def __init__(self, event_manager):
        self.event_manager = event_manager

    def handover(self):
        new = Event(NetworkSettings.simulation_time, 2, "handover")
        self.event_manager.add_new_event(new)

class UpdateAgent:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.min_ele_angle = 10
        self.execute()

    def execute(self):
        new = Event(SystemInfo.system_time, 1, "update agent")
        self.event_manager.add_new_event(new)

        self.update_agent_pos()
        self.find_candidate_sat()
        self.decide_host_sat()

    def update_agent_pos(self):
        for id in NetworkSettings.agent_id_list:
            ### 以下的NetworkSettings.time_interval要改成Sys的time才對 
            new_lat =  (NetworkSettings.object_info_dict[id].src_dst[1][0]-NetworkSettings.object_info_dict[id].src_dst[0][0])*(NetworkSettings.time_interval/NetworkSettings.simulation_time)
            new_long = (NetworkSettings.object_info_dict[id].src_dst[1][1]-NetworkSettings.object_info_dict[id].src_dst[0][1])*(NetworkSettings.time_interval/NetworkSettings.simulation_time)
            NetworkSettings.object_info_dict[id].curr_pos = (NetworkSettings.object_info_dict[id].curr_pos[0] + new_lat, NetworkSettings.object_info_dict[id].curr_pos[1] + new_long)
            ###
            # print(NetworkSettings.object_info_dict[id].curr_pos)

    def find_candidate_sat(self):
        for agent_id in NetworkSettings.agent_id_list:
            res = self.compute_elevation_angle(NetworkSettings.object_info_dict[agent_id].curr_pos)
            NetworkSettings.object_info_dict[agent_id].candidate_sat = res
        
    def compute_elevation_angle(self, agent_pos):
        sat_with_angle = {}
        for sat_id in NetworkSettings.sat_id_list:
            sat_pos = NetworkSettings.object_info_dict[sat_id].pos
            try:
                distance = geodesic(agent_pos, sat_pos).kilometers                    
                result = math.atan(diff_H/distance)
            except: # divide by zero
                result = 0
            if result != 0:
                res_ = result*180/math.pi
                if res_ > self.min_ele_angle:
                   sat_with_angle[sat_id] = result*180/math.pi
        return sat_with_angle
    
    def decide_host_sat(self):
        for id in NetworkSettings.agent_id_list:
            max_key = max(NetworkSettings.object_info_dict[id].candidate_sat, key=NetworkSettings.object_info_dict[id].candidate_sat.get)  
            NetworkSettings.object_info_dict[id].host_sat = NetworkSettings.object_info_dict[max_key]
            NetworkSettings.object_info_dict[max_key].used = 1

class AgentGenerator:
    event_handler_dict = {
        "trigger_handover": AgentHandover,
        "update_agent": UpdateAgent
    }

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.ini_agent_pos()

    def ini_agent_pos(self):
        cnt = 1
        with open('./data/airport/airports.txt') as file:
            lines = file.readlines()
        
        for i in range(0, len(lines), 2):
            line1 = lines[i].strip()
            line2 = lines[i+1].strip()

            lat1, lon1 = map(float, line1.split(', '))
            lat2, lon2 = map(float, line2.split(', '))
            
            src_dst_pair = ((lat1, lon1), (lat2, lon2))

            agent_id = 'agent{}'.format(cnt)
            agent = Agent(agent_id, src_dst_pair, (lat1, lon1), '')

            NetworkSettings.agent_id_list.append(agent_id)
            NetworkSettings.object_info_dict[agent_id] = agent
            cnt = cnt + 1

        file.close()

        new = Event(0, 1, "Initial all agent")
        self.event_manager.add_new_event(new)

        UpdateAgent(self.event_manager)

    # def update_agent_pos(self):
    #     for i in range(1, NetworkSettings.simulation_time, NetworkSettings.time_interval):
    #         new = Event(i, 1, "update all agent")
    #         self.event_manager.add_new_event(new)