import { data } from './data.day1';

export const countSumIncreases = (array: number[]) => {
    let count = 0;

    for (let i = 3; i < array.length; i++) {
        let currentSum = array[i] + array[i - 1] + array[i - 2];
        let previousSum = array[i - 1] + array[i - 2] + array[i - 3];
        if (currentSum > previousSum) {
            count++;
        }
    }

    return count;
};

export const day1part2 = (input: number[]) => countSumIncreases(data);

/*
--- Part Two ---

Considering every single measurement isn't as useful as you expected: there's
just too much noise in the data.

Instead, consider sums of a three-measurement sliding window.

[..]

Your goal now is to count the number of times the sum of measurements in this
sliding window increases from the previous sum.

[..]

Consider sums of a three-measurement sliding window. How many sums are larger
than the previous sum?
*/
