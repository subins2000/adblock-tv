from array import array
import os
import pyaudio
from pydub import AudioSegment
import wave

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

frames = []

try:
    while True:
        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)

        if vol >= MIN_VOLUME:
            frames.append(data)
except KeyboardInterrupt:
    print("* done recording")

    WAVE_OUTPUT_FILEPATH = "ads/" + input("Ad name: ")

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
