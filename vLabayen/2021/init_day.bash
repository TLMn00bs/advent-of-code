#!/bin/bash
here=$(dirname $(realpath ${BASH_SOURCE[0]}))

if [ $# -lt 1 ]; then
	echo "Usage: init_day.bash <dx> [sessionCookie]" 1>&2
	exit 1
fi
dx=$1

cp -r $here/template $here/$dx
cd $here/$dx

mv template.py $dx.py
cargo new ${dx}_rs
mv template.rs ${dx}_rs/src/main.rs

if [ $# == 2 ]; then
	# dx is, for example, d5, while the url must be just 5
	dx_url="${dx:1}"	# Remove first character
	curl --cookie "session=$2" "https://adventofcode.com/$(date +%Y)/day/${dx_url}/input" > input.txt
fi
