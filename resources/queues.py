# This is where the queue class is stored

class Queue:
    def __init__(self):
        self.queue = []
        self.now_playing = None
        self.loop = False

    def next(self):
        if not self.loop:
            if len(self.queue) > 0:
                self.now_playing = self.queue[0]
                self.queue.pop(0)
            else:
                self.now_playing = None

    def add(self, song):
        if self.now_playing is None:
            self.now_playing = song
        else:
            self.queue.append(song)


