# Queues go here

class Queue:
    def __init__(self):
        self.queue = []
        self.now_playing = None

    def skip(self):
        if len(self.queue) > 0:
            self.now_playing = self.queue[0]
            self.queue.pop(0)
        else:
            self.now_playing = None