import requests, json

token = "Bearer YOUR TOKEN"

def reloadInputs():
    print("Por favor, ingrese un número válido.\n")

def getTrackInfo(trackLink):
    trackId = trackLink.split('/')[-1]

    urlQueryTrackAudio = f"https://api.spotify.com/v1/audio-features/{trackId}"
    responseTrackAudo = requests.get(urlQueryTrackAudio, headers={"Authorization": token})
    trackAudio = responseTrackAudo.json()

    urlQueryTrackInfo = f"https://api.spotify.com/v1/tracks/{trackId}"
    responseTrackInfo = requests.get(urlQueryTrackInfo, headers={"Authorization": token})
    trackInfo = responseTrackInfo.json()


    print("Name:", trackInfo["name"])
    print("Danceability:", trackAudio["danceability"])
    print("Energy:", trackAudio["energy"])
    print("Instrumentalness:", trackAudio["instrumentalness"])
    print()

    aio.send_data(cancionesFeed.key, trackInfo["name"])
    aio.send_data(danceabilityFeed.key, trackAudio["danceability"])
    aio.send_data(energyFeed.key, trackAudio["energy"])
    aio.send_data(instrumentalnessFeed.key, trackAudio["instrumentalness"])

def getMultipleTracksInfo(tracksIds, name):
    urlTracks = "https://api.spotify.com/v1/audio-features?ids="
    for trackId in tracksIds:
        urlTracks += trackId + ","
    urlTracks = urlTracks[:-1]

    respuestaHTTPtracks = requests.get(urlTracks, headers={"Authorization": token})
    tracks = respuestaHTTPtracks.json()

    danceability = 0
    energy = 0
    instrumentalness = 0

    for trackInfo in tracks["audio_features"]:
        danceability += trackInfo["danceability"]
        energy += trackInfo["energy"]
        instrumentalness += trackInfo["instrumentalness"]

    albumSize = len(tracks["audio_features"])

    danceability /= albumSize
    energy /= albumSize
    instrumentalness /= albumSize
    
    danceability = round(danceability, 3)
    energy = round(energy, 3)
    instrumentalness = round(instrumentalness, 3)
    
    print("Name:", name)
    print("Danceability:", danceability)
    print("Energy:", energy)
    print("Instrumentalness:", instrumentalness)
    print()

    aio.send_data(cancionesFeed.key, name)
    aio.send_data(danceabilityFeed.key, danceability)
    aio.send_data(energyFeed.key, energy)
    aio.send_data(instrumentalnessFeed.key, instrumentalness)

def getPlaylistInfo(playlistLink):
    playlistId = playlistLink.split('/')[-1].split('?')[0]

    urlQueryPlaylist = f"https://api.spotify.com/v1/playlists/{playlistId}"
    responsePlaylist = requests.get(urlQueryPlaylist, headers={"Authorization": token})
    playlist = responsePlaylist.json()

    tracksIds = []
    for track in playlist["tracks"]["items"]:
        if(track["track"] and track["track"]["type"] == "track"): tracksIds.append(track["track"]["id"])

    getMultipleTracksInfo(tracksIds, playlist["name"])

def getAlbumInfo(albumLink):

    albumId = albumLink.split('/')[-1].split('?')[0]

    urlQueryAlbum = f"https://api.spotify.com/v1/albums/{albumId}"
    responseAlbum = requests.get(urlQueryAlbum, headers={"Authorization": token})
    album = responseAlbum.json()

    tracksIds = []
    for track in album["tracks"]["items"]:
        if(track["type"] == "track"): tracksIds.append(track["id"])
        
    getMultipleTracksInfo(tracksIds, album["name"])

from Adafruit_IO import Client, Feed
import json

ADAFRUIT_IO_USERNAME = "YOUR ADAFRUIT.IO USERNAME"
ADAFRUIT_IO_KEY = "YOUR ADAFRUIT.IO KEY"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
danceabilityFeed = aio.feeds('danceability')
energyFeed = aio.feeds('energy')
instrumentalnessFeed = aio.feeds('instrumentalness')
cancionesFeed = aio.feeds('canciones')

print("Ingrese un link de una CANCION, PLAYLIST o ALBUM de Spotify para analizarlo! Si desea TERMINAR, ingrese un '0'")

while(True):
    link = input()
    if(link == "0"): break
    key = link.split('/')[-2]
    if(key == "track"): getTrackInfo(link)
    elif(key == "playlist"): getPlaylistInfo(link)
    else: getAlbumInfo(link)
    print("Ingrese un link de una CANCIÓN o un ÁLBUM de Spotify para analizarlo! Si desea TERMINAR, ingrese un '0'")
