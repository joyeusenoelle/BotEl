from datetime import datetime
import random as r
import re
import ftplib
import BotElConfig

class BotElLog():
    """ Logs text into a file.
    """
    def __init__(self):
        bec = BotElConfig.BotElConfig()
        options = bec.getConfig("InputLog")
        self.prefix = options["LOG_PREFIX"] or "Saminga"
        self.username = options["LOG_USERNAME"]
        self.password = options["LOG_PASSWORD"]
        self.server = options["LOG_SERVER"]
        self.cwd = options["LOG_CWD"]
        self.url = options["LOG_URL"]
        self.connr = re.compile(r".+ has [disre]*connected.")
        self.curlog = None

    def startLog(self, players=None):
        """ Sets up the log, including player colors if assigned.
        """
        colors = ["#AA0000","#00AA00","#0000AA","#AAAA00","#AA00AA","#00AAAA",
                  "#882200","#008822","#220088","#888822","#882288","#228888",
                  "#440000","#440044","#004444"]
        tn = datetime.now()
        minute = tn.minute
        hour = tn.hour
        day = tn.day
        month = tn.month
        if minute < 10:
            minute = "0{}".format(minute)
        if hour < 10:
            hour = "0{}".format(hour)
        if day < 10:
            day = "0{}".format(day)
        if month < 10:
            month = "0{}".format(month)
        tnstr = "{}/{}/{}, starting {}:{}".format(month, day, tn.year, hour, minute)
        self.curlog = "{}-{}-{}-{}_{}-{}.html".format(self.prefix, tn.year, month, day, hour, minute)
        styletext = "\n.OOC { color: #666666; }\n.DICE { color: #883333; }\n"
        if players != None:
            ply = players.split(",")
            for player in ply:
                player = player.strip()
                try:
                    color = colors.pop(r.randint(0,len(colors)-1))
                except:
                    color = "#000000"
                styletext += ".{}".format(player)
                styletext += " { color: "
                styletext += "{}; ".format(color)
                styletext += "}\n"
        htext = "<html>\n<head>\n<style type=\"text/css\">{}</style>\n</head>\n<body>\n<h2>{} log {}</h2>\n<div id=\"content\">\n".format(styletext, self.prefix, tnstr)

        with open(self.curlog,"a+") as file:
            file.write(htext)
        
    def stopLog(self):
        """ Writes closing HTML and closes the log.
        """
        with open(self.curlog, "a+") as file:
            htext = "</div>\n</body>\n</html>"
            file.write(htext)
        output = "Okay, I stopped logging."
        if self.username:
            with open(self.curlog, "rb+") as file:
                with ftplib.FTP(self.server,self.username,self.password) as ftp:
                    ftp.cwd(self.cwd)
                    ftp.storbinary("STOR {}".format(self.curlog), file)
            remotefile = "http://{}/{}".format(self.url, self.curlog)
            output += " I uploaded the log to {} .".format(remotefile)
        self.curlog = None
        return output

    def appendLog(self, text):
        """ Appends a line to the log as long as it's not a connection notice.
        """
        match = self.connr.search(text)
        if match == None:
            with open(self.curlog, "a+") as file:
                cls = text.split(" ",1)[0]
                if cls == "<<OOC>>":
                    cls = "OOC"
                if cls == "<<DICE>>":
                    cls = "DICE"
                text = text.replace("<","&lt;")
                text = text.replace(">","&gt;")
                file.write("<p class=\"{}\">{}</p>\n".format(cls, text))