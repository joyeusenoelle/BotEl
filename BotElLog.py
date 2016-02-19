from datetime import datetime
import random as r
import re
import ftplib

class BotElLog():
    """ Logs text into a file.
    """
    def __init__(self, mush_name=None):
        self.mush = mush_name or "Saminga"
        self.connr = re.compile(r".+ has [disre]*connected.")
        self.curlog = None

    def startLog(self, players=None):
        """ Sets up the log, including player colors if assigned.
        """
        colors = ["#AA0000","#00AA00","#0000AA","#AAAA00","#AA00AA","#00AAAA",
                  "#882200","#008822","#220088","#888822","#882288","#228888",
                  "#440000","#440044","#004444"]
        tn = datetime.now()
        minit = tn.minute
        if minit < 10:
            minit = "0{}".format(minit)
        tnstr = "{}/{}/{}, starting {}:{}".format(tn.month, tn.day, tn.year, tn.hour, minit)
        self.curlog = "{}-{}-{}-{}_{}-{}.html".format(self.mush, tn.year, tn.month, tn.day, tn.hour, minit)
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
        htext = "<html>\n<head>\n<style type=\"text/css\">{}</style>\n</head>\n<body>\n<h2>{} log {}</h2>\n<div id=\"content\">\n".format(styletext, self.mush, tnstr)

        with open(self.curlog,"a+") as file:
            file.write(htext)
        
    def stopLog(self):
        """ Writes closing HTML and closes the log.
        """
        with open(self.curlog, "a+") as file:
            htext = "</div>\n</body>\n</html>"
            file.write(htext)

# write generalized code to handle FTP
# use remoteserver, remoteuser, remotepw, remotedir, finalremotedir

#        with open(self.curlog, "rb+") as file:
#            with ftplib.FTP(remoteserver, remoteuser, remotepw) as ftp:
#                ftp.cwd(remotedir)
#                ftp.storbinary("STOR {}".format(self.curlog), file)
#        remotefile = "http://{}/{}".format(finalremotedir, self.curlog)
        self.curlog = None
#        return "I uploaded the log to {} .".format(remotefile)
        return "Okay, I stopped logging." # remove this

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