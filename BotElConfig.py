import re

class BotElConfig:
    def __init__(self, filename=None):
        self.filename = filename or "config.txt"

    def getConfig(self, section=None):
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
#                    print("New header: {}".format(match.group(1)))
                    currentheader = match.group(1)
                    options[currentheader] = dict()
                else:
                    if line[0] == "#":
                        continue
#                    print("Option: {}".format(line))
                    optname, optvalue = line.split("=")
                    options[currentheader][optname] = optvalue
        if section == None:
            return options
        else:
            try:
                return options[section]
            except:
                raise KeyError("The specified section ({}) does not exist in the specified configuration file ({}).".format(section, self.filename))