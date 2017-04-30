import telnetlib as tn
import importlib as imp
import BotElLib as bel
import BotElConfig as config
from time import sleep
from datetime import datetime
import sys

class BotEl:
    VERSION = "0.3.2"

    def __init__(self, verbose=False, configfile=None):
        bec = config.BotElConfig(configfile)
        options = bec.getConfig("General")
        self.verbose = True if (options["VERBOSE"] == "true" or verbose == True) else False
        self.logfile = self.loginit()
        self.username = options["MUSH_USERNAME"]
        self.password = options["MUSH_PASSWORD"]
        self.server = options["MUSH_SERVER"]
        self.port = int(options["MUSH_PORT"])
        self.owner = options["MUSH_OWNER"]
        self.attempts = int(options["CONNECT_ATTEMPTS"]) or 10
        self.getlibs(True)
        self.buffer = ""
        self.output("BotEl v{} starting up.".format(self.VERSION))

    def loginit(self):
        tn = datetime.now()
        return "logs/BotEl-{}-{}-{}.log".format(tn.year, tn.month, tn.day)

    def output(self, message, nolog=False):
        if self.verbose == True:
            print(message)
        if nolog == False:
            with open(self.logfile,"a+") as file:
                file.write("{}\n".format(message.rstrip('\n')))

    def speak(self, message, nolog=False):
        self.t.write(bytes("{}\n".format(message),"UTF-8"))
        self.output("Sent text: {}".format(message), nolog)

    def start(self):
        self.t = tn.Telnet(self.server, self.port)
        self.t.read_until(b"\"news\"")
        self.speak("connect {0} {1}\n".format(self.username, self.password))
        self.output("Connected to {}:{}. Owner is {}.".format(self.server, self.port, self.owner))

    def listen(self):
        while True:
            try:
                g = self.t.read_until(b'\r\n')
                try:
                    g = g.decode(encoding="iso-8859-1").strip()
                except UnicodeDecodeError:
                    try:
                        g = g.decode(errors="replace").strip()
                    except:
                        g = g.decode(errors="ignore").strip()
                if g == "{} pages: reload".format(self.owner):
                    self.getlibs(False)
                    self.speak("p {}=Okay, I reloaded everything.\n".format(self.owner))
                    self.output("Reloaded libraries.")
                elif g == "{} pages: shutdown".format(self.owner):
                    raise(KeyboardInterrupt)
                else:
                    out = self.libraries.textmatch(g)
                    if out != None:
                        if out == self.buffer:
                            sleep(5)
                            continue
                        else:
                            self.buffer = out
                            self.speak("{}\n".format(out))
                            #self.output("Sent text: {}.".format(out))
            except KeyboardInterrupt:
                break
            except EOFError:
                sleep(60)
                self.start()
                continue
            except:
                continue

    def getlibs(self, init):
        if not init:
            imp.reload(bel)
        self.libraries = bel.BotElLib(self.username, self.owner, self)

if __name__ == "__main__":
    verbose = True if "-v" in sys.argv else False
    be = BotEl(verbose)
    be.start()
    be.listen()
