from ConfigParser import ConfigParser
import whatapi
import sqlite3
import urllib2
from torrent import Torrent
from subprocess import call
from pyquery import PyQuery as pq
from twilio.rest import TwilioRestClient

class RatioFix(object):
    def __init__(self, config):
        cfg = ConfigParser()
        cfg.read(config)
        self.min_votes = cfg.get('settings', 'min_votes')
        self.api = whatapi.WhatAPI(config=config)
        self.db = sqlite3.connect('torrents.db')
        self.html = self.api.check_requests()
        self.torrents = []

    def run(self):
        self.find_torrents()
        for torrent in self.torrents:
            print 'saving ' + torrent.id + '.torrent'
            torrent.save()

    def find_torrents(self):
        for torrent in pq(self.html).find('.rowb'):
            text = pq(torrent).find('td')
            album = Torrent()
            for i, cell in enumerate(text):
                if i == 0:
                    album._title = pq(cell).text()
                elif i == 1:
                    album._votes = pq(cell).text()
                elif i == 3:
                    album._id = pq(cell).find('a').attr('href')
                elif i > 3:
                    break

            # if we already have processed this torrent, gtfo
            if self.db_check_exist(album.id):
                continue

            # if votes aren't high enough, gtfo
            if int(album.votes) >= int(self.min_votes):
                album.blob = self.api.get_torrent(album.id)
                self.torrents.append(album)

    """ Returns True if torrent exists """
    def db_check_exist(self, torrent_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT exists(select 1 FROM torrents where id=\
                    ' + torrent_id + ' LIMIT 1);')

        return cursor.fetchone()[0] == 1

    def db_add(self, torrent_id):
        if self.db_check_exist(torrent_id): return
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO torrents values (' + torrent_id + ');')
        db.commit()

    def sms(self, msg="BIG TORRENT!"):
        account_sid = "AC7bf5b0d18411238e4854e66e73344811"
        auth_token = "c5b8dea7225d3d63df07d437b997eaea"
        client = TwilioRestClient(account_sid, auth_token)
        client.messages.create(to="+14199570527",
                            from_="+14195000069",
                            body=msg)


RatioFix('stuff.cfg').run()
