import json
from models.MediaType import MediaType
from flask import Flask, request
from models.TmdbAPI import TmdbAPI
app = Flask(__name__)
app.debug = True


@app.route('/autocomplete/')
def index():
    data = request.args.get("string")
    tapi = TmdbAPI("00e9022055ee3668ba734a4a70ff2755")
    result = tapi.searchMedia(data)
    prefetch = []
    for media in result :
        prefetch.append({'Title' : media.originalTitle, 'Overview' : media.overview, 'Poster' : media.posterUrl, 'Movie' : media.mediaType == MediaType.MOVIE})
    return json.dumps(prefetch)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)