import util

class Track(object):
    def __init__(self, info):
        self.tid = info['track']['track_id']
        self.name = info['track']['track_name']
        self.artist = info['track']['artist_name']

    def __eq__(self, other):
        return self.tid == other.tid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + " - " + self.artist
  
    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.tid)

    def get_lyrics(self):
        return util.get_track_lyrics(self)

