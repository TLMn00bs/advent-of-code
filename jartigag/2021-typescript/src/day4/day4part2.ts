import { data } from './data.day4';
import { Bingo } from './day4';

const checkingLastScore = true;
export const day4part2 = (input: string) => new Bingo(data).solve(checkingLastScore);

/*
--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure out
which board will win last and choose that one. That way, no matter which boards
it picks, it will win for sure.

[..]

Figure out which board will win last. Once it wins, what would its final score
be?
*/
