import { logAnswer } from '../utils/logging';
import { data } from './data.day2';
import { calculatePositionAndDepth, day2 } from './day2';

test('Provided test cases', () => {
    expect(
        calculatePositionAndDepth({
            horizontalPosition: 0,
            depth: 0,
            instructions: ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2'],
        }),
    ).toBe(150);
});

test('Returns an answer', () => {
    logAnswer(day2(data));
    expect(typeof day2(data)).toBe('number');
    expect(day2(data)).toBeGreaterThan(0);
});
