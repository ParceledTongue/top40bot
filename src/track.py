from PyLyrics import PyLyrics

class Track(object):
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return self.title + " - " + self.artist
  
    def __repr__(self):
        return str(self)

    def get_lyrics(self):
        print('  Getting lyrics for ' + str(self))
        lyrics = None
        try:
            lyrics = PyLyrics.getLyrics(
                    self.artist.split(' Featuring')[0], self.title)
            print('  * lyrics obtained via PyLyrics')
        except:
            print('  * lyrics could not be found via PyLyrics')
        return lyrics

