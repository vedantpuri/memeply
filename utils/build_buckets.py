import os
import json
import env_file
from wit import Wit

env = env_file.load('.env')
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
JSON_FILE = os.environ.get("JSON_FILE")
QUOTE_FILE = os.environ.get("QUOTE_FILE")
client = Wit(AUTH_TOKEN)
decode = {"intent_0": "none", "intent_1": "anger", "intent_2": "disgust", "intent_3": "fear", "intent_4": "happiness", "intent_5": "sadness", "intent_6": "surprise"}

def getJSON():
	with open(str(os.getcwd())+"/"+JSON_FILE) as f:
		data = json.load(f)
		return data

def getIntent(sentence, limit):
    res = client.message(sentence, n=8)
    intents = res["intents"]
    intents = sorted(intents, key = lambda x : x["confidence"], reverse=True)[:limit]
    return intents

def storeIntents(data):
	mainObj = data["quotes"]
	for obj in mainObj:
		intent = getIntent(obj["quote"], 1)
		writeJSON(intent[0]["name"], obj)
		

def writeJSON(filename, obj):
	with open(str(os.getcwd()) + "data/" + QUOTE_FILE + "/" + decode[filename] + ".json", "a+") as f:
		obj["intent"] = decode[filename]
		json.dump(obj, f, ensure_ascii=False, indent=4)

data = getJSON()
storeIntents(data)
