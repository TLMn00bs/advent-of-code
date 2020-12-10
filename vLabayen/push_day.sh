#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Usage : ./push_day.sh <day> <sessionCookie>"
	exit 1
fi

day=$1
sessionCookie=$2

#Fetch day formulation
url="https://adventofcode.com/2020/day/$day"
curl --cookie "session=$sessionCookie" $url 2>/dev/null > day$day/tmp.txt

#Parse day formulation
python3 -c "
import re
from bs4 import BeautifulSoup

html = open('day$day/tmp.txt').read().split('<main>', 1)[1].split('</main>', 1)[0].replace('<h2>', '').replace('</h2>', '\n')
soup = BeautifulSoup(html)
text = soup.get_text()

ans = re.findall('(Your puzzle answer was \d+.)', text)
for a in ans: text = text.replace(a, '{}\n\n'.format(a))

print(text.replace('[Shareon\n  Twitter\nMastodon]', 'share'))
" > day$day/formulation.txt

echo "Created file day$day/formulation.txt"


# GITHUB HTML SANITIZER FUCKED ME :*(
#Fetch day drawing
#url="https://adventofcode.com/"
#curl --cookie "session=$sessionCookie" $url 2>/dev/null > day$day/tmp.txt
#
#Parse day drawing
#python3 -c "
#import re
#color_mappings = {
#	'calendar-color-l' : '#ccccff',
#	'calendar-color-r' : '#ff0000',
#	'calendar-color-w' : '#ffffff',
#	'calendar-color-a' : '#cccccc',
#	'calendar-color-b' : '#333399',
#	'calendar-color-g' : '#00cc00'
#}
#
#dayhtml = open('day$day/tmp.txt').read().split('day$day calendar-verycomplete\">', 1)[1].split('<span class=\"calendar-day')[0]
#spans = re.findall('(<span class=\"(.*?)\"+>.*?<+/span>)', dayhtml)
#dayhtml = dayhtml.replace(' ', '&nbsp;')
#
#for sp,c in spans:
#	dayhtml = dayhtml.replace(sp.replace(' ', '&nbsp;'), sp.replace('class=\"{}\"'.format(c), 'style=\"color:{};\"'.format(color_mappings[c])))
#
#code_link = '<a style=\"color:#ffffff\" href=\"day$day\">$day <span style="color:#ffff66">**</span></a>'
#print('<div style=\"font-family:\'Source Code Pro\', monospace; background-color:#0f0f23; width:max-content\">{}{}</div>'.format(dayhtml, code_link))
#" >> README.md
#
#echo "Updated README.md"


#Remove tmp file
rm day$day/tmp.txt


#Ensure we are in sync
git fetch
git pull

#Push to git
git add day$day/*
git commit -m "Day$day"
git push origin vLabayen
