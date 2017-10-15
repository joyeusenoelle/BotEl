import random

# Global variables

RACES = {
  "Dwarf": {"Con":2},
  "Elf": {"Dex":2},
  "Halfling": {"Dex":2},
  "Human": {"Str":1,"Dex":1,"Con":1,"Int":1,"Cha":1,"Wis":1},
  "Dragonborn": {"Str":2,"Cha":1},
  "Gnome": {"Int":1},
  "Half-Elf": {"Cha":2,"Dex":1,"Int":1},
  "Half-Orc": {"Str":2,"Con":1},
  "Tiefling": {"Int":1,"Cha":2}
}

race_list = ["Dwarf","Elf","Halfling","Human","Dragonborn",
             "Gnome","Half-Elf","Half-Orc","Tiefling"]

class_list = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter_Arch","Fighter_Melee",
              "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

# Get skill names with self.SKILLS[n]
SKILLS = ["Athletics", #0
          "Acrobatics", #1
          "Sleight of Hand", #2
          "Stealth", #3
          "Arcana", #4
          "History", #5
          "Investigation", #6
          "Nature", #7
          "Religion", #8
          "Animal Handling", #9
          "Insight", #10
          "Medicine", #11
          "Perception", #12
          "Survival", #13
          "Deception", #14
          "Intimidation", #15
          "Performance", #16
          "Persuasion" #17
         ]

sel_class = None
sel_name = None
sel_race = None

# Global functions

def xdy(x, y):
    """ Rolls a y-sided die x times
    """
    ary = []
    for i in range(x):
        ary.append(random.randint(1,y))
    return ary

def xdyDrop(x, y, d):
    """ Rolls a y-sided die x times and drops the d lowest results
    """
    if d >= x:
        raise ValueError("The number of dice to drop must be less than the number of dice to roll.")
    ary = xdy(x,y)
    ary = sorted(ary)
    l = x - d
    return ary[-l:]

class Character:
    """ Parent class for D&D classes
    """

    # Class variables
    lb = "\n"
    name = ""
    class_name = ""
    sel_class = None
    sel_name = None
    sel_race = None
    stats = {
        "Str": 0,
        "Dex": 0,
        "Con": 0,
        "Int": 0,
        "Wis": 0,
        "Cha": 0
    }
    stat_weights = {
        "Str": 0,
        "Dex": 0,
        "Con": 0,
        "Int": 0,
        "Wis": 0,
        "Cha": 0
    }
    race = ""
    hit_die = 0
    hit_points = 0
    skills = []
    proficiencies = []
    abilities = []
    equipment = []
    background = ""
    saves = []
    potential_skills = []
    skill_num = 0
    wealth = 0

    def __init__(self, sel_name = None, sel_race = None):
        if sel_name == None:
            self.name = self.rName()
        else:
            self.name = sel_name
        if sel_race == None:
            self.race = random.choice(race_list)
        else:
            self.race = sel_race

    def doStats(self):
        self.assignStats()
        self.statMod(self.race)
        self.hit_points = self.hit_die + int((self.stats["Con"]-10)/2)
        self.skills = self.assignSkills()

    def statMod(self,cls):
        """ Adds race-based modifiers to the character's statistics
        """
        mods = RACES[cls]
        for stat, modifier in mods.items():
          self.stats[stat] = self.stats[stat] + modifier

    def rName(self):
        """ Generates a random name between 5 and 9 characters long.
            Picks randomly between a vowel and a consonant to start, then
            alternates vowels with consonants
        """
        vowels = ["a","e","i","o","u","w","y"]
        consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","z"]
        ln = random.randint(0,5) + 4
        nm = ""
        toggle = True if random.randint(0,1) == 1 else False
        for i in range(ln):
            if toggle:
                nm += random.choice(consonants)
            else:
                nm += random.choice(vowels)
            toggle = False if toggle == True else True
        return nm.capitalize()

    def getStats(self):
        """ Generates stats for the character
              Rolls 4d6, drops the lowest, sums the result; repeats 6 times
        """
        local_stats = []
        for j in range(6):
            local_stats.append(sum(xdyDrop(4,6,1)))
        local_stats.sort()
        return local_stats

    def assignStats(self, rs = None):
        """ Assigns stats based on the generated class's stat priority
          If a list of stats is passed in, use that; otherwise use getStats
        """
        raw_stats = self.getStats() if rs == None else rs
        raw_stats.sort()
        for nm, wgt in self.stat_weights.items():
          self.stats[nm] = raw_stats[wgt-1]

    def assignSkills(self, ps = None, ns = None):
        """
        Picks random skills from the class's skill list
        If a list of potential skills is passed in, use that
        otherwise use the default
        If a number of skills to pick is passed in, use that
        otherwise use the default
        """
        pskills = self.potential_skills if ps == None else ps
        nskills = self.skill_num if ns == None else ns
        final_skills = []
        for i in range(nskills):
            cskill = random.choice(pskills)
            final_skills.append(SKILLS[cskill])
            pskills.remove(cskill)
        return final_skills

    def getGold(self, num_dice, multiplier):
        """
        Get character starting gold (xd4 * 1 for monks, xd4 * 10 for others)
        """
        return sum(xdy(num_dice,4)) * multiplier

    def toString(self, lb = None):
        """
            Print a digest of the character
            $lb is the line break; \n by default, %r optionally
        """
        lb = self.lb if lb == None else lb
        output = ""
        output += "{} - {} {} 1{}".format(self.name, self.race, self.class_name, lb)
        output += "Background: {}{}".format(self.background, lb)
        for nm, score in self.stats.items():
            output += "{}: {}{}".format(nm, score, lb)
        output += "{} HP{}".format(self.hit_points, lb)
        their_stuff = {
            "Saving throws" : self.saves,
            "Skills"        : self.skills,
            "Proficiencies" : self.proficiencies,
            "Abilities"     : self.abilities,
            "Equipment"     : self.equipment,
        }
        for k,v in their_stuff.items():
            output += "{}: {}{}".format(k, ", ".join(v), lb)
        output += "Gold: {}{}".format(self.wealth, lb)
        return output

    def print_it(self):
        print(self.toString())

