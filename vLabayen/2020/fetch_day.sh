#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Usage : ./fetch_day.sh <day> <sessionCookie>"
	exit 1
fi

day=$1
sessionCookie=$2
url="https://adventofcode.com/2020/day/$day/input"

mkdir day$day
curl --cookie "session=$sessionCookie" $url > day$day/input.txt
