#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import json
import subprocess
from signal import signal, SIGTERM, SIGUSR1, SIGUSR2, SIGTSTP, SIGCONT, SIGIO, SIGRTMIN

def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    
    def handle_signal(signum, frame):
        print('signal')
        line = read_line()
        if line.startswith('['):
            line = ''
        else:
            if line.startswith(','):
                line = line[1:]
            event = json.loads(line)
            event['name'] = 'click'
            event['full_textl'] = 'click'
            sys.stdout.write(',[{}]\n'.format(json.dumps(event)))

    signal(SIGTSTP, handle_signal)
    signal(SIGCONT, handle_signal)
    signal(SIGIO, handle_signal)
    signal(SIGUSR1, handle_signal)
    signal(SIGUSR2, handle_signal)
    signal(SIGRTMIN, handle_signal)

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
        sys.stdout.flush()
