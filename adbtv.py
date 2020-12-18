from config import *
import eel
from libadbtv import *
from lirc import Client
import os

lirc = Client()

state = {
    "active": True
}

@eel.expose
def setState(newState):
    state.update(newState)
    print(state)
    eel.updateState(state)


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
    eel.init(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'web', 'public'))
    eel.start('index.html', mode=False, host="0.0.0.0", port=8100, block=False)

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