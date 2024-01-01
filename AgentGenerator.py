from NetworkSettings import NetworkSettings, SystemInfo
from EventManager import Event

R = 6373.0
H = 610
Airplane_H = 10
diff_H = H - Airplane_H

class AgentGenerator:
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
            agent = Agent(agent_id, src_dst_pair, '')

            NetworkSettings.agent_id_list.append(agent_id)
            NetworkSettings.object_info_dict[agent_id] = agent
            cnt = cnt + 1

        file.close()

        new = Event(0, 0, "Initial agent")
        self.event_manager.add_new_event(new)

        
        self.update_agent_pos()

    def update_agent_pos(self):
        for i in range(1, 5):
    
            new = Event(i, 0, "update agent")
            self.event_manager.add_new_event(new)

class Agent:
    def __init__(self, agent_id, src_dst, host_sat):
        self.agent_id = agent_id
        self.scr_dst = src_dst
        self.candidate_sat = []
        self.host_sat = host_sat
    