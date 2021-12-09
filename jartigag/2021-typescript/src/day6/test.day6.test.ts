import { parseInput } from '../utils/input';
import { logAnswer } from '../utils/logging';
import { data } from './data.day6';
import { day6, simulateLanternfish } from './day6';

test('Provided test cases', () => {
    expect(simulateLanternfish(parseInput(`3,4,3,1,2`), 18)).toBe(26);
    expect(simulateLanternfish(parseInput(`3,4,3,1,2`), 80)).toBe(5934);
});

test('Returns an answer', () => {
    logAnswer(day6(data));
    expect(typeof day6(data)).toBe('number');
    expect(day6(data)).toBeGreaterThan(0);
});
