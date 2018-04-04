#!/bin/bash
path="/home/lior/.config/i3/headphones"
read headphones < "${path}"
echo $headphones
if [ $headphones = "YES" ]
then
  echo 'changing headphons to no'
  printf "NO" | tee $path
  amixer sset Speaker 70%
  notify-send -t 200 --icon=gtk-info Speakers On
else
  echo 'changing headphons to yes'
  printf "YES" | tee $path
  amixer sset Speaker 0%
  notify-send -t 200 --icon=gtk-info Headphones On
fi
