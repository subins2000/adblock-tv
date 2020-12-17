from config import *
from libadbtv import *


def main():
    global mute_requested, muted

    adbtv = ADBTV(dejavu_config, "ads/", [".mp3", ".wav"])

    while True:
        result = adbtv.record()

        if result is not False and result is not None:
            sn = str(result['song_name'])
            inco = result['input_confidence']
            fco = result['fingerprinted_confidence']

            print("ad - " + sn)


if __name__ == "__main__":
    main()
