class local_queue():

    _queue = []

    def __init__(self):
        pass

    def add_song(self, song_name, song_link):
        self._queue.append({song_name: song_link})

    def delete_song(self):
        self._queue.pop(0)

    def pune_queue(self):
        self._queue = []

    def get_songs_queue(self):
        return self._queue
