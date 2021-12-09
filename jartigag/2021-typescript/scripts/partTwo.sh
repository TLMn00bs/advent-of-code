#!/bin/bash
echo "import { data } from './data.day$1';

export const func = (array: number[]) => {
  return $1;
};

export const day$1part2 = (input: number[]) => func(data);" >> src/day$1/day$1part2.ts

echo "import { logAnswer } from '../utils/logging';
import { data } from './data.day$1';
import { func, day$1part2 } from './day$1part2';

test('Provided test cases', () => {
    expect(func(data)).toBe($1);
});

test('Returns an answer', () => {
    logAnswer(day$1part2(data));
    expect(typeof day$1part2(data)).toBe('number');
    expect(day$1part2(data)).toBeGreaterThan(0);
});
" >> src/day$1/test.day$1part2.test.ts
