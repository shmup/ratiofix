import whatapi
from pyquery import PyQuery as pq


class Torrent(object):
    def __init__(self):
        self.title = None
        self.votes = None
        self.time_filled = None

api = whatapi.WhatAPI(username='jared', password='2YwwHl4EwjFmKyCTQoKK0VqZFVTnNIS1CIhU7sL7oFpdQAqcc3')
html = api.check_requests()
torrents = []
html_torrents = pq(html).find('.rowb')

for torrent in html_torrents:
    text = pq(torrent).find('td')

    album = Torrent()

    for i, cell in enumerate(text):
        if i == 0:
            album.title = pq(cell).text()
        elif i == 1:
            album.votes = pq(cell).text()
        elif i == 3:
            album.time_filled = pq(cell).text()
            torrents.append(album)
        elif i > 3:
            break

print torrents[0].time_filled




