from config import *
from lirc import Client

lirc = Client()
lirc.send(REMOTE_NAME, REMOTE_KEY_MUTE)
