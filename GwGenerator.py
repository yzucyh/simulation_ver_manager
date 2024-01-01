from NetworkSettings import NetworkSettings
import random
import time

class GwGenerator:
    def __init__(self):
        self.generate_all_gw()
    
    def generate_all_gw(self):
        with open('./data/gw/gw_positions.txt', 'r') as f:
            cnt = 1
            for line in f:
                gw_id = "gw{}".format(cnt)
                gw_coordinate = tuple(float(value) for value in line.split()) # 把gw座標寫成tuple
                
                gw = Gateway(gw_id, gw_coordinate)
                NetworkSettings.gw_id_list.append(gw_id)
                NetworkSettings.object_info_dict[gw_id] = gw # {"gw_id": {"gw_coordinate": (緯, 經), "used": 0沒用 1有用, "weather": 天氣}}
                cnt = cnt + 1
            f.close()

class Gateway:
    def __init__(self, gw_id, gw_coordinate):
        self.gw_id = gw_id
        self.gw_coordinate = gw_coordinate
        self.used = 0
        self.weather = random.randint(1,3)