import markovify, os, pickle, random
from musixmatch import Musixmatch
from PyLyrics import PyLyrics
from track import Track

CACHE_PATH = '../cache/cache.pkl'

# set up Musixmatch API
musixmatch = Musixmatch('***REMOVED***')

def create_cache_dir_if_not_exists():
    cache_dir = os.path.dirname(CACHE_PATH)
    try:
        os.makedirs(cache_dir)
    except OSError:
        if not os.path.isdir(cache_dir):
            raise

def read_cache():
    create_cache_dir_if_not_exists()
    if os.path.isfile(CACHE_PATH):
        with open(CACHE_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def write_cache(cache):
    create_cache_dir_if_not_exists()
    with open(CACHE_PATH, 'wb') as f:
        pickle.dump(cache, f, pickle.HIGHEST_PROTOCOL)

def update_cache():
    cache = read_cache()
    cache_tracks = set(cache.keys())
    top40_tracks = set(get_top_40())

    print('Updating cache...')
    
    if cache_tracks == top40_tracks:
        print('  Already up to date.')
        return cache

    # add missing track info
    new_tracks = top40_tracks - cache_tracks
    for track in new_tracks:
        print('  Adding ' + str(track) + ' to cache')
        cache[track] = track.get_lyrics()
  
    # delete info for tracks no longer in the top 40
    bumped_tracks = cache_tracks - top40_tracks
    for track in bumped_tracks:
        print('  Deleting ' + str(track) + ' from cache')
        cache.pop(track)

    write_cache(cache)
    return cache

def clear_cache():
    write_cache({})

def get_track_lyrics(track):
    lyrics = ''
    try:
        lyrics = PyLyrics.getLyrics(
                track.artist.split(' feat.')[0], track.name)
        print('* lyrics obtained via PyLyrics')
    except:
        lyrics = musixmatch.track_lyrics_get(track.tid) \
                ['message']['body']['lyrics']['lyrics_body']
        print('* lyrics obtained via musixmatch')
        lyrics = lyrics.split('...')[0] # remove text watermark
    return lyrics

def get_top_40():
    info_list = musixmatch.chart_tracks_get(1, 40, True) \
            ['message']['body']['track_list']
    return [Track(info) for info in info_list]

def make_tweet():
    cache = read_cache()

    if not cache:
        cache = update_cache()
 
    all_lyrics = ''.join(cache.values())
    models = [
        markovify.NewlineText(all_lyrics, state_size = 2),
        markovify.NewlineText(all_lyrics, state_size = 3),
        markovify.NewlineText(all_lyrics, state_size = 4)]

    tweet = None
    while tweet is None:
        tweet = random.choice(models).make_short_sentence(140)
  
    return tweet

