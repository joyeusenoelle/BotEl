from random import choice

class BotElMarkov():
    """ Creates Markov-chain paragraphs out of corpus texts.
    """
    def __init__(self):
        self.EOS = ['.', '?', '!']
        self.leodict = self.gtext("leo.txt")
        self.kaidict = self.gtext("kai.txt")
        self.arctrekdict = self.gtext("arctrek.txt")
        self.dicts = {"leo":self.leodict,"kai":self.kaidict,"arctrek":self.arctrekdict}

    def buildDict(self, words):
        """
        Build a dictionary from the words.
 
        (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
        """
        dictionary = {}
        for i, word in enumerate(words):
            try:
                first, second, third, fourth = words[i], words[i+1], words[i+2], words[i+3]
            except IndexError:
                break
            key = (first, second, third)
            if key not in dictionary:
                dictionary[key] = []
            dictionary[key].append(fourth)
        return dictionary

    def gtext(self, fname):
        """ Gets text from a local file, passes it to build_dict().
        """
        with open(fname, "rt", encoding="utf-8") as f:
            text = f.read()
        words = text.split()
        d = self.buildDict(words)
        #pprint(d)
        return d

    def generateSentence(self, dictionary):
        """ Creates a sentence out of the word chunks in the input dictionary.
        """
        init_words = [key for key in dictionary.keys() if key[0][0].isupper()]
        current_words = choice(init_words)
        word_list = []
        first, second, third = current_words
        word_list.append(first)
        word_list.append(second)
        word_list.append(third)
        while True:
            try:
                fourth = choice(dictionary[current_words])
            except KeyError:
                break
            word_list.append(fourth)
            if len(' '.join(word_list)) > 500:
                if (fourth[-1] in self.EOS) or (fourth[-1] == '"' and fourth[-2] in self.EOS):
                    break
            current_words = (second, third, fourth)
            first, second, third = current_words
        
        return ' '.join(word_list)
        
    def getChain(self, corpus, requester, leader=None):
        """ Exposes the chaining mechanism to BotEl.
        """
        if leader == None: leader = "" 
        print("{} requested a markov chain for {}.".format(requester, corpus))
        if corpus in self.dicts.keys():
            output = "quote "
            output += self.generateSentence(self.dicts[corpus])
        else:
            output = "{}'{} Sorry, {} isn't one of the texts I know.".format(leader, requester, corpus)
        return output