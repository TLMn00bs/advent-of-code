import { parseInput } from '../utils/input';
import { logAnswer } from '../utils/logging';
import { data } from './data.day6';
import { simulateLanternfish } from './day6';
import { day6part2 } from './day6part2';

test('Provided test cases', () => {
    expect(simulateLanternfish(parseInput(`3,4,3,1,2`), 256)).toBe(26984457539);
});

test('Returns an answer', () => {
    logAnswer(day6part2(data));
    expect(typeof day6part2(data)).toBe('number');
    expect(day6part2(data)).toBeGreaterThan(0);
});
