#!/bin/sh

rm README.md

for f in $(find src/ -name "*.ts" -not -path "src/utils/*" -not -name "*test*" -not -name "*data*" -not -name "*part*")
do
    title=$(grep -e "--- Day " $f | sed 's/--- //g' | sed 's/ ---//g' | sed 's/: /:  /g')
    echo "- [$title](https://github.com/jartigag/aoc-2021/blob/main/$f)  " >> solutions_links.tmp
done

for f in $(find src/ -name "*part*.ts" -not -path "./src/utils/*" -not -name "*test*" -not -name "*data*")
do
    day=$(echo $f | sed 's/\(.*\)part.*/\1/' | tail -c 2)
    echo "- [Day $day, part 2](https://github.com/jartigag/aoc-2021/blob/main/$f)" >> solutions_links.tmp
done

for f in $(find subreddit/ -name "*day*.html")
do
    day=$(echo $f | sed 's/subreddit\/day\(.*\).html/\1/')
    oneline_html=$(sed 's/  //g' $f | tr '\n' ' ')
    echo "- [DAY $day·$oneline_html" >> solutions_links.tmp
    echo "- [DAY $day·" >> solutions_links.tmp
done


cat << EOF >> README.md
# 🎄 AoC
my solutions to Advent of Code 2021.
this year i'm learning typescript, so i forked this [aoc-ts-starter](https://github.com/bpiggin/advent-of-code-typescript-starter) repo.

if i get the time, i'll try to take a look at [r/adventofcode](https://www.reddit.com/r/adventofcode) and post my favourites here. people is amazing.

> as last year, our group “[TLMn00bs](https://github.com/TLMn00bs)” keeps sharing our solutions in this [repository](https://github.com/TLMn00bs/advent-of-code).

i've also learnt how to set a [workflow file in Github Actions](https://github.com/jartigag/aoc-2021/blob/main/.github/workflows/leaderboard_pipeline.yml) to [update our scores in the leaderboard branch's readme](https://github.com/jartigag/aoc-2021/tree/leaderboard#readme), using [this bash script](https://github.com/jartigag/aoc-2021/blob/main/update_leaderboard.sh).
it was a bit annoying to test the pipeline, but i [discovered a couple of things about git merge](https://github.com/jartigag/aoc-2021/search?q=path%3A.github%2Fworkflows+git+merge) on the way and i see a lot of potential in this tool.

#### getting started

\`\`\`shell
$ time yarn install
yarn install v1.22.15
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...

Done in 2.42s.

real    0m2,601s
user    0m3,294s
sys     0m1,299s

$ du -hs node_modules/
147M    node_modules/
\`\`\`
not bad.. 😅

### solutions and posts
EOF

sort solutions_links.tmp | sed 's/\(.*\)part.*ts)$/\t\1part2.ts)/g' | sed 's/\(- \[DAY.*·\)/\t/g' >> README.md
rm solutions_links.tmp
