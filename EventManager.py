import heapq
from NetworkSettings import NetworkSettings, SystemInfo

class Event:
    def __init__(self, time, priority, description):
        self.time = time
        self.priority = priority
        self.description = description
    
    def __lt__(self, other):
        if self.time == other.time:
            return self.priority < other.priority
        return self.time < other.time
    
class EventManager:
    def __init__(self):
        self.event_list = []
    
    # def execute(self):
    #     while self.event_list.qsize() > 0 and SystemInfo.system_time < NetworkSettings.simulation_time:
    #         event = self.event_list.get()
    #         event_content = event[1]
    #         SystemInfo.system_time = event_content['event_trigger_time']
    #         print ("EventManager: current_system_time: {}, event_content: {}".format(event_content['event_trigger_time'], event_content))
    #         # NetworkSettings.object_info_dict[event_content['event_target']].event_handler(event_content)

    def add_new_event(self, event):
        heapq.heappush(self.event_list, event)
        # print("EventManager: insert event", event.description)

    def process_events(self):
        while self.event_list:
            event = heapq.heappop(self.event_list)
            self.handle_event(event)
    
    def handle_event(self, event):
        # print(f"Processing event at time {event.time}: {event.description}")
        pass