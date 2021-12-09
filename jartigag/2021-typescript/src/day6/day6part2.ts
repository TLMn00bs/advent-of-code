import { data } from './data.day6';
import { simulateLanternfish } from './day6';

export const day6part2 = (input: number[]) => simulateLanternfish(data, 256);

/*
--- Part Two ---

Suppose the lanternfish live forever and have unlimited food and space. Would
they take over the entire ocean?

[..]

How many lanternfish would there be after 256 days?
*/
