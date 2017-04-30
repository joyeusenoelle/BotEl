import telnetlib as tn
import importlib as imp
import BotElLib as bel
import BotElConfig as config
from time import sleep

class BotEl:
    VERSION = "0.3.0"
    
    def __init__(self, configfile=None):
        bec = config.BotElConfig(configfile)
        options = bec.getConfig("General")
        self.username = options["MUSH_USERNAME"]
        self.password = options["MUSH_PASSWORD"]
        self.server = options["MUSH_SERVER"]
        self.port = int(options["MUSH_PORT"])
        self.owner = options["MUSH_OWNER"]
        self.attempts = int(options["CONNECT_ATTEMPTS"]) or 10
        self.getlibs(True)
        self.buffer = ""
        print("BotEl v{} starting up.".format(self.VERSION))
        
    def start(self):
        self.t = tn.Telnet(self.server, self.port)
        self.t.read_until(b"\"news\"")
        self.t.write(bytes("connect {0} {1}\n".format(self.username, self.password),"UTF-8"))
        print("Connected.")
        
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
                    self.t.write(bytes("p {}=Okay, I reloaded everything.\n".format(self.owner),"UTF-8"))
                    print("Reloaded libraries.")
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
                            self.t.write(bytes("{}\n".format(out),"UTF-8"))
                            print("Sent text: {}.".format(out))
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
        self.libraries = bel.BotElLib(self.username, self.owner)
           
if __name__ == "__main__":
    be = BotEl()
    be.start()
    be.listen()