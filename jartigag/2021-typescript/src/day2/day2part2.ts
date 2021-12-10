import { data } from './data.day2';

export interface NamedParameters {
    aim?: number;
    horizontalPosition: number;
    depth: number;
    instructions: string[];
}

export const calculateNewPositionAndDepth = (params: NamedParameters): number => {
    for (let i = 0; i < params.instructions.length; i++) {
        let [direction, units] = params.instructions[i].split(' ');
        switch (direction) {
            case 'forward':
                params.horizontalPosition += Number(units);
                params.depth += params.aim * Number(units);
                break;
            case 'down':
                params.aim += Number(units);
                break;
            case 'up':
                params.aim -= Number(units);
                break;
        }
    }
    return params.horizontalPosition * params.depth;
};

export const day2part2 = (input: string[]) =>
    calculateNewPositionAndDepth({ aim: 0, horizontalPosition: 0, depth: 0, instructions: data });

/*
--- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense.
You find the submarine manual and discover that the process is actually slightly
more complicated.

In addition to horizontal position and depth, you'll also need to track a third
value, aim, which also starts at 0. The commands also mean something entirely
different than you first thought:

    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.

Again note that since you're on a submarine, down and up do the opposite of what
you might expect: "down" means aiming in the positive direction.

[..]

Using this new interpretation of the commands, calculate the horizontal position
and depth you would have after following the planned course. What do you get if
you multiply your final horizontal position by your final depth?
*/
