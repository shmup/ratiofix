#!/usr/bin/env python

from optparse import OptionParser
from ConfigParser import ConfigParser
import whatapi
import sqlite3
import urllib2
from subprocess import call
from pyquery import PyQuery as pq
from twilio.rest import TwilioRestClient


class Torrent(object):
    def __init__(self):
        self._id = None
        self._title = None
        self._votes = None
        self.blob = None

    @property
    def id(self):
        return self._id[self._id.rfind('=')+1:]

    @property
    def title(self):
        return self._title.strip()

    @property
    def votes(self):
        return self._votes.strip()

    def save(self):
        with open(self.id + '.torrent', 'wb') as handle:
            for block in self.blob.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

class RatioFix(object):
    def __init__(self, settings):
        self.settings = settings
        self.api = whatapi.WhatAPI(username=settings['username'],
                                   password=settings['password'])
        self.db = sqlite3.connect('torrents.db')
        self.html = self.api.get_filled_requests()
        self.torrents = []

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
            if int(album.votes) >= int(self.settings['min_votes']):
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

    def start(self):
        self.find_torrents()
        for torrent in self.torrents:
            print 'saving ' + torrent.id + '.torrent'
            torrent.save()


def main():

    parser = OptionParser()

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print "Usage: _ratiofix.py configfile"
        exit(1)

    settings = {}

    config = ConfigParser()
    config.read(args[0])


    for option in config.options("settings"):
        settings[option] = config.get("settings", option)
    
    fixit = RatioFix(settings)
    fixit.start()

if __name__ == "__main__":
    main()
