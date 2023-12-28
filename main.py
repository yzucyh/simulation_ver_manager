from EventManager import EventManager
from GwGenerator import GwGenerator
from SatGenerator import SatGenerator
from AgentGenerator import AgentGenerator
from NetworkSettings import NetworkSettings


def main():
    event_manager = EventManager()
    from_time = int(input("載入第幾秒開始資料: "))
    GwGenerator(event_manager)
    # print(NetworkSettings.gw_id_list) # ok
    SatGenerator(event_manager, from_time)
    # print(NetworkSettings.sat_id_list) # ok
    AgentGenerator(event_manager)

if __name__ == '__main__':
    main()
