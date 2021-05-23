class Profile :
    def __init__(self, json):
        self.name = json["name"]
        self.quality = json["quality"]
        self.qualityTags = json["quality_tags"]
        self.size = json["size"]
        self.lang = json["lang"]
        self.langTags = json["lang_tags"]
