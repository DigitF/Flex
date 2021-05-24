from models.Media import Media

class Movie(Media):
    def __init__(self, tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, mediaType, casting):
        super().__init__(tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, mediaType)
        self.casting = casting