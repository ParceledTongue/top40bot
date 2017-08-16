import markovify, pickle, random
from musixmatch import Musixmatch
from track import Track

# set up Musixmatch API
musixmatch = Musixmatch('***REMOVED***')

def get_track_lyrics(tid):
  lyrics = musixmatch.track_lyrics_get(tid)['message'] \
      ['body']['lyrics']['lyrics_body']
  lyrics = lyrics.split('...')[0] # remove text watermark
  return lyrics

def get_top_40():
  info_list = musixmatch.chart_tracks_get(1, 40, True)['message']['body'] \
      ['track_list']
  return [Track(info) for info in info_list]

def update_cache():

  # load in the cache
  with open('../cache/cache.pkl', 'rb') as f:
    cache = pickle.load(f)
  
  top40 = get_top_40()

  # add missing track info
  for track in top40:
    if not track in cache.keys():
      print('Adding ' + str(track) + ' to cache')
      cache[track] = track.get_lyrics()
  
  # delete info for tracks no longer in the top 40
  bumped_tracks = set(cache.keys()) - set(top40)
  for track in bumped_tracks:
    print('Deleting ' + str(track) + ' from cache')
    cache.pop(track)

  # update the cache file
  with open('../cache/cache.pkl', 'wb') as f:
    pickle.dump(cache, f, pickle.HIGHEST_PROTOCOL)

  return cache

def clear_cache():
  empty_cache = {}
  with open('../cache/cache.pkl', 'wb') as f:
    pickle.dump(empty_cache, f, pickle.HIGHEST_PROTOCOL)

def make_tweet():
  with open('../cache/cache.pkl', 'rb') as f:
    cache = pickle.load(f)
 
  all_lyrics = ''.join(cache.values())
  models = [
      markovify.NewlineText(all_lyrics, state_size = 2),
      markovify.NewlineText(all_lyrics, state_size = 3),
      markovify.NewlineText(all_lyrics, state_size = 4)]

  tweet = None
  while tweet is None:
    tweet = random.choice(models).make_short_sentence(140)
  
  return tweet

