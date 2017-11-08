import markovify, os, random
from musixmatch import Musixmatch
from PyLyrics import PyLyrics
from track import Track

# set up Musixmatch API
musixmatch = Musixmatch(os.environ['MUSIXMATCH_SECRET'])

def top_40_tracks():
    info_list = musixmatch.chart_tracks_get(1, 40, True) \
            ['message']['body']['track_list']
    return [Track(info) for info in info_list]

def lyrics_for_track(track):
    print('  Getting lyrics for ' + str(track))
    lyrics = ''
    try:
        lyrics = PyLyrics.getLyrics(
                track.artist.split(' feat.')[0], track.name)
        print('  * lyrics obtained via PyLyrics')
    except:
        lyrics = musixmatch.track_lyrics_get(track.tid) \
                ['message']['body']['lyrics']['lyrics_body']
        print('  * lyrics obtained via musixmatch')
        lyrics = lyrics.split('...')[0] # remove text watermark
    return lyrics

def no_duplicate_lines(old_lyrics):
    new_lyrics = ''
    seen = set()
    for line in old_lyrics.splitlines():
        if line not in seen:
            seen.add(line)
            new_lyrics += line + "\n"
    return new_lyrics

def make_lyric():
    all_lyrics = ''
    for track in top_40_tracks():
        all_lyrics += lyrics_for_track(track) + '\n'
    all_lyrics = no_duplicate_lines(all_lyrics)
    models = [
        markovify.NewlineText(all_lyrics, state_size = 2),
        markovify.NewlineText(all_lyrics, state_size = 3)]

    tweet = None
    while tweet is None:
        tweet = random.choice(models).make_short_sentence(140)
  
    return tweet

