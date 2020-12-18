from array import array
from config import *
import eel
from libadbtv import *
from lirc import Client
import os
from pathlib import Path
import pyaudio
from pydub import AudioSegment
import wave

lirc = Client()
lastRecordFrames = []
startRecording = False
stopRecording = False

state = {
    "active": True,
    "blocks": [],
    "adlist": []
}

@eel.expose
def setState(newState):
    state.update(newState)
    print(state)
    eel.updateState(state)


muted = False


def mute():
    global muted
    if not muted and startRecording is False:
        lirc.send(REMOTE_NAME, REMOTE_KEY_MUTE)


def unmute():
    global muted
    if muted:
        lirc.send(REMOTE_NAME, REMOTE_KEY_MUTE)
        muted = False


def record():
    global lastRecordFrames

    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    MIN_VOLUME = 300

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    while True:
        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)

        if vol >= MIN_VOLUME:
            lastRecordFrames.append(data)

        if stopRecording:
            break
    
    print("* done recording")


@eel.expose
def recordFinish(adName):
    WAVE_OUTPUT_FILEPATH = "ads/" + adName

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILEPATH + ".wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Converting to MP3...")

    sound = AudioSegment.from_wav(WAVE_OUTPUT_FILEPATH + ".wav")
    sound.export(WAVE_OUTPUT_FILEPATH + ".mp3", format='mp3')

    os.remove(WAVE_OUTPUT_FILEPATH + ".wav")

    print("Done")


@eel.expose
def recordStart():
    startRecording = True
    eel.spawn(record)


@eel.expose
def recordStop():
    stopRecording = True


def scan():
    eel.sleep(1.0)
    adbtv = ADBTV(dejavu_config, "ads/", [".mp3", ".wav"], True)

    state["adlist"] = list(Path("ads/").rglob("*"))

    while True:
        if startRecording is True:
            continue

        if not state["active"]:
            eel.sleep(1.0)
            continue

        try:
            result = adbtv.record(2, 0.15)

            if type(result) is tuple:
                sn = str(result['song_name'])
                inco = result['input_confidence']
                fco = result['fingerprinted_confidence']

                print("ad - " + sn)
                state.blocks.append("Detected ad '", sn, "'. Confidence - ", inco)

                eel.updateState(state)

                mute()
            else:
                unmute()
        except NoSound:
            pass

        eel.sleep(0.01)


def main():
    eel.init(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'web', 'public'))

    eel.spawn(scan)
    eel.start('index.html', mode=False, host="0.0.0.0", port=8100)


if __name__ == "__main__":
    main()
