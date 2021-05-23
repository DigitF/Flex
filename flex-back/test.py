from models.MediaManager import MediaManager

mm = MediaManager("./trackers/", "./profiles/", "00e9022055ee3668ba734a4a70ff2755", "./downloads")
for media in mm.searchTitle("machete") :
    print(media.originalTitle)
mm.downloadTitle("Machete")