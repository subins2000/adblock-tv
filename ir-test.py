from config import *
from lirc import Lirc

lirc = Lirc()
lirc.send_once(REMOTE_KEY_MUTE, REMOTE_NAME)
