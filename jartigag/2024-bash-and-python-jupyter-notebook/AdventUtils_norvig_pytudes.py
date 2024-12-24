#!/usr/bin/env python

############################
# Advent of Code Utilities #
#                          #
#            Peter Norvig, #
#      Decembers 2016–2023 #
############################

# __Advent of Code Utilities__
# Stuff I might need for [Advent of Code](https://adventofcode.com).
# First, some imports that I have used in past AoC years:

import matplotlib.pyplot as plt
import time
from statistics import mean, median
from typing import *

# __Daily Workflow__
# Each day's work will consist of three tasks, denoted by three sections in the notebook:
# - **Input**: Parse the day's input file with the function `parse`.
# - **Part 1**: Understand the day's instructions and:
#    - Write code to compute the answer to Part 1.
#    - Once I have computed the  answer and submitted it to the AoC site to verify it is correct,
#      I record it with the `answer` class.
# - **Part 2**: Repeat the above steps for Part 2.

# __Parsing Input Files__
# The function `parse` is meant to handle each day's input.
# A call `parse(day, parser, sections)` does the following:
# - Reads the input file for `day`.
# - Breaks the file into a *sections*.
#   By default, this is lines, but you can use `paragraphs`, or pass in a custom function.
# - Applies `parser` to each section and returns the results as a tuple of records.
#     - Useful parser functions include `ints`, `digits`, `atoms`, `words`, and the built-ins `int` and `str`.
# - Prints the first few input lines and output records.
#   This is useful to me as a debugging tool, and to the reader.
# - The defaults are `parser=str, sections=lines`,
#   so by default `parse(n)` gives a tuple of lines from fuile *day*.

lines = str.splitlines # By default, split input text into lines

def paragraphs(text): "Split text into paragraphs"; return text.split('\n\n')

def parse(day_or_text:Union[int, str], parser=str, sections=lines, show=8) -> tuple:
    """Split the input text into `sections`, and apply `parser` to each.
    The first argument is either the text itself, or the day number of a text file."""
    if isinstance(day_or_text, str) and show == 8:
        show = 0 # By default, don't show lines when parsing example text.
    start = time.time()
    text = get_text(day_or_text)
    show_items('Puzzle input', text.splitlines(), show)
    records = mapt(parser, sections(text.rstrip()))
    if parser != str or sections != lines:
        show_items('Parsed representation', records, show)
    return records

def get_text(day_or_text: Union[int, str]) -> str:
    import pathlib
    """The text used as input to the puzzle: either a string or the day number,
    which denotes the file 'input{day}.txt'."""
    if isinstance(day_or_text, str):
        return day_or_text
    else:
        filename = f'input{day_or_text}.txt'
        return pathlib.Path(filename).read_text()

def show_items(source, items, show:int, hr="─"*100):
    """Show the first few items, in a pretty format."""
    if show:
        types = Counter(map(type, items))
        counts = ', '.join(f'{n} {t.__name__}{"" if n == 1 else "s"}' for t, n in types.items())
        print(f'{hr}\n{source} ➜ {counts}:\n{hr}')
        for line in items[:show]:
            print(truncate(line))
        if show < len(items):
            print('...')

# Functions that can be used as the `parser` argument to `parse`
# (also, consider `str.split` to split the line on whitespace):

Char = str # Intended as the type of a one-character string
Atom = Union[str, float, int] # The type of a string or number
Ints = Sequence[int]

import re

def ints(text: str) -> Tuple[int]:
    """A tuple of all the integers in text, ignoring non-number characters."""
    return mapt(int, re.findall(r'-?[0-9]+', text))

def positive_ints(text: str) -> Tuple[int]:
    """A tuple of all the integers in text, ignoring non-number characters."""
    return mapt(int, re.findall(r'[0-9]+', text))

def digits(text: str) -> Tuple[int]:
    """A tuple of all the digits in text (as ints 0–9), ignoring non-digit characters."""
    return mapt(int, re.findall(r'[0-9]', text))

def words(text: str) -> Tuple[str]:
    """A tuple of all the alphabetic words in text, ignoring non-letters."""
    return tuple(re.findall(r'[a-zA-Z]+', text))

def atoms(text: str) -> Tuple[Atom]:
    """A tuple of all the atoms (numbers or identifiers) in text. Skip punctuation."""
    return mapt(atom, re.findall(r'[+-]?\d+\.?\d*|\w+', text))

def atom(text: str) -> Atom:
    """Parse text into a single float or int or str."""
    try:
        x = float(text)
        return round(x) if x.is_integer() else x
    except ValueError:
        return text.strip()

