from config import *
from libadbtv import *
from lirc import Lirc
import os
import sys

lirc = Lirc()

mute_requested = False
muted = False


def mute():
    global mute_requested, muted
    if not muted:
        lirc.send_once(REMOTE_KEY_MUTE, REMOTE_NAME)
        mute_requested = True


def main():
    global mute_requested, muted

    adbtv = ADBTV(dejavu_config, "ads/", [".mp3", ".wav"])

    while True:
        result = adbtv.record(0.05)

        if result is None:
            # Not enough volue i.e muted
            if mute_requested:
                muted = True
                mute_requested = False

        else:
            if mute_requested:
                mute()
            else:
                muted = False

            if result is not False:
                sn = str(result['song_name'])
                inco = result['input_confidence']
                fco = result['fingerprinted_confidence']

                print("ad - " + sn)
                mute()


if __name__ == "__main__":
    main()
