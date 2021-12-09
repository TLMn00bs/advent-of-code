import { logAnswer } from '../utils/logging';
import { data } from './data.day1';
import { countSumIncreases, day1part2 } from './day1part2';

test('Provided test cases', () => {
    expect(countSumIncreases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])).toBe(5);
});

test('Returns an answer', () => {
    logAnswer(day1part2(data));
    expect(typeof day1part2(data)).toBe('number');
    expect(day1part2(data)).toBeGreaterThan(0);
});
