from dejavu import Dejavu
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
import os
import sys


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


class ADBTV:

    def __init__(self, dejavu_config, folder, extensions):
        self.djv = Dejavu(dejavu_config)
        self.djv.fingerprint_directory(folder, extensions, 3)

    @blockPrinting
    def djv_record(self):
        return self.djv.recognize(MicrophoneRecognizer, seconds=3)

    def record(self, confidence=0.05):
        results = self.djv_record()

        for r in results[0]:
            sn = str(r['song_name'])
            inco = r['input_confidence']
            fco = r['fingerprinted_confidence']

            print()
            print(r)

            # Value will be grater than 100 if there's some sound
            # A hack to detect volume level
            if r['input_total_hashes'] > 200:
                if inco > confidence:
                    return r
            else:
                return None

        return False
