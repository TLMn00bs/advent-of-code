import { data } from './data.day6';

export const sum = (a: number[]): number => a.reduce((acc, cur) => acc + cur, 0);

export const simulateLanternfish = (fish: number[], days: number): number => {
    let fishesGroupedByInternalTimer = [...Array(9)].map(() => 0);
    fish.forEach((fish) => (fishesGroupedByInternalTimer[fish] += 1));

    for (let day = 0; day < days; day++) {
        // Advance 1 day (= shift fishes by 1 to the left):
        fishesGroupedByInternalTimer = [
            ...fishesGroupedByInternalTimer.slice(1),
            ...fishesGroupedByInternalTimer.slice(0, 1),
        ];
        // Reset fishes at day 6 (and increase by the number of new fishes):
        fishesGroupedByInternalTimer[6] += fishesGroupedByInternalTimer[8];
    }

    return sum(fishesGroupedByInternalTimer);
};

export const day6 = (input: number[]) => simulateLanternfish(data, 80);

/*
--- Day 6: Lanternfish ---

The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to
reach such large numbers - maybe **exponentially** quickly? You should model
their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make
some guesses about their attributes. Surely, each lanternfish creates a new
lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish -
one lanternfish might have 2 days left until it creates another lanternfish,
while another might have 4. So, you can model each fish as a single number that
represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer
before it's capable of producing more lanternfish: two more days for its first
cycle.

[..]

Find a way to simulate lanternfish. How many lanternfish would there be after 80
days?
*/
