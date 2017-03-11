from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from fetch import fetch_tracks
import os, sys, subprocess
import random, re
import json
import pafy

app = Flask(__name__)
CORS(app)
app.config['TRACKS_DIR'] = "./tracks/"
app.config['DATA_FILE'] = "./metadata.json"

data = {}
data['tracks'] = []

class Track:
    def __init__(self, name, genre, key, bpm, duration, url):
        self.name = name
        self.genre = genre
        self.key = key
        self.bpm = bpm
        self.duration = duration
        self.url = url

if not os.path.isfile(app.config['DATA_FILE']):
    with open(app.config['DATA_FILE'], 'w') as outfile:
        json.dump(data, outfile)

@app.route('/')
def index():
    with open(app.config['DATA_FILE'], 'r') as json_file:
        data = json.load(json_file)
    return render_template('index.html',table=data['tracks'])

@app.route('/download',methods=['POST'])
def download_track():
    try:
        genre = request.form['genre']
        key = request.form['key']
        bpm = request.form['bpm']

        if not (len(key) <= 27):
            return jsonify(status='error', message='Invalid Genre value')

        if not (len(key) <= 3 and re.match("^[A-Za-z#]+$", key)):
            return jsonify(status='error', message='Invalid Key value')

        if not (len(bpm) <= 3 and bpm.isdigit()):
            return jsonify(status='error', message='Invalid BPM value')

        search_results = fetch_tracks('backing track ' + genre + ' ' + key + ' ' + bpm + ' bpm')
        url = "http://www.youtube.com/watch?v=" + random.choice(search_results[:10])
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4a")
        filepath = bestaudio.download(filepath=app.config['TRACKS_DIR'], quiet=True)

        downloaded = Track(os.path.splitext(os.path.basename(filepath))[0], genre.title(), key.title(), bpm, video.duration, url)

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
        name = request.form['name']

        open_file(os.path.abspath(app.config['TRACKS_DIR'] + "/" + name + ".m4a"))
        return jsonify(status='ok', message='Playing "' + name + '"')

    except Exception,e:
        return jsonify(status='error', message=str(e))

@app.route('/delete',methods=['POST'])
def delete_track():
    try:
        name = request.form['name']

        with open(app.config['DATA_FILE'], 'r') as json_file:
            data = json.load(json_file)
            for i in xrange(len(data['tracks'])):
                if data['tracks'][i]['name'] == name:
                    data['tracks'].pop(i)
                    break

        with open(app.config['DATA_FILE'], 'w') as outfile:
            json.dump(data, outfile)

        os.remove(os.path.abspath(app.config['TRACKS_DIR'] + "/" + name + ".m4a"))
        return jsonify(status='ok', message='Deleted "' + name + '"')

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

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

if __name__ == '__main__':
        app.run(debug=True)
