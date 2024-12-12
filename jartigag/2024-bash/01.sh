#!/bin/bash

curl -H "Cookie: session=$COOKIE" -s https://adventofcode.com/2024/day/1/input -o input.txt

sorted_left=(  $(awk '{print $1}' input.txt | sort -n))
sorted_right=( $(awk '{print $2}' input.txt | sort -n))

total_distance=0
similarity_score=0
for i in "${!sorted_left[@]}"; do
  distance=$((       ${sorted_left[$i]} - ${sorted_right[$i]} ))
  total_distance=$(( total_distance + ${distance#-}           ))

  count=0
  left_value="${sorted_left[$i]}"
  for right_value in "${sorted_right[@]}"; do
  if [[ $left_value -eq $right_value ]]; then
    count=$((count + 1))
  fi
  done
  similarity_score=$((similarity_score + left_value * count))
done

echo "$total_distance"
echo "$similarity_score"
