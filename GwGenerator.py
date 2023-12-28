from NetworkSettings import NetworkSettings
import random
import time

class GwGenerator:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.generate_all_gw()
    
    def generate_all_gw(self):
        event = {
            "priority": 0,
            "event_target": "gw_group",
            "event_name": "initial",
            "event_trigger_time": 1,
            "event_details": {}
        }
        with open('./data/gw/gw_positions.txt', 'r') as f:
            cnt = 1
            for line in f:
                gw_id = "gw{}".format(cnt)
                gw_coordinate = tuple(float(value) for value in line.split()) # 把gw座標寫成tuple
                NetworkSettings.gw_id_list.append({gw_id: {"gw_coordinate": gw_coordinate, "used": 0, "weather": random.randint(1,3)}}) # {"gw_id": {"gw_coordinate": (緯, 經), "used": 0沒用 1有用, "weather": 天氣}}
                cnt = cnt + 1
            f.close()
        self.event_manager.add_new_event(event['event_trigger_time'], event['priority'], event)