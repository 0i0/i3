#!/bin/bash
path="/home/lior/.config/i3/headphones"
read headphones < "${path}"
if [ $1 = "up" ]
then
  if [ $headphones = "YES" ]
  then
    amixer  sset Speaker 0%
    amixer  sset 'PCM',0 5%+
    echo "headphons up"
  else
    amixer  sset Speaker 5%+
    amixer  sset 'PCM',0 100%
    echo "speaker up"
  fi
else
  if [ $headphones = "YES" ] 
  then
    amixer  sset Speaker 0%
    amixer  sset 'PCM',0 5%-
    echo "headphons dn"
  else
    amixer  sset Speaker 5%-
    amixer  sset 'PCM',0 100%
    echo "speaker dn"
  fi
fi