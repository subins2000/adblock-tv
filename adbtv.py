from array import array
from config import *
import eel
from libadbtv import *
from lirc import Client
import os
import glob
import pyaudio
from pydub import AudioSegment
import wave

lirc = Client()
lastRecordFrames = []
startRecording = False
stopRecording = False
pyAd = None
stream = None

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MIN_VOLUME = 300

state = {
    "active": True,
    "blocks": [],
    "adlist": [],
    "duration": 2,
    "confidence": 0.15
}

@eel.expose
def setState(newState):
    state.update(newState)
    print(state)
    eel.updateState(state)


@eel.expose
def getState():
    eel.updateState(state)


@eel.expose
def updateSettings(settings):
    state["duration"] = settings["duration"]
    state["confidence"] = settings["confidence"]
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
    global lastRecordFrames, stream, pyAd, stopRecording

    pyAd = pyaudio.PyAudio()

    stream = pyAd.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    while True:
        if stopRecording:
            break

        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)

        if vol >= MIN_VOLUME:
            lastRecordFrames.append(data)
        
        eel.sleep(0.0001)
    
    print("* done recording")


@eel.expose
def recordFinish(adName):
    global lastRecordFrames, stream, pyAd
    WAVE_OUTPUT_FILEPATH = "ads/" + adName

    stream.stop_stream()
    stream.close()
    pyAd.terminate()

    wf = wave.open(WAVE_OUTPUT_FILEPATH + ".wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyAd.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(lastRecordFrames))
    wf.close()

    print("Converting to MP3...")

    sound = AudioSegment.from_wav(WAVE_OUTPUT_FILEPATH + ".wav")
    sound.export(WAVE_OUTPUT_FILEPATH + ".mp3", format='mp3')

    os.remove(WAVE_OUTPUT_FILEPATH + ".wav")

    stream = None
    print("Done")


@eel.expose
def recordStart():
    global startRecording, stopRecording
    startRecording = True
    stopRecording = False
    eel.spawn(record)


@eel.expose
def recordStop():
    global startRecording, stopRecording
    stopRecording = True
    startRecording = False


def scan():
    global state

    eel.sleep(1.0)
    adbtv = ADBTV(dejavu_config, "ads/", [".mp3", ".wav"], True)

    state["adlist"] = os.listdir("ads/")
    eel.updateState(state)

    while True:
        if not state["active"] or startRecording is True:
            eel.sleep(1.0)
            continue

        try:
            result = adbtv.record(state['duration'], state['confidence'])

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

    def callback(page, sockets):
        pass

    eel.spawn(scan)
    eel.start('index.html', mode=False, host="0.0.0.0", port=8100, close_callback=callback)


if __name__ == "__main__":
    main()
