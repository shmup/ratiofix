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
