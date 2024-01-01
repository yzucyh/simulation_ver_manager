# import queue

# class Event:
#     def __init__(self, name, time, priority):
#         self.name = name
#         self.time = time
#         self.priority = priority

#     def __lt__(self, other):
#         # 定义比较函数，确保在相同时间时按照优先级排序
#         if self.time == other.time:
#             return self.priority < other.priority
#         else:
#             return self.time < other.time

# # 创建优先队列
# pq = queue.PriorityQueue()

# # 示例事件
# event1 = Event("Event 1", 10, 5)
# event2 = Event("Event 2", 10, 2)

# # 插入元素
# pq.put(10, 0, "event1")
# pq.put(10, 1, "event2")


# # 获取元素
# while not pq.empty():
#     item = pq.get()
#     print(item)

import heapq

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
        self.event_queue = []

    def add_event(self, event):
        heapq.heappush(self.event_queue, event)

    def process_events(self):
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.handle_event(event)

    def handle_event(self, event):
        print(f"Processing event at time {event.time}, priority {event.priority}: {event.description}")


event_manager = EventManager()

event_manager.add_event(Event(2, 1, "Event 1"))
event_manager.add_event(Event(1, 2, "Event 2"))
event_manager.add_event(Event(2, 3, "Event 3"))

# 处理事件
event_manager.process_events()
