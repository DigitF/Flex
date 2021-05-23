import libtorrent

class Torrent :
    def __init__(self, handle, keepSeed, autoStart):
        self.handle = handle
        self.keepSeed = keepSeed
        self.status = autoStart
    
    def hasMetadata(self):
        return self.handle.has_metadata()

    def getStatus(self):
        state_str = ['queued', 'checking_files', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
        status = self.handle.status()
        print(status.state)
        return state_str[status.state]
    
    def getProgress(self):
        status = self.handle.status()
        return status.progress * 100

    def getDownloadSpeed(self):
        status = self.handle.status()
        return status.download_rate / 1000
    
    def getUploadSpeed(self):
        status = self.handle.status()
        return status.upload_rate / 1000
    
    def getPeersNum(self):
        status = self.handle.status()
        return status.num_peers

    def pause(self):
        self.status = 'paused'
        self.handle.pause()

    def resume(self):
        self.handle.resume()

    def reannounce(self):
        self.handle.force_reannounce()
