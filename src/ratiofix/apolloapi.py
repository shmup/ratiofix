from ConfigParser import ConfigParser
import json
import requests

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'apolloapi [shmup]'
    }

class LoginException(Exception):
    pass


class RequestException(Exception):
    pass


class ApolloAPI:
    def __init__(self, config=None, username=None, password=None):
        self.session = requests.Session()
        self.session.headers = headers
        self.authkey = None
        self.passkey = None
        if config:
            cfg = ConfigParser()
            cfg.read(config)
            self.username = cfg.get('login', 'username')
            self.password = cfg.get('login', 'password')
        else:
            self.username = username
            self.password = password
        self._login()

    def _login(self):
        '''Logs in user and gets authkey from server'''
        loginpage = 'https://apollo.rip/login.php'
        data = {'username': self.username,
                'password': self.password,
                'keeplogged': 1,
                'login': 'Login'
        }
        r = self.session.post(loginpage, data=data, allow_redirects=False)
        if r.status_code != 302:
            raise LoginException
        accountinfo = self.request("index")
        self.authkey = accountinfo["response"]["authkey"]
        self.passkey = accountinfo["response"]["passkey"]

    def get_torrent(self, torrent_id):
        '''Downloads the torrent at torrent_id using the authkey and passkey'''
        torrentpage = 'https://apollo.rip/torrents.php'
        params = {'action': 'download', 'id': torrent_id}
        if self.authkey:
            params['authkey'] = self.authkey
            params['torrent_pass'] = self.passkey
        r = self.session.get(torrentpage, params=params, allow_redirects=False)
        if r.status_code == 200 and 'application/x-bittorrent' in r.headers['content-type']:
            return r
        return None

    def get_filled_requests(self):
        request_page = 'https://apollo.rip/requests.php?order=filled&sort=desc&'
        r = self.session.get(request_page, allow_redirects=False)
        if r.status_code == 200:
            return r.content
        return None

    def request(self, action, **kwargs):
        '''Makes an AJAX request at a given action page'''
        ajaxpage = 'https://apollo.rip/ajax.php'
        params = {'action': action}
        if self.authkey:
            params['auth'] = self.authkey
        params.update(kwargs)

        r = self.session.get(ajaxpage, params=params, allow_redirects=False)
        try:
            json_response = r.json()
            if json_response["status"] != "success":
                raise RequestException
            return json_response
        except ValueError:
            raise RequestException
