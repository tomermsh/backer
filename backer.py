from flask import Flask, jsonify, request
from fetch import fetch_tracks
import pafy
import webbrowser
import random

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/download',methods=['POST'])
def download_track():
    try:
        genre = request.form['genre']
        key = request.form['key']
        bpm = request.form['bpm']

        search_results = fetch_tracks('backing track ' + genre + ' ' + key + ' ' + bpm)
        url = "http://www.youtube.com/watch?v=" + random.choice(search_results[:10])
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        filename = bestaudio.download(quiet=True)

        return jsonify(status='ok',message='Downloaded "' + filename + '"')

    except Exception,e:
        return jsonify(status='error',message=str(e))
