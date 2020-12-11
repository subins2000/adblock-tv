from config import *
from dejavu import Dejavu


djv = Dejavu(dejavu_config)
for item in djv.get_fingerprinted_songs():
    print(item[0], " - ", item[1])

print()
try:
    did = input("Enter ids to delete separated by ',' (comma): ")
    djv.delete_songs_by_id(did.split(','))
except KeyboardInterrupt:
    print()
    pass
