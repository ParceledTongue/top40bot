class Track(object):
    def __init__(self, info):
        self.tid = info['track']['track_id']
        self.name = info['track']['track_name']
        self.artist = info['track']['artist_name']

    def __str__(self):
        return self.name + " - " + self.artist
  
    def __repr__(self):
        return str(self)

