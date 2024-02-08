from queue_manager import local_queue

lq = local_queue()
lq.add_song('some_name', 'path1')
lq.add_song('some_name1', 'path2')
print(lq.get_songs_queue())
