import { logAnswer } from '../utils/logging';
import { data } from './data.day1';
import { countIncreases, day1 } from './day1';

test('Provided test cases', () => {
    expect(countIncreases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])).toBe(7);
});

test('Returns an answer', () => {
    logAnswer(day1(data));
    expect(typeof day1(data)).toBe('number');
    expect(day1(data)).toBeGreaterThan(0);
});
