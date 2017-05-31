import re, urllib.request, urllib.parse, sys

class BotElWeather():
    """ Uses wttr.in to fetch the current weather forecast for a given location.
    """

    def __init__(self, prnt):
        self.prnt = prnt

    def getWeather(self, passed, requester=None, leader=None):
        if leader == None: leader = "\""
        if requester == None: requester = "Somebody"
        if self.isInt(passed[0]):
            arg = passed
        else:
            arg = "~" + "+".join(passed.split(" "))
        self.prnt.output("{} requested the weather for {}".format(requester, passed))
        url = "http://wttr.in/{}?0T".format(arg)
        self.prnt.output("Sending request: {}".format(url))
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent':'curl'
            }
        )
        try:
            weather = urllib.request.urlopen(req).read().decode()
        except:
            return "{}Sorry, I couldn't connect.".format(leader)

        wthr = self.sanitize(weather)
        self.prnt.output("Sanitized: {}".format(wthr))
        return "quote {}".format(wthr)

    def sanitize(self, text):
        text = re.sub(r"\n","%r",text)
        text = re.sub(r" ","%b",text)
        text = re.sub(r"\\u2013","-",text)
        text = re.sub(r"<[^>]+>","",text)
        text = re.sub("\\\\n","",text)
        text = re.sub("\\\\u.{4}","",text)
        text = re.sub("\\\\\"","\"",text)
        text = re.sub("\/[^\/]+\/","",text)
        text = re.sub("\[[^\]]+\]","",text)
        text = re.sub("%r%rNew.+$","",text)
        text = re.sub(r"\\","\\",text)
        #text = re.sub(r"[┌─┐┴└┘├┼┤┬]","%b",text)
        return text

    def isInt(self, s):
        try:
            if s.isdigit():
                return True
            return False
        except TypeError:
            return False
        except ValueError:
            return False