class Barbarian(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
          "Str": 6,
          "Dex": 4,
          "Con": 5,
          "Int": 1,
          "Wis": 2,
          "Cha": 3
        }
        self.class_name = "Barbarian"
        self.hit_die = 12
        self.saves = ["Str","Con"]
        self.equipment = [random.choice(["Greataxe","Martial melee weapon"]),
                     random.choice(["Handaxe * 2","Simple weapon"]),
                     "Explorer's pack", "Javelin * 4"]
        self.potential_skills = [9, 0, 15, 7, 12, 13]
        self.skill_num = 2
        self.proficiencies = ["Light armor","Medium armor","Shields",
                          "Simple weapons","Martial weapons"]
        self.abilities = ["Rage"]
        self.background = "Outlander"
        self.wealth = self.getGold(2,10)
        self.doStats()

class Bard(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 1,
            "Dex": 5,
            "Con": 2,
            "Int": 4,
            "Wis": 3,
            "Cha": 6
        }
        self.class_name = "Bard"
        self.hit_die = 8
        self.saves = ["Dex","Cha"]
        self.equipment = [random.choice(["Rapier","Longsword","Simple weapon"]),
                     random.choice(["Diplomat's pack","Entertainer's pack"]),
                     random.choice(["Lute","Musical instrument"]),
                     "Leather armor", "Dagger"]
        self.potential_skills = SKILLS
        self.skill_num = 3
        self.proficiencies = ["Light armor","Simple weapons","Hand crossbows",
                         "Longswords","Rapiers","Shortswords"]
        self.abilities = ["Cantrips * 2","Spells * 4"]
        self.background = "Entertainer"
        self.wealth = self.getGold(5,10)
        self.doStats()

class Cleric(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 4,
            "Dex": 1,
            "Con": 5,
            "Int": 3,
            "Wis": 6,
            "Cha": 2
        }
        self.class_name = "Cleric"
        DOMAINS = ["Knowledge", "Life", "Light", "Nature",
                     "Tempest", "Trickery", "War"]
        self.hit_die = 8
        self.saves = ["Wis","Cha"]
        self.equipment = ["Mace",random.choice(["Scale mail","Leather Armor"]),
                  random.choice([["Light Crossbow","Bolts * 20"],"Simple weapon"]),
                  random.choice(["Priest's pack","Explorer's pack"]),
                  "Shield", "Holy symbol"]
        self.potential_skills = [5, 10, 11, 17, 8]
        self.skill_num = 2
        self.proficiencies = ["Light armor","Medium armor","Shields","Simple weapons"]
        self.abilities = ["Domain: " + random.choice(DOMAINS),
                 "Cantrips * 3", "Spells"]
        self.background = "Acolyte"
        self.wealth = self.getGold(5,10)
        self.doStats()

class Druid(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 2,
            "Dex": 3,
            "Con": 5,
            "Int": 4,
            "Wis": 6,
            "Cha": 1
        }
        self.class_name = "Druid"
        self.hit_die = 8
        self.saves = ["Wis","Int"]
        self.equipment = ["Herbalism kit", random.choice(["Wooden shield","Simple weapon"]),
                 random.choice(["Scimitar","Melee weapon"]), "Leather armor",
                 "Explorer's pack", "Druidic focus"]
        self.potential_skills = [4, 9, 10, 11, 7, 12, 8, 13]
        self.skill_num = 2
        self.proficiencies = ["Light armor","Medium armor","Shields",
                      "Clubs","Daggers","Darts","Javelins","Maces",
                      "Quarterstaves","Scimitars","Sickles","Slings","Spears"]
        self.abilities = ["Druidic language", "Cantrips * 2", "Spells"]
        self.background = "Hermit"
        self.wealth = self.getGold(2,10)
        self.doStats()

