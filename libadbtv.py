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


class NoSound(BaseException):
    pass


class ADBTV:
    debug = False

    def __init__(self, dejavu_config, folder, extensions, debug=False):
        self.djv = Dejavu(dejavu_config)
        self.djv.fingerprint_directory(folder, extensions, 3)
        self.debug = debug

    @blockPrinting
    def djv_record(self, seconds):
        return self.djv.recognize(MicrophoneRecognizer, seconds=seconds)

    def record(self, seconds=4, confidence=0.10, min_confidence=0.03):
        results = self.djv_record(seconds)

        for r in results[0]:
            sn = str(r['song_name'])
            inco = r['input_confidence']
            fco = r['fingerprinted_confidence']

            if self.debug:
                print()
                print(results)

            # Value will be grater than 200 if there's some sound
            # A hack to detect volume level
            if r['input_total_hashes'] > 200:
                if (fco > 0.00 and inco >= min_confidence) or inco > confidence:
                    return r
            else:
                raise NoSound

        if inco <= min_confidence:
            if self.debug:
                print()
                print("ad-over")
            return False
