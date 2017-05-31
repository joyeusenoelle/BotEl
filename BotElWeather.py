import re, urllib.request, urllib.parse, sys

class BotElWeather():
    """ Uses wttr.in to fetch the current weather forecast for a given location.
    """

    def __init__(self, prnt):
        self.prnt = prnt

    def getWeather(self, passed, requester=None, leader=None):
        if leader == None: leader = "\""
        if requester == None: requester = "Somebody"
        if len(passed) == 1 and self.isInt(passed[0]):
            arg = passed[0]
        else:
            arg = "+".join(passed)
        s_passed = " ".join(passed)
        self.prnt.output("{} requested the weather for {}".format(requester, s_passed))
        url = "http://wttr.in/{}?1nT".format(arg)
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

        return "quote {}".format(self.sanitize(weather))

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
