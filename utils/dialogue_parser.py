import re
import sys
import json
import random
import logging
from nltk.corpus import stopwords

"""
Running command:
python dialogue_parser.py **path to dialogues_text.txt** ** path to dialogues_emotion.txt** ../data/dialogue_ems.json
"""


def read_dialogues(fname, delimeter):
    """
    Read the dialogue file provided
    :param fname:       The file name to be read
    :param delimeter:   The token demarcating dialogues
    :return:            pre-processed dialogues
    """
    with open(fname) as f:
        content = f.readlines()
    logger.debug(f"Reading dialogue file: {fname}")
    ctr = 0
    dialogue = []
    data = []
    for line in content:
        for word in line.split():
            if word == delimeter:
                data += [" ".join(dialogue)]
                dialogue = []
                ctr += 1
            else:
                dialogue += [word]
    logger.debug(f"Successfully read {ctr} utterances.")
    return data


def pre_process(dialogue, lower=False, stop_rem=False):
    """
    Preprocess based on settings
    :param dialogue:    The dialogue to be preprocessed
    :return:            Preprocessed dialogue
    """
    ret = []
    for word in dialogue.split():
        if lower or stop_rem:
            if lower:
                word = word.lower()
            if stop_rem and word not in stopwords.words("english"):
                ret += [word]
        else:
            ret += [word]
    return " ".join(ret)


def read_emotions(fname):
    """
    Read the emotion file provided
    :param fname:       The file name to be read
    :return:            list of emotions
    """
    with open(fname) as f:
        content = f.readlines()
    logger.debug(f"Reading emotions file: {fname}")
    ctr = 0
    emotions = []
    for line in content:
        ems = line.strip().split()
        for emotion in ems:
            emotions += [emotion]
            ctr += 1
    logger.debug(f"Successfully read {ctr} emotions.")
    return emotions


# ----- I/O utils
def print_list(content):
    """Pretty print a list"""
    for element in content:
        print(element)


def display_data(data, limit=50):
    """
    Show any 50 instances
    :param limit:   Limit to how many instances to display
    """
    random.shuffle(data)
    print_list(data[:limit])


def unite_data(data, emotions, suppress_noemo=True, no_emo_limit=300):
    """
    Map emotions to utterances
    :param data:            List of utterances
    :param emotions:        List of emotions
    :param filter_noemo:    Filter out no emotions
    """
    logger.debug(f"Mapping emotions to utterances, Filtering: {suppress_noemo}")
    united_data = []
    no_emo_ctr = 0
    for i in range(len(data)):
        utt = data[i]
        # Remove weird right quotation marks
        utt = re.sub("(\u2018|\u2019)", "'", utt)
        if suppress_noemo:
            if emotions[i] != NO_EMOTION:
                united_data += [(utt, emotions[i])]
            else:
                if no_emo_ctr < no_emo_limit:
                    united_data += [(utt, emotions[i])]
                    no_emo_ctr += 1
        else:
            united_data += [(utt, emotions[i])]
    logger.debug(f"Mapping complete. Total instances: {len(united_data)}")
    return united_data


def dump2json(data, json_file):
    logger.debug(f"Dumpting to json file: {json_file}")
    dump_data = []
    for element in data:
        dump_data += [{"utterance": element[0], "emotion": element[1]}]
    with open(json_file, "w") as fout:
        json.dump(dump_data, fout, indent=2)
    logger.debug("Dumping complete")


# ----- Main execution
if __name__ == "__main__":
    # Constants
    NO_EMOTION = "0"

    # Logging setup
    logging.basicConfig(format="%(asctime)s %(message)s")
    logger = logging.getLogger("dialogue_parser")
    logger.setLevel(logging.DEBUG)

    dialogue_fname, emotion_fname, json_out = sys.argv[1], sys.argv[2], sys.argv[3]
    delimeter = "__eou__"
    data = read_dialogues(dialogue_fname, delimeter)
    emotions = read_emotions(emotion_fname)
    # Sanity check
    assert len(data) == len(emotions)

    united_data = unite_data(data, emotions)
    dump2json(united_data, json_out)
