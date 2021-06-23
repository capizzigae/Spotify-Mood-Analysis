
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time
import numpy as np
import json
import os
import socket
import sys

def request_Token():
    #Setto lo scope per la richiesta
    scope = "user-read-currently-playing"
    #autorizzo l'applicativo e prendo il token
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp

def normalize_Data(data):
    #min e max reali=-60 e 0, ma inserire tarati secondo il dataset
    return (data - (-37.521)) / ((-0.721) - (-37.521))


def find_feature(uri):
    sp=request_Token()
   
    return sp.audio_features(tracks=uri)

def get_current_track_feature(feature):
    if feature is None or len(feature) == 0 or feature[0] is None:
        #raise ValueError("Qualcosa è andato storto nella richiesta della feature")
        return None
    return {
        'uri': feature[0]['uri'],
        'Acousticness': feature[0]['acousticness'],
        'Danceability': feature[0]['danceability'],
        'Liveness': feature[0]['liveness'],
        'Loudness':feature[0]['loudness'],
        'Speechiness':feature[0]['speechiness'],
    }

def json_message(current_track):
    local_ip = socket.gethostbyname(socket.gethostname())
    json_data = json.dumps(current_track)
    #print("Current: track %s" % json_data)

    send_message(json_data + ";")

    return json_data



def send_message(current_track):
    HOST, PORT = "localhost" ,8192
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # s.bind((HOST,PORT))
        s.connect((HOST, PORT))
        s.sendall(current_track.encode())
        #current_track = s.recv(1024)
        #s.close()
    #print('Received', repr(current_track))

def put_in_json(current_track):
    with open('songs_log.json','a') as outfile:
        json.dump(current_track,outfile)
        outfile.close()
    with open('songs_log.txt','a') as outfile:
        json.dump(current_track,outfile)
        outfile.write('\n')
        outfile.close()

def get_current_track(sp):
    return sp.current_user_playing_track()

def get_current_track_info(sp):
    current_track=get_current_track(sp)
    
    artist=current_track['item']['artists'][0]['name']
    song = current_track['item']['name']
    uri = current_track['item']['uri']
    dic={
        'Artist': artist,
        'Song': song,
        'uri': uri,
    }

    dic2= get_current_track_feature(find_feature(uri=uri))
    dic.update(dic2)
    dic['Loudness']=normalize_Data(dic['Loudness'])
    return dic

def main():
    current_track_uri= None
    while True:
        sp=request_Token()
        
        current_track_info=get_current_track_info(sp)

        if current_track_info['uri']!=current_track_uri:
            print(current_track_info)
            put_in_json(current_track_info)
            json_message(current_track_info)
            current_track_uri=current_track_info['uri']
        time.sleep(1)
main()