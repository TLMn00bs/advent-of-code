#!/usr/bin/env python

input = [0]
input.extend( sorted( [int(line) for line in open("input").readlines()] ) )
input.append( input[-1]+3 )

def diffs_in_list(l):
    return [second-first for first,second in zip(input[:-1], input[1:])]

diffs = diffs_in_list(input)


print( diffs.count(1) * diffs.count(3) )



from itertools import groupby

def run_length_encoding(l):
    """
    RLE is a form of lossless data compression in which
    runs of data (sequences in which the same value occurs in many consecutive elements)
    are stored as a single data value and count. Example:
    WWWWWWBBWWWB: 6W2B3W1B
    https://en.wikipedia.org/wiki/Run-length_encoding
    """
    return [(len(list(group)),key) for key,group in groupby(l)]

rle_encoded_diffs = run_length_encoding(diffs)
#example: input             = [  1,    2,    5,    6,    9,  10,   11,  14,  15,  16,  17, 18 ]
#         diffs             = [   1,    3,    1,    3,    1,   1,    3,   1,   1,   1,   1 ]
#         rle_encoded_diffs = [(1,1),(1,3),(1,1),(1,3),     (2,1),(1,3),              (4,1)]
#                               l k=1       l k=1            l k=1                     l k=1

# so, how many times does      a row of 5 ones                          appear in `diffs`?
# that is, how many times does key=1 and len_group=4 (4 diffs of one) appear in `rle_encoded_diffs`?
five_ones_in_a_row  = sum( 1 if (k==1 and len_group==4) else 0 for len_group,k in rle_encoded_diffs )
four_ones_in_a_row  = sum( 1 if (k==1 and len_group==3) else 0 for len_group,k in rle_encoded_diffs )
three_ones_in_a_row = sum( 1 if (k==1 and len_group==2) else 0 for len_group,k in rle_encoded_diffs )
two_ones_in_a_row   = sum( 1 if (k==1 and len_group==1) else 0 for len_group,k in rle_encoded_diffs )


# https://www.reddit.com/r/adventofcode/comments/ka9pc3/2020_day_10_part_2_suspicious_factorisation/gf93njy
def tribonacci(n, adict={0:0, 1:0, 2:1}):
    """
    Tribonacci numbers: a(n) = a(n-1) + a(n-2) + a(n-3) for n >= 3 with a(0) = a(1) = 0 and a(2) = 1.
    https://oeis.org/A000073
    """
    if n in adict:
        return adict[n]
    adict[n]=tribonacci(n-1)+tribonacci(n-2)+tribonacci(n-3)
    return adict[n] # David Nacin, Mar 07 2012

# get enough elements from the tribonacci sequence:
trib_seq = []
n = 2 # because tribonacci(0)=tribonacci(1)=0, and we don't want 0
while len(trib_seq)<4:
    next_number = tribonacci(n)
    if next_number not in trib_seq: # we only want unique elements
        trib_seq.append(next_number)
    n+=1
# trib_seq = [1, 2, 4, 7]


print( trib_seq[0]**two_ones_in_a_row * trib_seq[1]**three_ones_in_a_row * trib_seq[2]**four_ones_in_a_row * trib_seq[3]**five_ones_in_a_row )