# __Daily Answers__
# Here is the `answer` class, which gives verification of a correct computation
# (or an error message for an incorrect computation),
# times how long the computation took,
# and stores the result in the dict `answers`.

answers = {} # `answers` is a dict of {puzzle_number: answer}

unknown = 'unknown'

class answer:
    """Verify that calling `code` computes the `solution` to `puzzle`.
    Record results in the dict `answers`."""
    def __init__(self, puzzle: float, solution, code:Callable=lambda:unknown):
        self.puzzle, self.solution, self.code = puzzle, solution, code
        answers[puzzle] = self
        self.check()

    def check(self) -> bool:
        """Check if the code computes the correct solution; record run time."""
        start     = time.time()
        self.got  = self.code()
        self.secs = time.time() - start
        self.ok   = (self.got == self.solution)
        return self.ok

    def __repr__(self) -> str:
        """The repr of an answer shows what happened."""
        secs    = f'{self.secs:7.4f}'.replace(' 0.', '  .')
        comment = (f'' if self.got == unknown else
                   f' ok' if self.ok else
                   f' WRONG; expected answer is {self.solution}')
        return f'Puzzle {self.puzzle:4.1f}: {secs} seconds, answer {self.got:<15}{comment}'

def summary(answers):
    """Print a report that summarizes the answers."""
    for d in sorted(answers):
        print(answers[d])
    times = [answers[d].secs for d in answers]
    print(f'\nCorrect: {quantify(answers[d].ok for d in answers)}/{len(answers)}')
    print(f'\nTime in seconds: {median(times):.3f} median, {mean(times):.3f} mean, {sum(times):.3f} total.')

# __Additional utility functions__
# All of the following have been used in solutions to multiple puzzles in the past,
# so I pulled them all in here:

def prod(numbers) -> float: # Will be math.prod in Python 3.8
    """The product formed by multiplying `numbers` together."""
    result = 1
    for x in numbers:
        result *= x
    return result

def T(matrix: Sequence[Sequence]) -> List[Tuple]:
    """The transpose of a matrix: T([(1,2,3), (4,5,6)]) == [(1,4), (2,5), (3,6)]"""
    return list(zip(*matrix))

def total(counter: Counter) -> int:
    """The sum of all the counts in a Counter."""
    return sum(counter.values())

def cover(*integers) -> range:
    """A `range` that covers all the given integers, and any in between them.
    cover(lo, hi) is an inclusive (or closed) range, equal to range(lo, hi + 1).
    The same range results from cover(hi, lo) or cover([hi, lo])."""
    if len(integers) == 1: integers = the(integers)
    return range(min(integers), max(integers) + 1)

def the(sequence) -> object:
    """Return the one item in a sequence. Raise error if not exactly one."""
    for i, item in enumerate(sequence, 1):
        if i > 1: raise ValueError(f'Expected exactly one item in the sequence.')
    return item

def sign(x) -> int: "0, +1, or -1"; return (0 if x == 0 else +1 if x > 0 else -1)

def union(sets) -> set: "Union of several sets"; return set().union(*sets)

def accumulate(item_count_pairs: Iterable[Tuple[object, int]]) -> Counter:
    """Add up all the (item, count) pairs into a Counter."""
    counter = Counter()
    for (item, count) in item_count_pairs:
        counter[item] += count
    return counter

def truncate(object, width=100, ellipsis=' ...') -> str:
    """Use elipsis to truncate `str(object)` to `width` characters, if necessary."""
    string = str(object)
    return string if len(string) <= width else string[:width-len(ellipsis)] + ellipsis

def mapt(function: Callable, *sequences) -> tuple:
    """`map`, with the result as a tuple."""
    return tuple(map(function, *sequences))

# __Itertools Recipes__
# The Python docs for the itertools module has some
# [recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes)
# that I include here (some I have slightly modified):

from itertools import chain

flatten = chain.from_iterable # Yield items from each sequence in turn

def quantify(iterable, pred=bool) -> int:
    """Count the number of items in iterable for which pred is true."""
    return sum(1 for item in iterable if pred(item))

def append(sequences) -> Sequence: "Append into a list"; return list(flatten(sequences))

# __Points in Space__
# Many puzzles involve points; usually two-dimensional points on a plane.
# A few puzzles involve three-dimensional points,
# and perhaps one might involve non-integers,
# so I'll try to make my Point implementation flexible in a duck-typing way.
# A point can also be considered a Vector;
# that is, (1, 0) can be a Point that means "this is location x=1, y=0 in the plane"
# and it also can be a Vector that means "move Eat (+1 in the along the x axis)."
# First we'll define points/vectors:

