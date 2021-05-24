import os
import requests
import time
import json
from models.TrackerScraper import TrackerScraper
from models.TmdbAPI import TmdbAPI
from models.TorrentChooser import TorrentChooser
from models.Profile import Profile
from models.Torrent import Torrent
from models.TorrentEngine import TorrentEngine


class MediaManager :
    def __init__(self, trackerPath, profilePath, tmdbApiKey, downloadPath) :
        self.trackers = []
        for trackerConf in self.getFilesInDirectory(trackerPath) :
            file = open(trackerPath + trackerConf)
            conf = json.load(file)
            self.trackers.append(TrackerScraper(conf))
        self.tmdbApi = TmdbAPI(tmdbApiKey)
        self.torrentEngine = TorrentEngine("0.0.0.0", "6891", "", "0", "0")
        self.downloadPath = downloadPath
        self.profiles = []
        for profileConf in self.getFilesInDirectory(profilePath) :
            file = open(profilePath + profileConf)
            conf = json.load(file)
            self.profiles.append(conf)

    def getFilesInDirectory(self, path) :
        files = []
        for file in os.listdir(path) :
            files.append(file)
        return files
    
    def searchTitle(self, title) :
        return self.tmdbApi.searchMedia(title)
        
    def downloadTitle(self, title) :
        titles = []
        magnets = []
        seeds = []
        leeches = []
        sizes = []
        for tracker in self.trackers :
            result = tracker.find(title)
            titles.extend(result['titles'])
            magnets.extend(result['magnets'])
            seeds.extend(result['seeds'])
            leeches.extend(result['leeches'])
            sizes.extend(result['sizes'])
        chooser = TorrentChooser(title, self.profiles[0], seeds, leeches, sizes, titles, magnets)
        scores = chooser.fitProfile()
        bestScore, index = chooser.chooseBest(scores)
        torrent = Torrent(self.torrentEngine.addTorrent(magnets[index], self.downloadPath), True, True)
        torrent.resume()
        while not torrent.hasMetadata() :
            time.sleep(1.0)
        while torrent.getStatus() != "downloading" :
            time.sleep(1.0)
        while torrent.getStatus() != "seeding" :
            print("{} {}".format(torrent.getProgress(), torrent.getDownloadSpeed()))
