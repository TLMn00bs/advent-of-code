#!/bin/bash

if [ "$#" != "1" ]; then
	echo "Usage: bench.bash <day>" 1>&2
	exit 1
fi
day=$1


start=$(date +%s%N)
python3 $day/$day.py $day/input.txt #1>>/dev/null 2>&1
mid=$(date +%s%N)
./$day/${day}_rs/target/release/${day}_rs $day/input.txt #1>>/dev/null 2>&1
end=$(date +%s%N)

python_time=$(python3 -c "print(($mid - $start) / 10e6)")
rust_time=$(python3 -c "print(($end - $mid) / 10e6)")
echo "python: $python_time ms"
echo "rust: $rust_time ms"
