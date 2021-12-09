#!/bin/bash

########
# 2021 #
########

rm README.md

cat << EOF >> README.md
# 🎄 AoC - 2021
Here you can find some solutions to Advent of Code 2021.

 |  ☃️  |  🧰  |  ⭐  |
 | :--: | :--: | :-: |
EOF

curl --cookie "session=$COOKIE" -XGET https://adventofcode.com/2021/leaderboard/private/view/1065002.json 2>/dev/null > leaderboard2021.json

data=$(jq '.members | flatten | sort_by(.stars) | reverse | .[] | {name: .name, stars: .stars}' leaderboard2021.json | sed 's/Jesús Arellano/jesusarell/')

echo $data | jq -j '.name," ",.stars,"\n"' | \
awk 'BEGIN{
        langs["lassa97"]    ="Python"
        langs["vLabayen"]   ="Python / Rust"
        langs["calvo111979"]="Rust"
        langs["jartigag"]   ="Typescript"
        langs["mariaove"]   ="Java"
        langs["jesusarell"] ="Python"
        langs["0rb3"]       ="Python"
    }
    {print" | [@"$1"](https://github.com/"$1")| ["langs[$1]"](https://github.com/TLMn00bs/advent-of-code/tree/master/"$1") | "$2" |"}' >> README.md

########
# 2020 #
########

cat << EOF >> README.md

# 🎄 AoC - 2020
Here you can find some solutions to Advent of Code 2020.

 |  ☃️  |  🧰  |  ⭐  |
 | :--: | :--: | :-: |
EOF

curl --cookie "session=$COOKIE" -XGET https://adventofcode.com/2020/leaderboard/private/view/1065002.json 2>/dev/null > leaderboard2020.json

data=$(jq '.members | flatten | sort_by(.stars) | reverse | .[] | {name: .name, stars: .stars}' leaderboard2020.json | sed 's/Jesús Arellano/jesusarell/')

# fix order:
data=$(echo $data | sed 's/{ "name": "lassa97", "stars": 50 } { "name": "vLabayen", "stars": 50 }/{ "name": "vLabayen", "stars": 50 } { "name": "lassa97", "stars": 50 }/')

echo $data | jq -j '.name," ",.stars,"\n"' | \
awk 'BEGIN{
        langs["lassa97"]    ="Python"
        langs["vLabayen"]   ="Python"
        langs["calvo111979"]="Python"
        langs["jartigag"]   ="Python"
        langs["mariaove"]   ="Java"
        langs["jesusarell"] ="Python"
    }
    {print" | [@"$1"](https://github.com/"$1")| ["langs[$1]"](https://github.com/TLMn00bs/advent-of-code/tree/master/"$1") | "$2" |"}' >> README.md

rm leaderboard*.json
