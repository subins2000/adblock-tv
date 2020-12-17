import eel


eel.init('web/public')
eel.start('index.html', mode=False, host="0.0.0.0", port=8100)
