import billboard, lyricsgenius, markovify, os, random

genius = lyricsgenius.Genius(os.environ['GENIUS_ACCESS_TOKEN'])

def genius_track(billboard_track):
    return genius.search_song(billboard_track.title, billboard_track.artist, get_full_info=False)

def get_top_tracks(n=40):
    if (n < 1 or n > 100):
        raise ValueError('n must be a number from 1 to 100')
    billboard_tracks = billboard.ChartData('hot-100')[0:n]
    genius_tracks = [genius_track(bt) for bt in billboard_tracks]
    return [gt for gt in genius_tracks if gt is not None]

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
    for track in get_top_tracks():
        all_lyrics += track.lyrics + '\n'
    all_lyrics = no_duplicate_lines(all_lyrics)
    models = [
        markovify.NewlineText(all_lyrics, state_size = 2),
        markovify.NewlineText(all_lyrics, state_size = 3)]

    tweet = None
    while tweet is None:
        tweet = random.choice(models).make_short_sentence(280)
  
    return tweet

