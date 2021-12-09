import { logAnswer } from '../utils/logging';
import { data } from './data.day2';
import { calculateNewPositionAndDepth, day2part2 } from './day2part2';

test('Provided test cases', () => {
    expect(
        calculateNewPositionAndDepth({
            aim: 0,
            horizontalPosition: 0,
            depth: 0,
            instructions: ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2'],
        }),
    ).toBe(900);
});

test('Returns an answer', () => {
    logAnswer(day2part2(data));
    expect(typeof day2part2(data)).toBe('number');
    expect(day2part2(data)).toBeGreaterThan(0);
});
