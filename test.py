import queue

class Event:
    def __init__(self, name, time, priority):
        self.name = name
        self.time = time
        self.priority = priority

    def __lt__(self, other):
        # 定义比较函数，确保在相同时间时按照优先级排序
        if self.time == other.time:
            return self.priority < other.priority
        else:
            return self.time < other.time

# 创建优先队列
pq = queue.PriorityQueue()

# 示例事件
event1 = Event("Event 1", 10, 5)
event2 = Event("Event 2", 10, 2)

# 插入元素
pq.put(10, 0, "event1")
pq.put(10, 1, "event2")


# 获取元素
while not pq.empty():
    item = pq.get()
    print(item)

