import sys
import telnetlib as tn
import importlib as imp
import BotElLib as bel
from time import sleep

class BotEl:
    VERSION = "0.3.0"
    
    def __init__(self, username, password, server, port, owner, attempts=None):
        self.username = username
        self.password = password
        self.server = server
        self.port = int(port)
        self.owner = owner
        self.attempts = attempts or 10
        self.getlibs(True)
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
    username, password, server, port, owner = sys.argv[1:5]        
    be = BotEl(username, password, server, port, owner)
    be.start()
    be.listen()