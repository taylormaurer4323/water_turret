from pynput.keyboard import Key, Listener


def read_input(key):

with Listener(on_press = show) as listener:
    listener.join()
