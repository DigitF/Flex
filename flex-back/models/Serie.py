from models.Media import Media

class Serie(Media):
    def __init__(self, tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, mediaType, seasons):
        super().__init__(tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, mediaType)
        self.seasons = seasons