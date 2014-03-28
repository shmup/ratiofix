import whatapi
import sqlite3
import urllib2
from subprocess import call
from pyquery import PyQuery as pq


class Torrent(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.votes = None
        self.time_filled = None
        self.download_url = None

api = whatapi.WhatAPI(username='jared', password='2YwwHl4EwjFmKyCTQoKK0VqZFVTnNIS1CIhU7sL7oFpdQAqcc3')
html = api.check_requests()
torrents = []
html_torrents = pq(html).find('.rowb')
db = sqlite3.connect('torrents.db')
authkey = "d47f7ec2d34ed7cca818eeab4519b877"
torrent_pass = "16bc0c98af3d7b0eae8ee38ba9d037ee"


def get_download_link(torrent_id):
    return ("https://what.cd/torrents.php?action=download" +
            "&id=" + torrent_id +
            "&authkey=" + authkey +
            "&torrent_pass=" + torrent_pass)


def torrent_name(torrent_id):
    return torrent_id + ".torrent"


def download_torrent(torrent):
    torrent = urllib2.urlopen(get_download_link(torrent.id))
    output = open(torrent_name(torrent.id), 'wb')
    output.write(torrent.read())
    output.close()


# Returns True if torrent exists
def db_check_exist(torrent_id):
    db = sqlite3.connect('torrents.db')

    cursor = db.cursor()
    cursor.execute('SELECT exists(select 1 FROM  torrents where id=\
                   ' + torrent_id + ' LIMIT 1);')

    return cursor.fetchone()[0] == 1


def db_add(torrent_id):
    db = sqlite3.connect('torrents.db')

    cursor = db.cursor()
    cursor.execute('INSERT INTO torrents values (' + torrent_id + ');')

    db.commit()


def trim_id(line):
    return line[line.rfind('=')+1:]

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
            album.id = trim_id(pq(cell).find('a').attr('href'))
            torrents.append(album)
        elif i > 3:
            break

hit_once = False

for torrent in torrents:
    if int(torrent.votes) > 20:
        if not db_check_exist(torrent.id):
            if not hit_once:
                call(['sm', 'big torrent!'])
            hit_once = True
            db_add(torrent.id)
            # print torrent.votes
            # print api.get_torrent(torrent.id)
