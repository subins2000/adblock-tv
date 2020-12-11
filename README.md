# Adblock TV

## Setup

### Hardware

* Raspberry Pi
* [Infrared Emitter](https://robu.in/product/grove-infrared-emitter/)
* [USB Sound Card](https://robu.in/product/usb-to-3-5mm-mic-and-headphone-jack-stereo-headset-audio-adapter-usb-sound-card-7-1-hot/) since Raspberry Pi doesn't support audio input

### Software

* Clone
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

* Record ads by running `record-ad.py`
* Run the adblocker by running `main.py`