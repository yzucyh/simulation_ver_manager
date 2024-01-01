from EventManager import EventManager
from GwGenerator import GwGenerator
from SatGenerator import SatGenerator
from AgentGenerator import AgentGenerator
from NetworkSettings import NetworkSettings


def main():
    event_manager = EventManager()
    from_time = int(input("載入第幾秒的資料: "))

    GwGenerator()
    # print(NetworkSettings.gw_id_list) # ok
    AgentGenerator(event_manager)
    # print(NetworkSettings.agent_id_list) # ok
    SatGenerator(event_manager, from_time)
    # print(NetworkSettings.sat_id_list) # ok

    event_manager.process_events()

if __name__ == '__main__':
    main()
