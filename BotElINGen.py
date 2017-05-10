import random
from datetime import datetime

class BotElINGen():
    """ Creates random In Nomine characters.
    """
    def __init__(self, prnt=None, maxforces=None):
        self.prnt = prnt
        self.MAXFORCES = maxforces or 9
        self.SKILLPOINTS = self.MAXFORCES * 4
        self.characters = dict()
        self.loadCharacters()
        self.words = {"angel":["Dreams","Children","Stone","Judgment","Creation","Fire","the Wind","Lightning","Animals","Faith","the Sword","Revelation","Trade","War","Flowers","the Waters","Knowledge","Purity","Destiny","Protection","Death"],
                      "demon":["Nightmares","Lust","the Game","the War","Corruption","Fire","Drugs","Hardcore","Secrets (shhh!)","Gluttony","Dark Humor","Fate","Corruption","Freedom","Cruelty","Disease","Factions","Greed","Oblivion","Sloth","the Media","Death","Theft","Technology","the Oceans"]}
        self.types = {"angel":["Serꙮph","Cherub","Ofanite","Elohite","Malakite","Kyriotate","Mercurian","Bright Lilim"],
                      "demon":["Balserꙮph","Djinn","Calabite","Habbalite","Lilim","Shedite","Impudite"]}
        self.namelist = ["Barbara","Marita","Ridwan","Wu","Wallace","Marcella","Bedwyr","Diamantina","Jaroslava","Lennard","Zahi","Braith","Dajana","Jessalyn","Dieuwert","Neven","Yehudah","Panayiotis","Vasanta","Jumaane","Valerie","Erlea","Mujo","Farooq","Arachne","Mile","Nensi","Radoslava","Zosia","Lilianne","Alphege","Regina","Lumusi","Abelone","Sixten","Lorita","Hode","Natalija","Franzi","Bogdana","Maurus","Mariya","Noel","Gottfrid","Miloslav","Hakon","Bartosz","Ljubica","Chrysanthe","Aeneas","Floriana","Ata","Maala","Francesca","Albert","Vladimira","Meridith","Dewey","Elis","Silvester","Petre","Veslemoy","Fahim","Vassilis","Tonina","Dionne","Inge","Sagi","Ira","Edgar","Liliana","Benedictus","Jadranka","Giacinto","Ivana","Lumusi","Ljuba","Shanae","Elmo","Luisa","Kobe","Samuel","Alexandre","Septima","Silvio","Melantha","Neve","Sandra","Odon","Steinn","Gavriilu","Joel","Gloriana","Iva","Hippokrates","Yadon","Shiphrah","Thurayya","Ichabod","Gerwazy","Tahirih","Nereus","Iair","Ekkehard","Lucia","Hrafn","Anatoliu","Shun","Csilla","Trista","Estevao","Sheena","Nicholas","Fuat","Nelinha","Opeyemi","Esmund","Ellar","Aruna","Ljuba","Anastazie","Jason","Unnur","Natalia","Rosalba","Gerulf","Kristy","Eilidh","Caroline","Mordecai","Traian","Roza","Cadence","Parth","Mykhaylo","Zuzanna","Ivette","Paega","Xolani","Deidre","Malik","Heike","Lazaros","Jeroen","Iairus","Kimball","Marco","Max","Guifre","Yutke","Vlad","Lestat","Zaahira","Vinay","Sini","Venus","Danijel","Bor","Baldur","Ozbej","Delilah","Dragan","Niv","Neas","Jenci","Moysei","Apollon","Hulda","Boris","Hannah","Pandora","Loic","Quirijn","Pene","Paderau","Gabino","Adrian","Agne","Sumati","Onni","Fabian","Eugenie","Debbie","Taner","Agape","Manno","Allegria","Kore","Roma","Avgustin","Murali","Helge","Caitlyn","Sa'dia","Marianne","Cinzia","Maribel","Jamshed","Cedomir","Kaveh","Vita","Sharma","Micaiah","Shadya","Marie","Ibbie","Micheline","Cipriano","Peregrine","Chinasa","Ketilridr","Tamara","Klimentina","Cnut","Darko","Gaizka","Ogden","Ghayth","Dionisie","Jeannie","Euadne","Rizwan","Abel","Faiga","Liadan","Merce","Ronald","Stigr","Durai","Jelena","Nudd","Origenes","Xavia","Yissakhar","Abigail","Irmentrud","Klavdija","Lucija","Romaine","Virgil","Cerridwen","Jayendra","Judah","Sunshine","Theodoar","Tiw","Brigid","Fearghas","Ife","Lara","Liviana","Rocco","Branislav","Carpus","Gwythyr","Jacki","Lazer","Priya","Faustino","Josiah","Justin","Leobwin","Mahmood","Salih","Ailen","Evadne","Felicia","Pelagius","Presley","Botros","Donovan","Gregor","Keiko","Radoslav","Thanatos","Baxter","Bedelia","Edison","Govinda","India","Nazario","Astraea","Davor","Mao","Sergey","Sjurd","Stafford","Abd-al-Qadir","Domotor","Evaristus","Garbi","Jeffry","Rayen","Carolina","Cordelia","Eva","Ingi","Naseer","Oona","Ansobert","Antigone","Lorrin","Paget","Walter","Christoffer","Felix","Gormlaith","Pilvi","Anais","Merav","Pablo","Zdeslav"]
        self.skills = {"Corporeal": ["Acrobatics","Climbing","Dodge","Escape","Fighting","Large Weapon","Move Silently","Running","Swimming","Throwing"],
                       "Ethereal": ["Knowledge","Knowledge","Knowledge","Area Knowledge","Area Knowledge","Area Knowledge","Chemistry","Computer Operation","Driving","Electronics","Engineering","Language","Lockpicking","Lying","Medicine","Ranged Weapon","Savoir-Faire","Small Weapon","Tactics"],
                       "Celestial": ["Artistry","Detect Lies","Emote","Fast-Talk","Seduction","Singing","Survival","Tracking"]}
        self.areaknowledge = ["Heaven","Hell","Marches","Caribbean","New York","New England","Florida","Atlanta","Texas","California","American Southwest","Pacific Northwest","Portland","Toronto","Vancouver","Mexico","Central America","Brazil","Argentina","England","London","France","Paris","Norway","Scandinavia","Greece","Egypt","North Africa","Sub-Saharan Africa","Saudi Arabia","Middle East","Russia","Moscow","China","Shanghai","Hong Kong","Japan","Hokkaido","Tokyo","Australia","Sydney","Melbourne","Perth","Fiji","Antarctica"]
        self.knowledge = ["Astronomy","Biology","Literature","Aircraft","American Football","Football","Baseball","Sumo","Giant Robot Anime","German Cuisine","Catholicism","Islam","Buddhism","Shinto","Architecture","Eschatology","Numinology","Role-Playing Games","Spelunking","Parliamentary Procedure","Olympic History","18th-Century Botanical Manuals","Photography","Marine Biology","Entomology","Archaeology"]
        self.language = ["Mandarin","Spanish","English","Hindi","Arabic","Portuguese","Bengali","Russian","Japanese","Punjabi","German","Javanese","Wu","Malay","Telugu","Vietnamese","Korean","French","Marathi","Tamil","Urdu","Turkish","Italian","Yue (Cantonese)", "Thai", "Latin", "Greek", "Ancient Egyptian", "Apache", "Ainu", "Aleut", "Inuit", "Mayan"]

    def createCharacter(self, name=None, side=None, ret=False):
        name = name or random.choice(self.namelist)
        id = random.randint(10000,99999)
        fullid = "{}{}".format(name,id)
        self.characters[fullid] = dict()
        self.characters[fullid]["name"] = name
        if side not in ["angel","demon"]:
            side = random.choice(["angel","demon"])
        self.characters[fullid]["type"] = random.choice(self.types[side])
        self.characters[fullid]["word"] = random.choice(self.words[side])
        self.characters[fullid]["attunements"] = ["{} of {}".format(self.characters[fullid]["type"], self.characters[fullid]["word"])]
        forces = {"Corporeal":1, "Ethereal":1, "Celestial":1}
        while sum(forces.values()) < self.MAXFORCES:
            forces[random.choice(list(forces.keys()))] += 1
        for realm, score in forces.items():
            self.characters[fullid][realm] = score
        ability_points = {"Corporeal":(forces["Corporeal"]*4),
                  "Ethereal":(forces["Ethereal"]*4),
                  "Celestial":(forces["Celestial"]*4)}
        abilities = {"Corporeal":{"Strength":1,"Agility":1},
                     "Ethereal":{"Intellect":1, "Precision":1},
                     "Celestial":{"Will":1,"Perception":1}}
        if (side == "angel" and self.characters[fullid]["type"] != "Kyriotate") or self.characters[fullid]["type"] == "Lilim":
            #print("It's an angel or a Lilim.")
            abilities["Celestial"]["Perception"] += 2
        elif (side == "demon" and self.characters[fullid]["type"] != "Lilim") or self.characters[fullid]["type"] == "Kyriotate":
            #print("It's a demon or a Kyrio.")
            abilities["Celestial"]["Will"] += 2
        else:
            #print("It's neither.")
            abilities["Celestial"]["Perception"] += 1
            abilities["Celestial"]["Will"] += 1
        for realm in abilities.keys():
            while sum(abilities[realm].values()) < ability_points[realm]:
                abilities[realm][random.choice(list(abilities[realm].keys()))] += 1
        for pair in abilities.values():
            for ability, score in pair.items():
                 self.characters[fullid][ability] = score
        skills = {}
        skilldelta = int(self.SKILLPOINTS*0.33) - 1
        skillpoints = self.SKILLPOINTS - random.randint(skilldelta,int(skilldelta*1.25))
        skrealms = []
        for realm,forces in forces.items():
            for _ in range(forces):
                skrealms.append(realm)
        while skillpoints > 1:
            choose = random.randint(0,9)
            if choose in range(0,5):
                # Skills!
                skill = random.choice(self.skills[random.choice(skrealms)])
                if (self.characters[fullid]["type"] == "Balseraph" or
                    self.characters[fullid]["type"] == "Seraph") and skill == "Lying":
                    continue
                if skill == "Knowledge":
                    skill += " ({})".format(random.choice(self.knowledge))
                if skill == "Area Knowledge":
                    skill += " ({})".format(random.choice(self.areaknowledge))
                if skill == "Language":
                    skill += " ({})".format(random.choice(self.language))
                if skill in skills.keys():
                    skills[skill] += 1
                    skillpoints = skillpoints - 1
                else:
                    spent = random.randint(1,3)
                    skills[skill] = spent
                    skillpoints = skillpoints - spent
            elif choose in range(5,9):
                pass
                # Songs!
            elif choose == 9:
                if random.randint(0,1) == 1:
                    atntypes = list(self.types[side])
                    atntypes.remove(self.characters[fullid]["type"])
                    atntype = random.choice(atntypes)
                    atnword = self.characters[fullid]["word"]
                else:
                    atntype = self.characters[fullid]["type"]
                    atnwords = list(self.words[side])
                    atnwords.remove(self.characters[fullid]["word"])
                    atnword = random.choice(atnwords)
                attunement = "{} of {}".format(atntype, atnword)
                self.characters[fullid]["attunements"].append(attunement)
                skillpoints = skillpoints - 10
                # Attunements!
        self.characters[fullid]["cpdelta"] = self.SKILLPOINTS - (sum(skills.values()) + ((len(self.characters[fullid]["attunements"])-1)*10))
        skills["Language (Local)"] = 3 # the character gets this for free, so don't count it in the delta
        self.characters[fullid]["skills"] = skills
        self.saveCharacters()
        if ret:
            return self.printCharacter(fullid, True)
        self.printCharacter(fullid)

    def listCharacters(self, ret=False):
        if len(self.characters) == 0:
            output = "No characters stored."
        else:
            output = ""
            for key, value in self.characters.items():
                output += "{}: {} ({} of {})\n".format(key, value['name'], value['type'], value['word'])
        if ret:
            return output
        self.prnt.output(output)

    def printCharacter(self, character, ret=False):
        if character not in self.characters.keys():
            output = "I don't have a character by that name."
        else:
            char = self.characters[character]
            output = ""
            output += "{}, {} of {}\n".format(char['name'], char['type'], char['word'])
            output += "Corporeal: {}\tEthereal: {}\tCelestial: {}\n".format(char['Corporeal'], char['Ethereal'], char['Celestial'])
            output += "Strength: {}\tIntellect: {}\tWill: {}\n".format(char['Strength'], char['Intellect'], char['Will'])
            output += "Agility: {}\tPrecision: {}\tPerception: {}\n".format(char['Agility'], char['Precision'], char['Perception'])
            output += "Skills: "
            skillout = ""
            for skill, score in sorted(char["skills"].items()):
                if skillout != "":
                    skillout += ", "
                skillout += "{}/{}".format(skill, score)
            output += "{}\n".format(skillout)
            atnout = ""
            for attunement in char["attunements"]:
                if atnout != "":
                    atnout += ", "
                atnout += attunement
            output += "Attunements: {}\n".format(atnout)
            output += "Remaining CP: {}".format(char['cpdelta'])
        if ret:
            return output
        else:
            self.prnt.output(output)

    def saveCharacters(self):
        try:
            with open("incharacters.txt", "w") as file:
                file.write(str(self.characters))
        except:
            self.prnt.output("Couldn't write to the character file.")

    def loadCharacters(self):
        try:
            with open("incharacters.txt", 'r+') as file:
                text = file.read()
            self.characters = eval(text)
        except:
            self.prnt.output("Couldn't read from the character file.")
            try:
                file = open('incharacters.txt', 'w')
                file.close()
                self.prnt.output("Created the character file.")
            except:
                self.prnt.output("Couldn't create the character file either.")
