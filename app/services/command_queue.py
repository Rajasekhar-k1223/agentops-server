# agentops-server/app/services/command_queue.py
from collections import defaultdict, deque

class CommandQueue:
    def __init__(self):
        self.queues = defaultdict(deque)

    def enqueue(self, agent_id: str, command: str):
        self.queues[agent_id].append(command)

    def dequeue(self, agent_id: str):
        if self.queues[agent_id]:
            return self.queues[agent_id].popleft()
        return None