import os
import json
import env_file
from wit import Wit

"""
Running command:
python build_buckets.py
"""


"""
Load environment variables
"""
env = env_file.load(".env")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
JSON_FILE = os.environ.get("JSON_FILE")
QUOTE_FILE = os.environ.get("QUOTE_FILE")


"""
Decode intent numbers
"""
decode = {
    "intent_0": "none",
    "intent_1": "anger",
    "intent_2": "disgust",
    "intent_3": "fear",
    "intent_4": "happiness",
    "intent_5": "sadness",
    "intent_6": "surprise",
}


"""
Connect to WitAI client
"""
client = Wit(AUTH_TOKEN)


def get_JSON():
    """
    Load the quotes from the JSON file
    :return:    Quotes JSON data file
    """
    with open(str(os.getcwd()) + "/" + JSON_FILE) as f:
        data = json.load(f)
        return data


def get_intent(sentence, limit):
    """
    Use Wit AI to get a pretrained intent for a sentence
    :param sentence:    Sentence for which the intent is to be found
    :param limit:       Number of intents
    :return:            Intent object
    """
    res = client.message(sentence, n=8)
    intents = res["intents"]
    intents = sorted(intents, key=lambda x: x["confidence"], reverse=True)[:limit]
    return intents


def store_intents(data):
    """
    Write intents into different JSON files
    :param data:        Intent object
    :return:            None
    """
    mainObj = data["quotes"]
    for obj in mainObj:
        intent = get_intent(obj["quote"], 1)
        write_JSON(intent[0]["name"], obj)


def write_JSON(filename, obj):
    """
    Write JSON file from the JSON object passed
    :param filename:    Name of the file - also the intent
    :param obj:         JSON object to be written
    :return:            None
    """
    with open(
        str(os.getcwd()) + "/data/" + QUOTE_FILE + "/" + decode[filename] + ".json",
        "a+",
    ) as f:
        obj["intent"] = decode[filename]
        json.dump(obj, f, ensure_ascii=False, indent=4)


# ----- Main execution
if __name__ == "__main__":
    data = get_JSON()
    store_intents(data)
