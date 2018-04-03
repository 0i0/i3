#!/bin/sh
# shell script to prepend i3status with more stuff

i3status -c ~/.config/i3/i3stats.config | while :
do
  read line
  MESSAGE="$(curl -s https://api.coinmarketcap.com/v1/ticker/|jq '.[]|select((.rank|tonumber)<3)|{id,price_usd}|.id+" "+.price_usd'|awk '{gsub(/"/, "", $0);print " " substr($1,0,10) " " $2 " "}'|paste -sd "|" -)"
  MESSAGE+=" | GPU $(nvidia-settings -t -q [gpu:0]/GPUUtilization | awk -F, '{print $1}'|awk -F= '{print $2}')% $(nvidia-settings -t -q [gpu:0]/GPUCoreTemp)°"
  echo $MESSAGE $line || exit 1
done