import whatapi
import sqlite3
import urllib2
from subprocess import call
from pyquery import PyQuery as pq
from twilio.rest import TwilioRestClient


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


def sms(msg="BIG TORRENTS!"):
    account_sid = "AC7bf5b0d18411238e4854e66e73344811"
    auth_token = "c5b8dea7225d3d63df07d437b997eaea"
    client = TwilioRestClient(account_sid, auth_token)
    client.messages.create(to="+14199570527",
                           from_="+14195000069",
                           body=msg)


def get_download_link(torrent_id):
    return ("https://what.cd/torrents.php?action=download" +
            "&id=" + torrent_id +
            "&authkey=" + authkey +
            "&torrent_pass=" + torrent_pass)


def torrent_name(torrent_id):
    return torrent_id + ".torrent"


def download_torrent(name, torrent):
    with open(name + '.torrent', 'wb') as handle:
        for block in torrent.iter_content(1024):
                if not block:
                    break

                handle.write(block)


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


for torrent in torrents:
    hit_once = False

    if int(torrent.votes) >= 20:
        print torrent.id
        if not db_check_exist(torrent.id):
            if not hit_once:
                # download_torrent(torrent)
                download_torrent(torrent.id, api.get_torrent(torrent.id))
                sms()
            hit_once = True
            db_add(torrent.id)
