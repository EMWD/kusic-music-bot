import os
path = '/home/klim/Desktop/chords/audios'
files = os.listdir(path)

for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), '.mp3'])))
