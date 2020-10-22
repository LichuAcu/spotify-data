import requests, json

token = "Bearer BQB9At9VcCy92J4RycRklB_mMFPvLaLCmDru-6Kg4kdaOHrRl8_1Io-Z-Uc4qlNJBCW_k9CWKOjPeafZvsw1EAwXdDvuBmnqNcIAl8M5Est32DDU78jzIAi3P5F03nE47hS7UbAwXvQ"

def reloadInputs():
    print("Por favor, ingrese un número válido.\n")

def getTrackInfo(trackLink):
    trackId = trackLink.split('/')[-1]

    urlQuerytrack = f"https://api.spotify.com/v1/audio-features/{trackId}"
    respuestaHTTPtrack = requests.get(urlQuerytrack, headers={"Authorization": token})

    trackInfo = respuestaHTTPtrack.json()

    print("Danceability", trackInfo["danceability"])
    print("Energy", trackInfo["energy"])
    print("Instrumentalness", trackInfo["instrumentalness"])
    print()

def getMultipleTracksInfo(tracksIds):
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
    
    print("Danceability", danceability)
    print("Energy", energy)
    print("Instrumentalness", instrumentalness)
    print()

def getPlaylistInfo(playlistLink):
    playlistId = playlistLink.split('/')[-1].split('?')[0]

    urlQueryPlaylist = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?additional_types=track"
    respuestaHTTPplaylist = requests.get(urlQueryPlaylist, headers={"Authorization": token})
    playlist = respuestaHTTPplaylist.json()

    tracksIds = []
    for track in playlist["items"]:
        tracksIds.append(track["track"]["id"])

    getMultipleTracksInfo(tracksIds)

def getAlbumInfo(albumLink):

    albumId = albumLink.split('/')[-1].split('?')[0]

    urlQueryAlbum = f"https://api.spotify.com/v1/albums/{albumId}/tracks?limit=50"
    respuestaHTTPalbum = requests.get(urlQueryAlbum, headers={"Authorization": token})
    album = respuestaHTTPalbum.json()

    tracksIds = []
    for track in album["items"]:
        tracksIds.append(track["id"])
        
    getMultipleTracksInfo(tracksIds)

print("Ingrese un link de una CANCION, PLAYLIST o ALBUM de Spotify para analizarlo! Si desea TERMINAR, ingrese un '0'")

while(True):
    link = input()
    if(link == "0"): break
    key = link.split('/')[-2]
    if(key == "track"): getTrackInfo(link)
    elif(key == "playlist"): getPlaylistInfo(link)
    else: getAlbumInfo(link)
    print("Ingrese un link de una CANCIÓN o un ÁLBUM de Spotify para analizarlo! Si desea TERMINAR, ingrese un '0'")