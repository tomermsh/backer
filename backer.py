#!/usr/bin/python

from fetch import fetch
import sys
import pafy
import webbrowser

search_results = fetch(sys.argv[1])
url = "http://www.youtube.com/watch?v=" + search_results[0]
video = pafy.new(url)
bestaudio = video.getbestaudio()
filename = bestaudio.download(quiet=True)

print(filename)
webbrowser.open(filename)
