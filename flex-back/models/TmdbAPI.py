import requests
from models.Genre import Genre
from models.Media import Media
from models.Episode import Episode
from models.Season import Season
from models.Serie import Serie
from models.Movie import Movie
from models.People import People
from models.Department import Department
from models.Appearance import Appearance
from models.MediaType import MediaType

class TmdbAPI :
    def __init__(self, apikey):
        self.config =  {}
        self.config['apikey'] = apikey
        self.config['apiURL'] = "https://api.themoviedb.org/3"
        self.config['movieSearchEndpoint'] = "https://api.themoviedb.org/3/search/movie?api_key={apikey}&query={search}"
        self.config['movieCastEndpoint'] = "https://api.themoviedb.org/3/movie/{id}/credits?api_key={apikey}"
        self.config['episodeCastEndpoint'] = "https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}/credits?api_key={apikey}"
        self.config['serieSearchEndpoint'] = "https://api.themoviedb.org/3/search/tv?api_key={apikey}&query={search}"
        self.config['personSearchEndpoint'] = "https://api.themoviedb.org/3/search/person?api_key={apikey}&query={search}"
        self.config['movieGetEndpoint'] = "https://api.themoviedb.org/3/movie/{id}?api_key={apikey}"
        self.config['serieGetEndpoint'] = "https://api.themoviedb.org/3/tv/{id}?api_key={apikey}"
        self.config['personGetEndpoint'] = "https://api.themoviedb.org/3/person/{id}?api_key={apikey}"
        self.config['genreGetEndpoint'] = "https://api.themoviedb.org/3/genre/movie/list?api_key={apikey}"
        self.config['imageGetEndpoint'] = "https://image.tmdb.org/t/p/{size}{imgUrl}"
        self.config['serieSeasonEndpoint'] = "https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={apikey}"
        self.config['serieEpisodeEndpoint'] = "https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}?api_key={apikey}"
        self.session = requests.Session()
        self.genres = self.getGenres()

    def searchMovie(self, movieName):
        url = self.config['movieSearchEndpoint'].format(apikey = self.config['apikey'], search = movieName)
        request = self.session.get(url).json()
        return request

    def searchSerie(self, serieName):
        url = self.config['serieSearchEndpoint'].format(apikey = self.config['apikey'], search = serieName)
        request = self.session.get(url).json()
        return request

    def getInfoSerie(self, serieId):
        url = self.config['serieGetEndpoint'].format(apikey = self.config['apikey'], id = serieId)
        request = self.session.get(url).json()
        return request
        
    def getInfoMovie(self, movieId):
        url = self.config['movieGetEndpoint'].format(apikey = self.config['apikey'], id = movieId)
        request = self.session.get(url).json()
        return request

    def getCastMovie(self, movieId):
        url = self.config['movieCastEndpoint'].format(apikey = self.config['apikey'], id = movieId)
        request = self.session.get(url).json()
        return request

    def getCastEpisode(self, serieId, seasonNumber, episodeNumber):
        url = self.config['episodeCastEndpoint'].format(apikey = self.config['apikey'], tv_id = serieId, season_number = seasonNumber, episode_number = episodeNumber)
        request = self.session.get(url).json()
        return request

    def getPerson(self, castId):
        url = self.config['personGetEndpoint'].format(apikey = self.config['apikey'], id = castId)
        request = self.session.get(url).json()
        return request
    
    def getSeason(self, tvId, seasonNumber):
        url = self.config['serieSeasonEndpoint'].format(apikey = self.config['apikey'], tv_id = tvId, season_number = seasonNumber)
        request = self.session.get(url).json()
        return request   
    
    def getEpisode(self, tvId, seasonNumber, episodeNumber):
        url = self.config['serieEpisodeEndpoint'].format(apikey = self.config['apikey'], tv_id = tvId, season_number = seasonNumber, episode_number = episodeNumber)
        request = self.session.get(url).json()
        return request   

    def getGenres(self):
        genres = []
        url = self.config['genreGetEndpoint'].format(apikey = self.config['apikey'])
        request = self.session.get(url).json()
        for genre in request['genres'] :
            genres.append(Genre(genre['name'], genre['id']))
        return genres

    def castToObject(self, json):
        casting = []
        if 'cast' in json :
            for people in json['cast'] :
                peopleObj = self.tmdbPeopleToObject(self.getPerson(people['id']))
                department = Department.ACTOR
                character = people['character']
                person = self.tmdbPeopleToObject(self.getPerson(people['id']))
                casting.append(Appearance(person, department, character))
        if 'guest_star' in json :
            for people in json['guest_star'] :
                peopleObj = self.tmdbPeopleToObject(self.getPerson(people['id']))
                department = Department.ACTOR
                character = people['character']
                person = self.tmdbPeopleToObject(self.getPerson(people['id']))
                casting.append(Appearance(person, department, character))
        if 'crew' in json :
            for people in json['crew'] :
                character = ""
                if people['department'] == "Production" :
                    department = Department.PRODUCER
                elif people['department'] == 'Directing' :
                    department = Department.DIRECTOR
                elif people['department'] == 'Writing' : 
                    department = Department.WRITOR
                else :
                    department = Department.CREW
                person = self.tmdbPeopleToObject(self.getPerson(people['id']))
                casting.append(Appearance(person, department, character))
        return casting

    def EpisodeToObject(self, json, tvId, seasonNumber):
        name = json['name']
        order = json['episode_number']
        casting = self.castToObject(self.getCastEpisode(tvId, seasonNumber, order))
        releaseDate = json['air_date']
        overview = json['overview']
        stillUrl = json['still_path']
        return Episode(name, order, casting, releaseDate, overview, stillUrl)

    def SeasonsToObject(self, json, tvId, seasonNumber):
        order = seasonNumber
        episodes = []
        for episode in json['episodes'] :
            episodes.append(self.EpisodeToObject(episode, tvId, seasonNumber))
        overview = json['overview']
        posterUrl = json['poster_path']
        return Season(order, episodes, overview, posterUrl)
    
    def tmdbPeopleToObject(self, json):
        name = json['name']
        birthDate = json['birthday']
        bio = json['biography']
        deathDate = json['deathday']
        pictureURL = json['profile_path']
        return People(name, birthDate, bio, deathDate, pictureURL)

    def mediaToSerie(self, media):
        tvId = media.tmdbId
        seasons = []
        seasonNumber = self.getSeasonNumber(tvId)
        for i in range(1, seasonNumber + 1) :
            seasons.append(self.SeasonsToObject(self.getSeason(tvId, i), tvId, i))
        return Serie(media.tmdbId, media.originalTitle, media.genres, media.overview, media.originalLang, media.posterUrl, media.firstAir, media.mediaType, seasons)

    def mediaToMovie(self, media):
        return Movie(media.tmdbId, media.originalTitle, media.genres, media.overview, media.originalLang, media.posterUrl, media.firstAir, media.mediaType, self.castToObject(self.getCastMovie(media.tmdbId)))

    def tmdbMovieSearchToMedia(self, json):
        movies = []
        for movie in json['results'] :
            posterUrl = movie['poster_path']
            genres = []
            for genre_id in movie['genre_ids']:
                for genre in self.genres :
                    if genre_id == genre.tmdbId :
                        genres.append(genre)
                        break
            tmdbId = movie['id']
            originalLang = movie['original_language']
            originalTitle = movie['original_title']
            overview = movie['overview']
            if 'release_date' in movie:
                releaseDate = movie['release_date']
            else :
                releaseDate = 'notout'
            movies.append(Media(tmdbId, originalTitle, genres, overview, originalLang, posterUrl, releaseDate, MediaType.MOVIE))
        return movies
    
    def tmdbSerieSearchToMedia(self, json):
        series = []
        for serie in json['results'] :
            tmdbId = serie['id']
            genres = []
            for genre_id in serie['genre_ids']:
                for genre in self.genres :
                    if genre_id == genre.tmdbId :
                        genres.append(genre)
                        break
            if 'first_air_date' in serie:
                firstAir = serie['first_air_date']
            else :
                firstAir = 'notout'
            originalTitle = serie['original_name']
            originalLang = serie['original_language']
            overview = serie['overview']
            posterUrl = serie['poster_path']
            series.append(Media(tmdbId, originalTitle, genres, overview, originalLang, posterUrl, firstAir, MediaType.SERIE))
        return series
    
    def getSeasonNumber(self, tvId):
        url = self.config['serieGetEndpoint'].format(apikey = self.config['apikey'], id = tvId)
        request = self.session.get(url).json()
        return request['number_of_seasons']

    def searchMedia(self, title) :
        medias = []
        medias += self.tmdbMovieSearchToMedia(self.searchMovie(title))
        medias += self.tmdbSerieSearchToMedia(self.searchSerie(title))
        return medias