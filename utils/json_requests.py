import sys
import logging
import json
import requests
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv


"""
Running command:
python json_requests.py **path to dialogues_ems.json/empty string **  **intents to post separated by spaces/empty string***
"""


def post_intent(intents: str, url: str, auth_token: str) -> None:
    """
    :param intents: A list of all intents to be added to the app
    :return:
    """
    logger.debug(f"****** Add intents to wit app ********")

    header = {
        "Authorization": "Bearer " + auth_token,
        "content-type": "application/json",
    }

    for i, intent in enumerate(intents):
        data = {"name": intent}
        response = requests.post(url, json=data, headers=header)
        logger.debug(f"Response for intent {i} : {response.json()}")


def post_utterrances(file, url, auth_token):
    """
    :param json_file: File name from folder data to post utterances for training
    :return:
    """
    logger.debug(f"******** Training for the utterrances *********")

    payload = []
    header = {
        "Authorization": "Bearer " + auth_token,
        "content-type": "application/json",
    }

    with open(file) as json_file:
        data = json.load(json_file)
        for d in data:
            if 1 < len(d["utterance"]) <= 280:
                temp_dict = {}
                temp_dict["text"] = d["utterance"]
                temp_dict["intent"] = "intent_" + d["emotion"]
                temp_dict["entities"] = []
                temp_dict["traits"] = []
                payload.append(temp_dict)

    for i in range(0, len(payload), 200):
        response = requests.post(url, json=payload[i : i + 200], headers=header)
        logger.debug(f"Response for training:\n {response.json()}")
        time.sleep(70)

    logger.debug(f"********* Training complete **********")


if __name__ == "__main__":

    # Setup for reading from .env file
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    # Environment variables
    auth_token = os.environ.get("AUTH_TOKEN")
    intents_url = os.environ.get("INTENTS_URL")
    utterance_url = os.environ.get("UTT_URL")

    # Logging setup
    logging.basicConfig(format="%(asctime)s %(message)s")
    logger = logging.getLogger("dialogue_parser")
    logger.setLevel(logging.DEBUG)

    # Read from stdin
    json_file, intents = sys.argv[1], sys.argv[2:]

    if intents:
        post_intent(intents, intents_url, auth_token)

    if json_file:
        post_utterrances(json_file, utterance_url, auth_token)
