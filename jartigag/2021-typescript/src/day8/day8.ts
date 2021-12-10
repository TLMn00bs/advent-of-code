import { data, signalOutputPair } from './data.day8';

export const countUniqueNumberOfSegments = (signalOutputPairs: signalOutputPair[]) => {
    let count = 0;
    for (const signalOutputPair of signalOutputPairs) {
        for (const outputValue of signalOutputPair.outputValues) {
            if (
                outputValue.length == 2 /* only digit 1 has 2 segments */ ||
                outputValue.length == 3 /* only digit 7 has 3 segments */ ||
                outputValue.length == 4 /* only digit 4 has 4 segments */ ||
                outputValue.length == 7 /* only digit 8 has 7 segments */
            ) {
                count += 1;
            }
        }
    }
    return count;
};

export const day8 = (input: signalOutputPair[]) => countUniqueNumberOfSegments(data);

/*
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave
mouth, collapsing it. Sensors indicate another exit to this cave at a much
greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that
the four-digit seven-segment displays in your submarine are malfunctioning; they
must have been damaged during the escape. You'll be in a lot of trouble without
them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of
seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

So, to render a 1, only segments c and f would be turned on; the rest would be
off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on
each display. The submarine is still trying to display numbers by producing
output on signal wires a through g, but those wires are connected to segments
randomly. Worse, the wire/segment connections are mixed up separately for each
four-digit display! (All of the digits within a display use the same
connections, though.)

So, you might know that only signal wires b and g are turned on, but that
doesn't mean segments b and g are turned on: the only digit that uses two
segments is 1, so it must mean segments c and f are meant to be on. With just
that information, you still can't tell which wire (b/g) goes to which segment
(c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all
ten unique signal patterns you see, and then write down a single four digit
output value (your puzzle input). Using the signal patterns, you should be able
to work out which pattern corresponds to which digit.

[..]

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you
should be able to tell which combinations of signals correspond to those digits.
Counting only digits in the output values (the part after | on each line), in
the above example, there are 26 instances of digits that use a unique number of
segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
*/
