import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from credentials import client_id, client_secret

# provide api credentials
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret))


def get_song_id(name_of_song, correct_artist):
    # step 1: encode artists name and pass to search query
    results = sp.search(
        q=name_of_song.replace(' ', '%'),  # song searched
        limit=5
    )

    # step 2: save id of song for later comparison
    song_id = results['tracks']['items'][0]['uri']
    song_id = song_id.replace('spotify:track:', '')

    # step 3: save artists of song of first result
    song_artists_list = results['tracks']['items'][0]['artists']

    # step 4: create dictionary mapping each artist name key to the spotify id
    artist_info_dict = {}
    for artist in song_artists_list:
        artist_info_dict[artist['name']] = artist['id']

    lowercase_artists = [artist.casefold() for artist in artist_info_dict.keys()]

    # step 5 confirm if correct artist is in artists on song
    if correct_artist.casefold() in lowercase_artists \
            or any(correct_artist.casefold().find(artist)
                   for artist in lowercase_artists):
        print(f'Song ID: {song_id}')
        print('Artists featured:')
        for artist in artist_info_dict.keys():
            print(f'- {artist}')
            print(f'\t- artist ID: {artist_info_dict[artist]}')

        return [song_id, list(artist_info_dict.values())]
    else:
        print('Song ID not found.')
        print(f'{correct_artist} not found in song artists:')
        for artist in artist_info_dict.keys():
            print(artist)
        return None


def get_artist_genres(artist_id):
    artist_genre_dict = dict(sp.artist(artist_id))
    artist_genres = artist_genre_dict['genres']
    # print('\n')
    # for genre in artist_genres:
    #     print(genre)
    return artist_genres


def get_song_genres(artist_id_list):
    genre_list = []
    for artist_id in artist_id_list:
        genre_list += get_artist_genres(artist_id)
        # print(genre_list)
    # print(genre_list)
    return genre_list


song_info = get_song_id('Family Ties', 'Baby Keem & Kendrick Lamar')

song_id = song_info[0]
artists_ids = song_info[1]
song_genres = get_song_genres(artists_ids)
print(song_genres)
