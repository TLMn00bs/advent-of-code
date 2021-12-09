#!/bin/bash
mkdir src/day$1
sessionCookie=$(cat cookie)
curl --cookie "session=$sessionCookie" https://adventofcode.com/2021/day/$1/input > src/day$1/input

if [ $? -ne 0 ] ; then
  echo "Day already exists!"
  exit
fi

echo "import { data } from './data.day$1';

export const func = (array: number[]) => {
  return $1;
};

export const day$1 = (input: number[]) => func(data);" >> src/day$1/day$1.ts

echo "import { logAnswer } from '../utils/logging';
import { data } from './data.day$1';
import { func, day$1 } from './day$1';

test('Provided test cases', () => {
  expect(func(data)).toBe($1);
});

test('Returns an answer', () => {
  logAnswer(day$1(data));
  expect(typeof day$1(data)).toBe('number');
  expect(day$1(data)).toBeGreaterThan(0);
});" >> src/day$1/test.day$1.test.ts

echo "import * as fs from 'fs';
import { parseInput } from '../utils/input';

const input = fs.readFileSync(__dirname + '/input').toString();

export const data = parseInput(input) as number[];" >> src/day$1/data.day$1.ts
exit
