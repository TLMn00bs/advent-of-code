# 🎄 AoC
my solutions to Advent of Code 2021.
this year i'm learning typescript, so i forked this [aoc-ts-starter](https://github.com/bpiggin/advent-of-code-typescript-starter) repo.

if i get the time, i'll try to take a look at [r/adventofcode](https://www.reddit.com/r/adventofcode) and post my favourites here. people is amazing.

> as last year, our group “[TLMn00bs](https://github.com/TLMn00bs)” keeps sharing our solutions in this [repository](https://github.com/TLMn00bs/advent-of-code).

i've also learnt how to set a [workflow file in Github Actions](https://github.com/jartigag/aoc-2021/blob/main/.github/workflows/leaderboard_pipeline.yml) to [update our scores in the leaderboard branch's readme](https://github.com/jartigag/aoc-2021/tree/leaderboard#readme), using [this bash script](https://github.com/jartigag/aoc-2021/blob/main/update_leaderboard.sh).
it was a bit annoying to test the pipeline, but i [discovered a couple of things about git merge](https://github.com/jartigag/aoc-2021/search?q=path%3A.github%2Fworkflows+git+merge) on the way and i see a lot of potential in this tool.

#### getting started

```shell
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
```
not bad.. 😅

### solutions and posts
	
- [Day 1:  Sonar Sweep](https://github.com/jartigag/aoc-2021/blob/main/src/day1/day1.ts)  
	- [Day 1, part 2](https://github.com/jartigag/aoc-2021/blob/main/src/day1/day1part2.ts)
	<details> <summary> from <a href="https://www.reddit.com/r/adventofcode/comments/r71sss/2021_day_1_ue4_short_intro_video">r/adventofcode</a> <code>#viz</code> [UE4] Short intro video! </summary> <a href="https://youtu.be/RgNOVMDoNgs"><img src="http://i3.ytimg.com/vi/RgNOVMDoNgs/maxresdefault.jpg"/></a> </details> 
	
- [Day 2:  Dive!](https://github.com/jartigag/aoc-2021/blob/main/src/day2/day2.ts)  
	- [Day 2, part 2](https://github.com/jartigag/aoc-2021/blob/main/src/day2/day2part2.ts)
	<details> <summary> from <a href="https://www.reddit.com/r/adventofcode/comments/r7o188/2021_day_2_part_1_python_terminal_visualization">r/adventofcode</a> <code>#viz</code> [Python] Terminal Visualization. (Don't worry, Christmas smoke is non-toxic!) </summary> <a href="https://www.reddit.com/r/adventofcode/comments/r7o188/2021_day_2_part_1_python_terminal_visualization"> <img src="https://external-preview.redd.it/zbexd6zMaZt8AcyDTSyvslGjwFdbLIohJ3EDPVjWUsk.png?width=960&crop=smart&format=pjpg&auto=webp&s=c7f0b306905f9635d1f935995f6e9e3f882d9498"/> </a> </details> 
	
- [Day 3:  Binary Diagnostic](https://github.com/jartigag/aoc-2021/blob/main/src/day3/day3.ts)  
	- [Day 3, part 2](https://github.com/jartigag/aoc-2021/blob/main/src/day3/day3part2.ts)
	<details> <summary> from <a href="https://www.reddit.com/r/adventofcode/comments/r7x4yk/2021_day_3_part_2pygame_oxy_filter/">r/adventofcode</a> <code>#viz</code> [Pygame] OXY filter </summary> <a href="https://www.reddit.com/r/adventofcode/comments/r7x4yk/2021_day_3_part_2pygame_oxy_filter/"> <img src="https://external-preview.redd.it/kuPpBvcF3VGo8wr1JJPR_yrTP8d0H1wgqGOnfcgU9tI.png?width=960&crop=smart&format=pjpg&auto=webp&s=2e8addc9519f9fe4e43d1f4d4d83b2fe9e7864f4"/> </a> </details> 
	
- [Day 4:  Giant Squid](https://github.com/jartigag/aoc-2021/blob/main/src/day4/day4.ts)  
	- [Day 4, part 2](https://github.com/jartigag/aoc-2021/blob/main/src/day4/day4part2.ts)
	<details> <summary> from <a href="https://www.reddit.com/r/adventofcode/comments/r8wq0c/2021_day_4_bingo_blinkenlights/">r/adventofcode</a> <code>#viz</code> Bingo Blinkenlights </summary> <a href="https://www.reddit.com/r/adventofcode/comments/r8wq0c/2021_day_4_bingo_blinkenlights/"> <img src="https://external-preview.redd.it/CQ2SnbwRcpxOpCchIo5BL-pCO2uvnLuh-JNzwZwza2c.png?width=960&crop=smart&format=pjpg&auto=webp&s=878b488ea3dedc2e33536145fcdab17bc7475c82"/> </a> </details> 
- [Day 6:  Lanternfish](https://github.com/jartigag/aoc-2021/blob/main/src/day6/day6.ts)  
	- [Day 6, part 2](https://github.com/jartigag/aoc-2021/blob/main/src/day6/day6part2.ts)
- [Day 8:  Seven Segment Search](https://github.com/jartigag/aoc-2021/blob/main/src/day8/day8.ts)  

---
(merged from [https://github.com/jartigag/aoc-2021](https://github.com/jartigag/aoc-2021))