class FighterArch(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 4,
            "Dex": 6,
            "Con": 5,
            "Int": 2,
            "Wis": 3,
            "Cha": 1
        }
        self.class_name = "Fighter"
        self.hit_die = 10
        self.saves = ["Str","Con"]
        self.equipment = ["Leather armor","Longbow","Arrow * 20","Martial weapon",
                  "Martial weapon","Handaxe * 2",
                  random.choice(["Dungeoneer's pack","Explorer's pack"])]
        self.potential_skills = [9, 1, 0, 5, 10, 15, 12, 13]
        self.skill_num = 2
        self.proficiencies = ["All armor","Shields","Simple weapons","Martial weapons"]
        self.abilities = ["Fighting Style: Archery","Second Wind"]
        self.background = "Soldier"
        self.wealth = self.getGold(5,10)
        self.doStats()

class FighterMelee(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 6,
            "Dex": 4,
            "Con": 5,
            "Int": 2,
            "Wis": 3,
            "Cha": 1
        }
        FIGHTING_STYLES = ["Defense","Dueling","Great Weapon Fighting",
                             "Protection","Two-Weapon Fighting"]
        self.class_name = "Fighter"
        self.hit_die = 10
        self.saves = ["Str","Con"]
        self.equipment = ["Chain mail","Martial weapon","Shield","Light crossbow",
                  "Bolts * 20",random.choice(["Dungeoneer's pack","Explorer's pack"])]
        self.potential_skills = [9, 1, 0, 5, 10, 15, 12, 13]
        self.skill_num = 2
        self.proficiencies = ["All armor","Shields","Simple weapons","Martial weapons"]
        self.abilities = ["Fighting Style: " + random.choice(FIGHTING_STYLES),"Second Wind"]
        self.background = "Soldier"
        self.wealth = self.getGold(5,10)
        self.doStats()

class Monk(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 3,
            "Dex": 6,
            "Con": 4,
            "Int": 2,
            "Wis": 5,
            "Cha": 1
        }
        self.class_name = "Monk"
        self.hit_die = 8
        self.saves = ["Str","Dex"]
        self.equipment = [random.choice(["Artisan's tools","Musical instrument"]),
                  random.choice(["Shortsword","Simple weapon"]),
                  random.choice(["Dungeoneer's pack","Explorer's pack"]),
                  "Darts * 10"]
        self.potential_skills = [1, 0, 5, 10, 8, 3]
        self.skill_num = 2
        self.proficiencies = ["Simple weapons","Short swords"]
        self.abilities = ["Unarmored Defense","Martial Arts"]
        self.background = "Hermit"
        self.wealth = self.getGold(5,1)
        self.doStats()

class Paladin(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 6,
            "Dex": 2,
            "Con": 4,
            "Int": 1,
            "Wis": 3,
            "Cha": 5
        }
        self.class_name = "Paladin"
        self.hit_die = 10
        self.saves = ["Wis","Cha"]
        self.equipment = ["Martial weapon",random.choice(["Martial weapon","Shield"]),
                  random.choice(["Javelin * 5","Simple melee weapon"]),
                  random.choice(["Priest's pack","Explorer's pack"]),
                  "Chain mail","Holy symbol"]
        self.potential_skills = [0, 10, 15, 11, 17, 8]
        self.skill_num = 2
        self.proficiencies = ["All armor","Shields","Simple weapons","Martial weapons"]
        self.abilities = ["Divine Sense", "Lay on Hands"]
        self.background = "Noble"
        self.wealth = self.getGold(5,10)
        self.doStats()

class Ranger(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 4,
            "Dex": 6,
            "Con": 3,
            "Int": 2,
            "Wis": 5,
            "Cha": 1
        }
        FAVORED_ENEMIES = ["Aberrations","Beasts","Celestials","Constructs",
                             "Dragons","Elementals","Fey","Fiends","Giants",
                             "Monstrosities","Oozes","Plants","Undead",
                             "Humanoids * 2"]
        FAVORED_TERRAINS = ["Arctic","Coast","Desert","Forest","Grassland",
                              "Mountain","Swamp","The Underdark","Underwater"]
        self.class_name = "Ranger"
        self.hit_die = 10
        self.saves = ["Str","Dex"]
        self.equipment = [random.choice(["Scale mail","Leather armor"]),
                  random.choice(["Shortsword * 2","Simple weapon * 2"]),
                  random.choice(["Dungeoneer's pack","Explorer's pack"]),
                  "Longbow","Arrows * 20"]
        self.potential_skills = [9, 0, 10, 6, 7, 12, 3, 13]
        self.skill_num = 3
        self.proficiencies = ["Light armor","Medium armor","Shields","Simple weapons",
                      "Martial weapons"]
        self.abilities = ["Favored Enemy: " + random.choice(FAVORED_ENEMIES),
                  "Natural Explorer",
                  "Favored Terrain: " + random.choice(FAVORED_TERRAINS)]
        self.background = "Outlander"
        self.wealth = self.getGold(5,10)
        self.doStats()

