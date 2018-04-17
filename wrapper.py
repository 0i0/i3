#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a simple wrapper which prefixes each i3status line with custom
# information. It is a python reimplementation of:
# http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.pl
#
# To use it, ensure your ~/.i3status.conf contains this line:
#     output_format = "i3bar"
# in the 'general' section.
# Then, in your ~/.i3/config, use:
#     status_command i3status | ~/i3status/contrib/wrapper.py
# In the 'bar' section.
#
# In its current version it will display the cpu frequency governor, but you
# are free to change it to display whatever you like, see the comment in the
# source code below.
#
# © 2012 Valentin Haenel <valentin.haenel@gmx.de>
# © 2015 Thom Wiggers <thom@thomwiggers.nl>
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You can redistribute it and/or modify it under
# the terms of the Do What The Fuck You Want To Public License (WTFPL), Version
# 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more
# details.

import sys
import json
import subprocess
from signal import signal, SIGTERM, SIGUSR1, SIGTSTP, SIGCONT, SIGIO

def get_gpu_text():
    util = subprocess.Popen(['nvidia-settings', '-t','-q','[gpu:0]/GPUUtilization'], stdout=subprocess.PIPE).communicate()[0]
    temp = subprocess.Popen(['nvidia-settings', '-t','-q','[gpu:0]/GPUCoreTemp'], stdout=subprocess.PIPE).communicate()[0]
    util = util.strip().split(',')[0].split('=')[1]
    return '<span color="#BBBBBB">GPU:</span>{util:02d}% {temp:02d}°'.format(util=int(util),temp=int(temp.strip()))

def get_cpu_text():
    temp = subprocess.Popen(['sensors'], stdout=subprocess.PIPE).communicate()[0]
    temparr = temp.split('\n')
    temparr =temparr[3:7]
    return '<span color="#BBBBBB">CPU:</span> {}° {}° {}° {}°'.format(temparr[0].split()[2][1:3],temparr[1].split()[2][1:3],temparr[2].split()[2][1:3],temparr[3].split()[2][1:3])

def get_networkspeed():
    return subprocess.Popen(['/home/lior/.config/i3/measure-netspeed.bash'], stdout=subprocess.PIPE).communicate()[0]

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


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

def handle_signal(self, signum, frame):
    # print_line(read_line())
    print('test')

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    # signal(SIGTSTP, self.i3bar_stop)
    # # SIGCONT indicates output should be resumed.
    # signal(SIGCONT, self.i3bar_start)
    signal(SIGIO,handle_signal)
    header = read_line()

    new_header = {
        'version': 1,
        'click_events': True
    }
    print_line(json.dumps(new_header))

    # The second line contains the start of the infinite array.
    print_line(read_line())
    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        
        cpuusage = ''
        for child in j:
             
            if child['name'] == 'wireless':
                text = child['full_text']
                child['border'] = '#89DDFF'
                child['full_text'] = '{} {}'.format(text.encode('utf-8'),get_networkspeed())

            if child['name'] == 'cpu_usage':
                cpuusage = child['full_text']

            if child['name'] == 'volume':
                child['border'] = '#FF5370'
 
            if child['name'] == 'battery':
                child['border'] = '#C792EA'

            if child['name'] == 'tztime':
                child['border'] = '#F78C6C'

        del j[0]
        # subprocess.call(['notify-send','f {}'.format(cpu_usage)])
        j.insert(0, {
            'full_text':"{} {}".format(get_cpu_text(),cpuusage),
            'name': 'cpu',
            'markup':'pango',
            'border': '#ffb63c'
            
        })
        j.insert(0, {
            'full_text':get_gpu_text(),
            'name': 'gpu',
            'markup':'pango',
            'border': '#91B859'
        })
        for child in j:
            child['border_bottom'] = 3
            child['border_left'] = 0
            child['border_right'] = 0
            child['border_top'] = 0
        # and echo back new encoded json
        print_line('{}{}'.format(prefix,json.dumps(j)))

