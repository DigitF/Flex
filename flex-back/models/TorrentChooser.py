class TorrentChooser :
    def __init__(self, search, profile,  seeds, leeches, sizes, titles, magnets) :
        self.search = search
        self.profile = profile
        self.seeds = seeds
        self.leeches = leeches
        self.sizes = sizes
        self.titles = titles
        self.magnets = magnets
    
    def chooseBest(self, scores) :
        best = 0
        index = 0
        for i in range(len(scores)) :
            if scores[i] > best :
                index = i
                best = scores[i]
        return best, index 

    def getHighestSeed(self) : 
        seedCopy = self.seeds
        seedCopy.sort(key = int, reverse = True)
        return seedCopy[0]

    def fitProfile(self) :
        scores = []
        bestSeed = self.getHighestSeed()
        for i in range(len(self.seeds)) :
            score = 0
            for criteria in self.profile :
                if criteria == "title" :
                    title = []
                    current = self.titles[0][i]
                    temp = current
                    for remove in self.profile[criteria]["remove"] :
                        current = current.replace(remove, " ")
                    for replacement in self.profile[criteria]["space"] :
                        title.append(temp.replace(" ", replacement))
                    for t in title :
                        if t.lower().find(self.search) >= 0 :
                            score += int(self.profile[criteria]["weight"])
                elif criteria == "size" :
                    print(self.sizes)
                    size, unit = self.sizes[i].split(" ")
                    if unit.lower().find("k") | unit.lower().find("m") :
                        score += int(self.profile[criteria]["weight"])
                    elif unit.lower().find("g") :
                        if score <= self.profile[criteria]["max"] :
                            score += int(self.profile[criteria]["weight"])
                else :
                    for tag in self.profile[criteria]["tags"] :
                        if self.titles[0][i].lower().find(tag.lower()) >= 0 :
                            score += int(self.profile[criteria]["weight"])
            score = score * (int(self.seeds[i]) / int(bestSeed))
            scores.append(score)
        return scores

