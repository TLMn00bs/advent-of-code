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

mkdir $here/$dx
cp $here/template.py $here/$dx/$dx.py
cd $here/$dx

if [ $# == 2 ]; then
	# dx is, for example, d5, while the url must be just 5
	dx_url="${dx:1}"	# Remove first character
	curl --cookie "session=$2" "https://adventofcode.com/2023/day/${dx_url}/input" > input.txt
fi
