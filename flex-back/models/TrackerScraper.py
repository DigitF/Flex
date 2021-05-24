from models.AsyncHttp import AsyncHttp
from aiohttp import ClientSession, TCPConnector
from parsel import Selector
from collections import OrderedDict
import asyncio
import codecs
import unicodedata


class TrackerScraper:
    def __init__(self, tracker):
        self.clientSession = ClientSession()
        self.tracker = tracker
        self.results = {}
        if 'login' in self.tracker :
            self.login()

    async def post(self, data):
        async with self.clientSession.post(self.tracker["login"]["loginUrl"], data = data) as resp :
            return await resp.content.read()

    def login(self):
        payload = {self.tracker["login"]["usernameString"] : self.tracker["login"]["username"], self.tracker["login"]["passwordString"] : self.tracker["login"]["password"], self.tracker["login"]["otherString"] : self.tracker["login"]["other"]}
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.post(payload)))

    async def getUrl(self, clientSession, url, order):
        async with self.clientSession.get(url) as resp :
            return await resp.content.read(), order

    async def close(self):
        await self.clientSession.close()
    
    def getUrls(self, urls):
        tasks = []
        for i in range(len(urls)) :
            tasks.append(self.getUrl(self.clientSession, urls[i], i))
        loop = asyncio.get_event_loop()
        results = [loop.run_until_complete(asyncio.gather(*tasks))]
        return results
    
    def find(self, search):
        search = search.replace(" ", self.tracker['searchSeparator'])
        self.results = { "search_init" : [str(self.tracker['search_init']).format(search = search)] }
        self.results["search_url"] = self.tracker['search_url']
        for step in self.tracker['flow'] :
            pages = self.getUrls(self.results[step])
            if len(pages[0]) > 1 : 
                for action in self.tracker['flow'][step] :
                    self.action(step, action, pages[0], search)
            else :
                for action in self.tracker['flow'][step] :
                    self.action(step, action, pages[0], search) 
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close())
        return self.results

    def action(self, step, action, pages, search):
        if action == "extract" :
            for result in self.tracker['flow'][step][action]['result'] :
                extracts = []
                for page in pages :
                    extract = Selector(text=bytes(page[0]).decode(self.tracker['charset'])).css(self.tracker['items'][result]['selector']).getall()
                    if result == "magnets" :
                        extract = list(OrderedDict.fromkeys(extract))
                    sanitized = [[unicodedata.normalize("NFKD", element)] for element in extract]
                    extracts = extracts + sanitized[0]
                if "filters" in self.tracker['items'][result] :
                    if self.tracker['items'][result]['filters'][0] == "s" :
                        filtered = []
                        for extract in extracts :
                            filtered.append(str(extract).split(self.tracker['items'][result]['filters'][1])[int(self.tracker['items'][result]['filters'][2])])
                        extracts = filtered
                    elif self.tracker['items'][result]['filters'][0] == "a" :
                        filtered = []
                        for extract in extracts :
                            filtered.append(self.tracker['items'][result]['filters'][2] + str(extract))
                        extracts = filtered
                    elif self.tracker['items'][result]['filters'][0] == "r" :
                        filtered = []
                        for extract in extracts :
                            filtered.append(str(extract).replace(self.tracker['items'][result]['filters'][1],self.tracker['items'][result]['filters'][2]))
                        extracts = filtered
                self.results[result] = extracts
        elif action == "create_search_urls" :
            lastpageDict = self.tracker['flow'][step][action]['params'][1]
            pageVar = self.tracker['flow'][step][action]['params'][1]
            searchUrlDict = self.tracker['flow'][step][action]['params'][0]
            self.results[self.tracker['flow'][step][action]['result'][0]] = []
            if len(self.results[lastpageDict]) > 0 :
                for i in range(int(self.results[lastpageDict][0])) :
                    self.results[self.tracker['flow'][step][action]['result'][0]].append(str(self.results[searchUrlDict]).format(search = search, page = int(self.tracker['start']) + i * int(self.tracker['steps'])))
            else :
                self.results[self.tracker['flow'][step][action]['result'][0]].append(str(self.results[searchUrlDict]).format(search = search, page = 1))
        elif action == "walk" :
            searchinit = self.results["search_init"][0].format(search = search)
            links = [searchinit]
            nextlink = searchinit
            while len(nextlink) > 0 :
                pages = self.getUrls([nextlink])
                extract = Selector(text=bytes(pages[0][0][0]).decode(self.tracker['charset'])).css(self.tracker['flow'][step][action]['params'][1]).get()
                if extract is not None :
                    nextlink = self.tracker['search_url'].format(page = extract.split('=')[2], search = search)
                    links.append(nextlink)
                else : 
                    nextlink = ""
            self.results[self.tracker['flow'][step][action]['result'][0]] = links
