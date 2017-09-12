import re

class Config:
    def __init__(self, filename=None):
        self.filename = filename or "config.txt"
        self.options = dict()

    def getConfig(self, section=None):
        if self.options == {}:
            options = dict()
            currentheader = ""
            with open(self.filename, "r+") as file:
                while True:
                    line = file.readline()
                    if line == "":
                        break
                    line = line.strip()
                    if line == "":
                        continue
                    match = re.match(r"# SECTION: ([^ ]+)", line)
                    if match:
                        currentheader = match.group(1)
                        options[currentheader] = dict()
                    else:
                        if line[0] == "#":
                            continue
                        optname, optvalue = line.split("=")
                        options[currentheader][optname] = optvalue
            self.options = options
        if section == None:
            return self.options
        else:
            try:
                return self.options[section]
            except:
                raise KeyError("The specified section ({}) does not exist in the specified configuration file ({}).".format(section, self.filename))