Point  = Tuple[int, ...] # Type for points
Vector = Point           # E.g., (1, 0) can be a point, or can be a direction, a Vector
Zero   = (0, 0)

directions4 = East, South, West, North = ((1, 0), (0, 1),  (-1, 0), (0, -1))
diagonals   = SE,   NE,    SW,   NW    = ((1, 1), (1, -1), (-1, 1), (-1, -1))
directions8 = directions4 + diagonals
directions5 = directions4 + (Zero,)
directions9 = directions8 + (Zero,)
arrow_direction = {'^': North, 'v': South, '>': East, '<': West, '.': Zero,
                   'U': North, 'D': South, 'R': East, 'L': West}

def X_(point) -> int: "X coordinate of a point"; return point[0]
def Y_(point) -> int: "Y coordinate of a point"; return point[1]
def Z_(point) -> int: "Z coordinate of a point"; return point[2]

def Xs(points) -> Tuple[int]: "X coordinates of a collection of points"; return mapt(X_, points)
def Ys(points) -> Tuple[int]: "Y coordinates of a collection of points"; return mapt(Y_, points)
def Zs(points) -> Tuple[int]: "X coordinates of a collection of points"; return mapt(Z_, points)

import operator
def add(p: Point, q: Point)              -> Point:  "Add points";      return mapt(operator.add, p, q)
def sub(p: Point, q: Point)              -> Point:  "Subtract points"; return mapt(operator.sub, p, q)
def neg(p: Point)                        -> Vector: "Negate a point";  return mapt(operator.neg, p)
def mul(p: Point, k: float)              -> Vector: "Scalar multiply"; return tuple(k * c for c in p)

def distance(p: Point, q: Point) -> float:
    """Euclidean (L2) distance between two points."""
    d = sum((pi - qi) ** 2 for pi, qi in zip(p, q)) ** 0.5
    return int(d) if d.is_integer() else d

def slide(points: Set[Point], delta: Vector) -> Set[Point]:
    """Slide all the points in the set of points by the amount delta."""
    return {add(p, delta) for p in points}
def make_turn(facing:Vector, turn:str) -> Vector:
    """Turn 90 degrees left or right. `turn` can be 'L' or 'Left' or 'R' or 'Right' or lowercase."""
    (x, y) = facing
    return (y, -x) if turn[0] in ('L', 'l') else (-y, x)

def add2(p: Point, q: Point) -> Point:
    """Specialized version of point addition for 2D Points only. Faster."""
    return (p[0] + q[0], p[1] + q[1])

def sub2(p: Point, q: Point) -> Point:
    """Specialized version of point subtraction for 2D Points only. Faster."""
    return (p[0] - q[0], p[1] - q[1])

def taxi_distance(p: Point, q: Point) -> int:
    """Manhattan (L1) distance between two 2D Points."""
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

# __Points on a Grid__
# Many puzzles seem to involve a two-dimensional rectangular grid with integer coordinates.
# A `Grid` is a rectangular array of (integer, integer) points, where each point holds some contents.
# Important things to know:
# - `Grid` is a subclass of `dict`
# - Usually the contents will be a character or an integer, but that's not specified or restricted.
# - A `Grid` can be initialized three ways:
#   - With another dict of `{point: contents}`, or an iterable of `(point, contents)` pairs.
#   - With an iterable of strings, each depicting a row (e.g. `["#..", "..#"]`).
#   - With a single string, which will be split on newlines.
# - Contents that are a member of `skip` will be skipped.
#   For example, you could do `skip=[' ']` to not store any point that has a space as its contents.
# - There is a `grid.neighbors(point)` method.
#   By default it returns the 4 orthogonal neighbors but you could make it all 8 adjacent squares,
#   or something else, by specifying the `directions` keyword value in the `Grid` constructor.
# - By default, grids have bounded size; accessing a point outside the grid results in a `KeyError`.
#   But some grids extend in all directions without limit; you can implement that by specifying,
#   say, `default='.'` to make `'.'` contents in all directions.