class Rogue(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 2,
            "Dex": 6,
            "Con": 3,
            "Int": 5,
            "Wis": 1,
            "Cha": 4
        }
        self.class_name = "Rogue"
        self.hit_die = 8
        self.saves = ["Int","Dex"]
        self.equipment = [random.choice(["Rapier","Shortsword"]),
                  random.choice([["Shortbow","Arrows * 20"],"Shortsword"]),
                  random.choice(["Burglar's pack","Dungeoneer's pack","Explorer's pack"]),
                  "Leather Armor","Dagger","Dagger","Thieves' tools"]
        self.potential_skills = [1, 0, 14, 10, 15, 6, 12, 16, 2, 3]
        self.skill_num = 4
        self.proficiencies = ["Light armor","Simple weapons","Hand crossbows",
                      "Longswords","Rapier","Shortswords"]
        self.abilities = ["Expertise", "Sneak Attack", "Thieves' Cant"]
        self.background = "Charlatan"
        self.wealth = self.getGold(4,10)
        self.doStats()

class Sorcerer(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 1,
            "Dex": 2,
            "Con": 5,
            "Int": 4,
            "Wis": 3,
            "Cha": 6
        }
        self.class_name = "Sorcerer"
        self.hit_die = 6
        self.saves = ["Con","Cha"]
        self.equipment = [random.choice([["Light crossbow, Bolts * 20"],"Simple weapon"]),
                  random.choice(["Component pouch","Arcane focus"]),
                  random.choice(["Dungeoneer's Pack","Explorer's pack"]),"Dagger * 2"]
        self.potential_skills = [4, 14, 10, 15, 17, 8]
        self.skill_num = 2
        self.proficiencies = ["Daggers","Darts","Slings",
                     "Quarterstaffs","Light crossbows"]
        self.abilities = ["Cantrips * 3", "Spells * 2",
                 "Sorcerous Origin: " + random.choice(["Draconic Bloodline","Wild Magic"])]
        self.background = "Hermit"
        self.wealth = self.getGold(3,10)
        self.doStats()

class Warlock(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 1,
            "Dex": 2,
            "Con": 3,
            "Int": 4,
            "Wis": 5,
            "Cha": 6
        }
        self.class_name = "Warlock"
        self.hit_die = 6
        self.saves = ["Wis","Cha"]
        self.equipment = [random.choice([["Light crossbow","Bolts * 20"],"Simple weapon"]),
                  random.choice(["Component pouch","Arcane focus"]),
                  random.choice(["Scholar's pack","Dungeoneer's pack"]),
                  "Leather armor","Simple weapon","Dagger * 2"]
        self.potential_skills = [4, 14, 5, 15, 6, 7, 8]
        self.skill_num = 2
        self.proficiencies = ["Light armor", "Simple weapons"]
        self.abilities = ["Cantrips * 2", "Spells * 2",
                  "Otherworldly Patron", "Pact Magic"]
        self.background = "Charlatan"
        self.wealth = self.getGold(4,10)
        self.doStats()

class Wizard(Character):
    def __init__(self):
        super().__init__()
        self.stat_weights = {
            "Str": 1,
            "Dex": 2,
            "Con": 4,
            "Int": 6,
            "Wis": 5,
            "Cha": 3
        }
        self.class_name = "Wizard"
        self.hit_die = 6
        self.saves = ["Int","Wis"]
        self.equipment = [random.choice(["Quarterstaff","Dagger"]),
                  random.choice(["Component pouch","Arcane focus"]),
                  random.choice(["Scholar's pack","Explorer's pack"]),
                  "Spellbook"]
        self.potential_skills = [4, 5, 10, 6, 11, 8]
        self.skill_num = 2
        self.proficiencies = ["Daggers","Darts","Slings",
                     "Quarterstaffs","Light crossbows"]
        self.abilities = ["Cantrips * 3", "Spells * 6"]
        self.background = "Sage"
        self.wealth = self.getGold(4,10)
        self.doStats()

def get_character():
    CLASSES = [Barbarian, Bard, Cleric, Druid, FighterArch,FighterMelee,
               Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard]
    cls = random.choice(CLASSES)
    chr = cls()
    return chr

if __name__ == "__main__":
    chr = get_character()
    print(chr.toString())
