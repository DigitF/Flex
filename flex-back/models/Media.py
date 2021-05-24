import json

class Media :
    def __init__(self, tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, mediaType):
        self.tmdbId = tmdbId
        self.genres = genres
        self.firstAir = firstAir
        self.originalTitle = originalTitle
        self.originalLang = originalLang
        self.overview = overview
        self.posterUrl = posterUrl
        self.mediaType = mediaType
