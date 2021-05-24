import libtorrent

class TorrentEngine() :
    def __init__(self, listenInterface, port, outgoingInterface, maxDownloadRate, maxUploadRate) :
        self.listenInterface = listenInterface 
        self.port = int(port)
        self.outgoingInterface = outgoingInterface
        self.maxDownloadRate = maxDownloadRate
        self.maxUploadRate = maxUploadRate
        self.settings = {
            'user_agent': 'python_client/' + libtorrent.__version__,
            'listen_interfaces': '%s:%d' % (self.listenInterface, self.port),
            'download_rate_limit': int(self.maxDownloadRate),
            'upload_rate_limit': int(self.maxUploadRate),
            'alert_mask': libtorrent.alert.category_t.all_categories,
            'outgoing_interfaces': self.outgoingInterface
        }
        self.session = libtorrent.session(self.settings)

    def addTorrent(self, magnet, path) :
        params = {
            'save_path': path,
            'storage_mode': libtorrent.storage_mode_t(2),
            'sequential_download': True
        }
        return libtorrent.add_magnet_uri(self.session, magnet, params)