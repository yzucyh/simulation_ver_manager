from queue import PriorityQueue
from NetworkSettings import NetworkSettings, SystemInfo

class EventManager:
    def __init__(self):
        self.event_list = PriorityQueue()
    
    def execute(self):
        while self.event_list.qsize() > 0 and SystemInfo.system_time < NetworkSettings.time_interval:
            event = self.event_list.get()
            event_content = event[1]
            SystemInfo.system_time = event_content['event_trigger_time']
            print ("EventManager: current_system_time: {}, event_content: {}".format(event_content['event_trigger_time'], event_content))
            # NetworkSettings.object_info_dict[event_content['event_target']].event_handler(event_content)

    def add_new_event(self, event_time, event_content):
        self.event_list.put((event_time, event_content))
        print("EventManager: insert event ", event_content)
