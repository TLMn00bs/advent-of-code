#!/bin/bash
here=$(cd $(dirname $BASH_SOURCE) && pwd)

if [ $# -lt 1 ]; then
	echo "Usage: init_day.bash <dx> [sessionCookie]" 1>&2
	exit 1
fi
dx=$1

if [ -d $dx ]; then
	echo "Error: $dx already exists" 1>&2
	exit 1
fi

cp -r $here/template $here/$dx
cd $here/$dx

mv template.py $dx.py

if [ $# == 2 ]; then
	# dx is, for example, d5, while the url must be just 5
	dx_url="${dx:1}"	# Remove first character
	curl --cookie "session=$2" "https://adventofcode.com/2022/day/${dx_url}/input" > input.txt
fi
