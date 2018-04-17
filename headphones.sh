#!/bin/bash
path="/home/lior/.config/i3/headphones"
read headphones < "${path}"
echo $headphones
if [ $headphones = "YES" ]
then
  echo 'changing headphons to no'
  printf "NO" | tee $path
  amixer sset Speaker 70%
  notify-send -t 200 Speakers On
else
  echo 'changing headphons to yes'
  printf "YES" | tee $path
  amixer sset Speaker 0%
  notify-send -t 200 Headphones On
fi
