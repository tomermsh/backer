from flask import Flask, jsonify, request, render_template
from fetch import fetch_tracks
import pafy
import webbrowser
import random
import json
import os

app = Flask(__name__)
app.config['TRACKS_DIR'] = "./tracks"
app.config['DATA_FILE'] = "./data.json"

data = {}
data['tracks'] = []

if not os.path.isfile(app.config['DATA_FILE']):
    with open(app.config['DATA_FILE'], 'w') as outfile:
        json.dump(data, outfile)

class Track:
    def __init__(self, filename, genre, key, bpm, duration, url):
        self.filename = filename
        self.genre = genre
        self.key = key
        self.bpm = bpm
        self.duration = duration
        self.url = url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download',methods=['POST'])
def download_track():
    try:
        genre = request.form['genre']
        key = request.form['key']
        bpm = request.form['bpm']

        search_results = fetch_tracks('backing track ' + genre + ' ' + key + ' ' + bpm)
        url = "http://www.youtube.com/watch?v=" + random.choice(search_results[:10])
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4a")
        filepath = bestaudio.download(filepath=app.config['TRACKS_DIR'], quiet=True)

        downloaded = Track(os.path.basename(filepath), genre, key, bpm, video.duration, url)

        with open(app.config['DATA_FILE'], 'r') as json_file:
            data = json.load(json_file)
        data['tracks'].append(downloaded.__dict__)

        with open(app.config['DATA_FILE'], 'w') as outfile:
            json.dump(data, outfile)

        return jsonify(status='ok', message='Downloaded "' + video.title + '"')

    except Exception,e:
        return jsonify(status='error', message=str(e))

@app.route('/play',methods=['POST'])
def play_track():
    try:
        filename = request.form['filename']
        webbrowser.open(app.config['TRACKS_DIR'] + "/" + filename)

        return jsonify(status='ok', message='Playing ' + filepath)

    except Exception,e:
        return jsonify(status='error', message=str(e))

@app.route('/tracks',methods=['POST'])
def get_tracks():
    try:
        with open(app.config['DATA_FILE'], 'r') as json_file:
            data = json.load(json_file)

        return jsonify(data['tracks'])

    except Exception,e:
        return jsonify(status='error', message=str(e))

if __name__ == '__main__':
        app.run()
