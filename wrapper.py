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

def get_gpu_text():
    util = subprocess.Popen(['nvidia-settings', '-t','-q','[gpu:0]/GPUUtilization'], stdout=subprocess.PIPE).communicate()[0]
    temp = subprocess.Popen(['nvidia-settings', '-t','-q','[gpu:0]/GPUCoreTemp'], stdout=subprocess.PIPE).communicate()[0]
    util_split = util.strip().split(',')
    return '<span color="#BBBBBB">GPU:</span>{}% {}°'.format(util_split[0].split('=')[1],temp.strip())

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

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        # CHANGE THIS LINE TO INSERT SOMETHING ELSE
        j.insert(0, {
            'full_text':get_cpu_text(),
            'name': 'cpu',
            'markup':'pango'
        })
        j.insert(0, {
            'full_text':get_gpu_text(),
            'name': 'gpu',
            'markup':'pango'
        })
        j.insert(0, {
            'full_text':get_networkspeed(),
            'name': 'network',
            'markup':'pango'
        })
        # j.insert(4, {'full_text': '%s' % get_governor(), 'name': 'gov'})
        # and echo back new encoded json
        print_line(prefix+json.dumps(j))