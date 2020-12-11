# Adblock TV

## Setup Infrared

* Follow tutorial https://devkimchi.com/2020/08/12/turning-raspberry-pi-into-remote-controller/
  * Setup lirc
  * Reverse image search photo of remote
  * Get remote config file. Example: https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/samsung/AA59-00382A.lircd.conf
  * Test lirc with
    ```
    irsend LIST Samsung_AA59-00382A ""
    irsend SEND_ONCE Samsung_AA59-00382A KEY_POWER
    ```
