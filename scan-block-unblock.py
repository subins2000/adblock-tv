from config import *
from libadbtv import *
from lirc import Client
import os
import sys

lirc = Client()

muted = False


def mute():
    global muted
    if not muted:
        lirc.send(REMOTE_NAME, REMOTE_KEY_MUTE)


def unmute():
    global muted
    if muted:
        lirc.send(REMOTE_NAME, REMOTE_KEY_MUTE)
        muted = False


def main():
    adbtv = ADBTV(dejavu_config, "ads/", [".mp3", ".wav"], True)

    while True:
        try:
            result = adbtv.record(2, 0.15)

            if result is not False:
                sn = str(result['song_name'])
                inco = result['input_confidence']
                fco = result['fingerprinted_confidence']

                print("ad - " + sn)
                mute()
            else:
                unmute()
        except:
            pass


if __name__ == "__main__":
    main()
