import pickle
import random
import logging
from nltk.corpus import stopwords

class DialogueParser:
    """
    A class to be used to read and wrangle the dialogue data
    """
    def __init__(self, fname, delimeter="__eou__", lower=True, stop_rem=True):
        """
        :param fname:       File name to be read in
        :param delimeter:   Token that delimets dialogues
        :param lower:       Boolean specifying conversion to lowercase
        :param stop_rem:    Boolean specifying stopword removal
        """
        self.fname = fname
        self.delimeter = delimeter
        self.lower = lower
        self.stop_rem = stop_rem
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger("dialogue_parser")
        self.logger.setLevel(logging.DEBUG)
        self.data = []

    def read_file(self):
        """Read the file provided"""
        self.logger.debug("Reading file")
        ctr = 0
        with open(self.fname) as f:
            content = f.read()
        dialogue = []
        for word in content.split():
            if word == self.delimeter:
                self.data += [self.pre_process(" ".join(dialogue))]
                dialogue = []
                ctr += 1
                print(ctr)
            else:
                dialogue += [word]
        self.logger.debug("Reading complete")

    def pre_process(self, dialogue):
        """
        Preprocess based on settings
        :param dialogue:    The dialogue to be preprocessed
        :return:            Preprocessed dialogue
        """
        ret = []
        for word in dialogue.split():
            if self.lower or self.stop_rem:
                if self.lower:
                    word = word.lower()
                if self.stop_rem and word not in stopwords.words('english'):
                    ret += [word]
            else:
                ret += [word]
        return " ".join(ret)


    def dump_data(self, pickle_file):
        """
        Dump data to a pickle file
        :param pickle_file:     Dump destination
        """
        if not self.data:
            self.logger.error("Nothing to dump, read file first")
            return
        pickle.dump(self.data, open(pickle_file, "wb"))

    def load_data(self, pickle_file):
        """
        Load data from pickle file
        :param pickle_file:     Load destination
        :return:                Loaded data
        """
        return pickle.load(open(pickle_file, "rb"))

    @staticmethod
    def print_list(content):
        for element in content:
            print(element)

    def display_data(self, limit=50):
        """
        Show any 50 instances
        :param limit:   Limit to how many instances to display
        """
        random.shuffle(self.data)
        DialogueParser.print_list(self.data[:limit])
