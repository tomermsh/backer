import urllib
import urllib2
import re

def fetch_tracks(query):
    query_string = urllib.urlencode({"search_query" : query})
    html_content = urllib2.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
    return search_results
