import re, urllib.request, urllib.parse

class Wiki():
    """ Fetches the introduction of a Wikipedia article and strips it of
        characters that aren't MUSH-safe.
    """
    def __init__(self, prnt):
        self.prnt = prnt
        self.EOS = ['.', '?', '!']
        self.cache = dict()

    def smartTruncate(self, content, length=100, suffix='...'):
        """ Truncates text at no more than the specified length, but never
            breaking in the middle of a word. Trails off with the specified
            suffix if the text is truncated.
        """
        output = ""
        content_words = content.split()
        for word in content_words:
            output += " {}".format(word)
            if len(output) > length:
                if (word[-1] in self.EOS) or (word[-1] == '"' and word[-2] in self.EOS):
                    break
        return output

    def sanitize(self, text):
        text = re.sub(r"\\u2013","-",text)
        text = re.sub(r"<[^>]+>","",text)
        text = re.sub("\\\\n","",text)
        text = re.sub("\\\\u.{4}","",text)
        text = re.sub("\\\\\"","\"",text)
        text = re.sub("\/[^\/]+\/","",text)
        text = re.sub("\[[^\]]+\]","",text)
        return text

    def getWiki(self, qstr, requester=None, leader=None):
        """ Gets the Wikipedia entry.
        """
        if leader == None: leader = "\""
        if requester == None: requester = "Someone"
        self.prnt.output("{} requested a wikipedia entry for {}.".format(requester, qstr))
        qstr = urllib.parse.quote(qstr,':/')
        if qstr.lower() in self.cache.keys():
            self.prnt.output("Entry was cached.")
            return "quote {}".format(self.cache[qstr.lower()])
        url = "http://en.wikipedia.org/w/api.php?action=query&titles={}&prop=extracts&exintro=True&format=json&redirects".format(qstr)
        try:
            wintro = urllib.request.urlopen(url).read().decode()
        except:
            return "{}Sorry, I couldn't connect to Wikipedia.".format(leader)
        if re.search(r"\"pages\":\{\"-1\"", wintro) != None:
            # this could probably use string.replace() just fine
            return "{}Sorry, Wikipedia doesn't have a page that matches {}.".format(leader, re.sub(r"%20", " ", qstr))
        wintro = re.search(r"\"extract\":\"([^\}]+)",wintro).group(1)[:-1]
        wintro = self.sanitize(wintro)
        wintrosm = self.smartTruncate(wintro, 1000)
        wintrosm += "%r%rRead more: http://en.wikipedia.org/wiki/{}".format(re.sub(r"%20", "_", qstr))
        self.cache[qstr.lower()] = wintrosm
        return "quote {}".format(wintrosm)