class Grid(dict):
    """A 2D grid, implemented as a mapping of {(x, y): cell_contents}."""
    def __init__(self, grid=(), directions=directions4, skip=(), default=None):
        """Initialize one of four ways:
        `Grid({(0, 0): '#', (1, 0): '.', ...})`
        `Grid(another_grid)
        `Grid(["#..", "..#"])
        `Grid("#..\n..#")`."""
        self.directions = directions
        self.skip = skip
        self.default = default
        from collections import abc
        if isinstance(grid, abc.Mapping):
            self.update(grid)
            self.size = (len(cover(Xs(self))), len(cover(Ys(self))))
        else:
            if isinstance(grid, str):
                grid = grid.splitlines()
            self.size = (max(map(len, grid)), len(grid))
            self.update({(x, y): val
                         for y, row in enumerate(grid)
                         for x, val in enumerate(row)
                         if val not in skip})

    def __missing__(self, point):
        """If asked for a point off the grid, either return default or raise error."""
        if self.default == KeyError:
            raise KeyError(point)
        else:
            return self.default

    def in_range(self, point) -> bool:
        """Is the point within the range of the grid's size?"""
        return (0 <= X_(point) < X_(self.size) and
                0 <= Y_(point) < Y_(self.size))

    def follow_line(self, start: Point, direction: Vector) -> Iterable[Point]:
        while self.in_range(start):
            yield start
            start = add2(start, direction)

    def copy(self):
        return Grid(self, directions=self.directions, skip=self.skip, default=self.default)

    def neighbors(self, point) -> List[Point]:
        """Points on the grid that neighbor `point`."""
        return [add2(point, Δ) for Δ in self.directions
                if add2(point, Δ) in self or self.default not in (KeyError, None)]

    def neighbor_contents(self, point) -> Iterable:
        """The contents of the neighboring points."""
        return (self[p] for p in self.neighbors(point))

    def findall(self, contents: Collection) -> List[Point]:
        """All points that contain one of the given contents, e.g. grid.findall('#')."""
        return [p for p in self if self[p] in contents]

    def to_rows(self, xrange=None, yrange=None) -> List[List[object]]:
        """The contents of the grid, as a rectangular list of lists.
        You can define a window with an xrange and yrange; or they default to the whole grid."""
        xrange = xrange or cover(Xs(self))
        yrange = yrange or cover(Ys(self))
        default = ' ' if self.default in (KeyError, None) else self.default
        return [[self.get((x, y), default) for x in xrange]
                for y in yrange]

    def print(self, sep='', xrange=None, yrange=None):
        """Print a representation of the grid."""
        for row in self.to_rows(xrange, yrange):
            print(*row, sep=sep)

    def plot(self, markers={'#': 's', '.': ','}, figsize=(14, 14), **kwds):
        """Plot a representation of the grid."""
        plt.figure(figsize=figsize)
        plt.gca().invert_yaxis()
        for m in markers:
            plt.plot(*T(p for p in self if self[p] == m), markers[m], **kwds)

def neighbors(point, directions=directions4) -> List[Point]:
    """Neighbors of this point, in the given directions.
    (This function can be used outside of a Grid class.)"""
    return [add(point, Δ) for Δ in directions]

if __name__ == "__main__":
    def tests():
        """Run tests on utility functions. Also serves as usage examples."""

        # PARSER

        assert parse("hello\nworld", show=0) == ('hello', 'world')
        assert parse("123\nabc7", digits, show=0) == ((1, 2, 3), (7,))
        assert truncate('hello world', 99) == 'hello world'
        assert truncate('hello world', 8)  == 'hell ...'

        assert         atoms('hello, cruel_world! 24-7') == ('hello', 'cruel_world', 24, -7)
        assert         words('hello, cruel_world! 24-7') == ('hello', 'cruel', 'world')
        assert        digits('hello, cruel_world! 24-7') == (2, 4, 7)
        assert          ints('hello, cruel_world! 24-7') == (24, -7)
        assert positive_ints('hello, cruel_world! 24-7') == (24, 7)

        # UTILITIES

        assert total(Counter('hello, world')) == 12
        assert cover(3, 1, 4, 1, 5) == range(1, 6)
        assert T([(1, 2, 3), (4, 5, 6)]) == [(1, 4), (2, 5), (3, 6)]
        assert the({1}) == 1
        assert union([{1, 2}, {3, 4}, {5, 6}]) == {1, 2, 3, 4, 5, 6}

        # ITERTOOL RECIPES
        assert append(([1, 2], [3, 4], [5, 6])) == [1, 2, 3, 4, 5, 6]

        # POINTS

        p, q = (0, 3), (4, 0)
        assert Y_(p) == 3 and X_(q) == 4
        assert distance(p, q) == 5
        assert add(p, q) == (4, 3)
        assert sub(p, q) == (-4, 3)
        assert add(North, South) == (0, 0)

    tests()
