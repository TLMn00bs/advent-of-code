import { data } from './data.day1';

export const countIncreases = (array: number[]) => {
    let count = 0;

    for (let i = 1; i < array.length; i++) {
        if (array[i] > array[i - 1]) {
            count++;
        }
    }

    return count;
};

export const day1 = (input: number[]) => countIncreases(data);

/*
--- Day 1: Sonar Sweep ---

You're minding your own business on a ship at sea when the overboard alarm goes
off! You rush to see if you can help. Apparently, one of the Elves tripped and
accidentally sent the sleigh keys flying into the ocean!

Before you know it, you're inside a submarine the Elves keep ready for
situations like this. It's covered in Christmas lights (because of course it
is), and it even has an experimental antenna that should be able to track the
keys if you can boost its signal strength high enough; there's a little meter
that indicates the antenna's signal strength by displaying 0-50 stars.

Your instincts tell you that in order to save Christmas, you'll need to get all
fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!
*/

/*
As the submarine drops below the surface of the ocean, it automatically
performs a sonar sweep of the nearby sea floor. On a small screen, the sonar
sweep report (your puzzle input) appears: each line is a measurement of the sea
floor depth as the sweep looks further and further away from the submarine.

[..]

The first order of business is to figure out how quickly the depth increases,
just so you know what you're dealing with - you never know if the keys will get
carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the
previous measurement. (There is no measurement before the first measurement.)

[..]

How many measurements are larger than the previous measurement?
*/
