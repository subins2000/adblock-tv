from config import *
from dejavu import Dejavu
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
from lirc import Lirc
import os
import sys

lirc = Lirc()

muted = False


def mute():
    global muted
    if not muted:
        lirc.send_once(REMOTE_KEY_MUTE, REMOTE_NAME)
        muted = True


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


djv = Dejavu(dejavu_config)
djv.fingerprint_directory("ads/", [".mp3", ".wav"], 3)


@blockPrinting
def record():
    return djv.recognize(MicrophoneRecognizer, seconds=2)


def main():
    while True:
        results = record()

        for r in results[0]:
            sn = str(r['song_name'])
            inco = r['input_confidence']
            fco = r['fingerprinted_confidence']

            # Value will be grater than 100 if there's some sound
            # A hack to detect volume level
            if r['input_total_hashes'] > 100:
                muted = False

            # print(r)
            if inco > 0.05:
                print("ad - " + sn)
                mute()


if __name__ == "__main__":
    main()
