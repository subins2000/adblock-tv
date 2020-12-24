# Adblock TV

An AdBlocker (Ad-Muter) for TV. When ads appear in between programs, the TV audio will be muted and when program comes back on, TV is unmuted. Completely offline and runs on a Raspberry Pi.

[Video Demo](https://devfolio.co/submissions/adblock-tv-adbtv)

## Setup

### Hardware

* Raspberry Pi
* [Infrared Emitter](https://robu.in/product/grove-infrared-emitter/)
* [USB Sound Card](https://robu.in/product/usb-to-3-5mm-mic-and-headphone-jack-stereo-headset-audio-adapter-usb-sound-card-7-1-hot/) since Raspberry Pi doesn't support audio input
* Your set-top-box (STB) probably support AV output, then connect a [3.5mm-RCA-Female cable](https://www.amazon.in/Twisted-3-5mm-Female-Audio-Video/dp/B00NSP2E7G) to it and then connect a [AUX-Male-3.5mm cable](https://www.alibaba.com/product-detail/3-5-mm-to-2-RCA_477152309.html) to the USB sound card
* Test if audio from STB reaches Raspberry Pi by using `pavucontrol` or Audacity or other voice recording softwares

### Software

* Clone into your Raspberry Pi
* `pipenv install`
* Setup postgres database, copy `.env.example` to `.env` and edit config

#### Setup Infrared

* Follow tutorial https://devkimchi.com/2020/08/12/turning-raspberry-pi-into-remote-controller/
  * Connect infrared emitter. Connect the TX pin to `GPIO17`
  * Setup lirc
  * Reverse image search photo of remote
  * Get remote config file from [remotes database](http://lirc-remotes.sourceforge.net/remotes-table.html). Example: https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/samsung/AA59-00382A.lircd.conf
  * Test lirc with
    ```
    irsend LIST Samsung_AA59-00382A ""
    irsend SEND_ONCE Samsung_AA59-00382A KEY_POWER
    ```
  * Edit remote config values in `.env`
  * Test by running `ir-test.py`

## Running

* Run the adblocker by running `adbtv.py`
* ADBTV web interface runs on port 8100

Scripts :

* `record-ad.py` - For recording ads
* `scan.py` - Scan for ads, no blocking
* `scan-block.py` - Scan for ads, and block (mute) them, but no unmute
* `scan-block-unblock.py` - Scan, block ads and unblock when no ad is detected
* `adbtv.py` - Run the web interface and blocker. The main script

### Tips

* Keep the audio level coming into rasppi to a standard, peak should reach -3dB only. Use `pavucontrol` for this
* From experience, audio recognition has correlation with the volume of the audio

### TODO

* [ ] Instead of mute, decrease/increase volume. Helps much in false positives
* [ ] Improve audio recognition. Volume has a significant effect on detection
