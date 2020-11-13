from dejavu import Dejavu
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
import os
import sys

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "username",
        "password": "password",
        "database": "adtv",
    },
    "database_type": "postgres"
}


# decorater used to block function printing to the console
def blockPrinting(func):
    def func_wrapper(*args, **kwargs):
        # block all printing to the console
        sys.stdout = open(os.devnull, 'w')
        # call the method in question
        value = func(*args, **kwargs)
        # enable all printing to the console
        sys.stdout = sys.__stdout__
        # pass the return value of the method back
        return value

    return func_wrapper


djv = Dejavu(config)
djv.fingerprint_directory("ads/", [".mp3", ".wav"], 3)


@blockPrinting
def record():
    return djv.recognize(MicrophoneRecognizer, seconds=2)


while True:
    results = record()

    for r in results[0]:
        sn = str(r['song_name'])
        inco = r['input_confidence']
        fco = r['fingerprinted_confidence']

        # print(r)
        if inco > 0.05:
            print("ad - " + sn)
