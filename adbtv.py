import eel
import os

state = {
    "active": True
}

@eel.expose
def setState(newState):
    state.update(newState)
    print(state)
    eel.updateState(state)

eel.init(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'web', 'public'))
eel.start('index.html', mode=False, host="0.0.0.0", port=8100)
