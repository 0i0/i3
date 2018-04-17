import sys
import signal
import time
import json

class SIGIOHandler:
    def __init__(self):
        self.handlers = []
        self.on()
    
    def on(self):
        signal.signal(signal.SIGIO, self)

    def off(self):
        signal.signal(signal.SIGIO, signal.SIG_DFL)

    def register(self, callback):
        self.handlers.append(callback)
        return len(self.handlers) - 1 # the handle

    def unregister(self, handle=0):
        if self.handlers:
            del self.handlers[handle]

    def __call__(self, sig, frame):
        for h in self.handlers:
            h(frame)

def printevent():
    print('click')

if __name__ == '__main__':
    click = SIGIOHandler()
    click.register(printevent)

    click.on()

    header = {
        'version': 1,
        'click_events': True
    }

    sys.stdout.write(json.dumps(header))

    # begining of an infinite array.
    sys.stdout.write('\n[[]\n')

    # ibar 3 object
    j = [
        {
            "full_text": "full test",
            # "short_text": "test",
            # "color": "#00ff00",
            # "background": "#1c1c1c",
            # "border": "#ee0000",
            # "min_width": 300,
            # "align": "right",
            # "urgent": False,
            "name": "test",
            # "instance": "eth1",
            # "separator": True,
            # "separator_block_width": 90,
            "button":1
        }
    ]
    sys.stdout.write(',{}\n'.format(json.dumps(j)))
    sys.stdout.flush()
    while True:
        time.sleep(3)
        sys.stdout.write(',{}\n'.format(json.dumps(j)))
        sys.stdout.flush()3
