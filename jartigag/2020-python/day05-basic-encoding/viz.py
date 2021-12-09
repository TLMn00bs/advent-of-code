#!/usr/bin/env python3
# Visualization for airplane (@nirenjan)

import sys
import curses

def bsp(inp):
    bitmap = {
        'F': '0',
        'B': '1',
        'L': '0',
        'R': '1',
    }

    seat_id = ''.join(bitmap[i] for i in inp.strip())

    seat_id = int(seat_id, 2)
    row, seat = seat_id >> 3, seat_id & 7
    return row, seat, seat_id

def load_data(datafile):
    with open(datafile) as df:
        data = df.readlines()

    return data

def _main():
    try:
        datafile = sys.argv[1]
    except IndexError:
        datafile = 'input'

    data = load_data(datafile)

    # Get seats
    seats = [bsp(x) for x in data]

    max_seat_id = 0
    min_seat_id = 1024
    seat_map = ['0'] * 1024
    for seat in seats:
        seat_map[seat[2]] = '1'
        if max_seat_id < seat[2]:
            max_seat_id = seat[2]
        if min_seat_id > seat[2]:
            min_seat_id = seat[2]

    my_seat_id = ''.join(seat_map).find('101') + 1
    my_row, my_seat = my_seat_id >> 3, my_seat_id & 7

    max_row = max_seat_id >> 3
    min_row = min_seat_id >> 3
    num_rows = (max_row - min_row + 3)

    window = curses.initscr()
    curses.start_color()
    window.clearok(True)
    window.refresh()

    window.addstr(1, 6, '-' * num_rows)
    window.addstr(2, 5, '/')
    window.addstr(3, 4, '/')
    window.addstr(4, 3, '/')
    window.addstr(5, 2, '/')
    window.addstr(6, 1, '|')
    window.addstr(7, 1, '|')
    window.addstr(8, 2, '\\')
    window.addstr(9, 3, '\\')
    window.addstr(10, 4, '\\')
    window.addstr(11, 5, '\\')
    window.addstr(12, 6, '-' * num_rows)

    window.addstr(2, 6 + num_rows, '\\')
    window.addstr(3, 7 + num_rows, '\\')
    window.addstr(4, 8 + num_rows, '\\')
    window.addstr(5, 9 + num_rows, '\\')
    window.addstr(6, 10 + num_rows, '\\')
    window.addstr(7, 10 + num_rows, '/')
    window.addstr(8, 9 + num_rows, '/')
    window.addstr(9, 8 + num_rows, '/')
    window.addstr(10, 7 + num_rows, '/')
    window.addstr(11, 6 + num_rows, '/')

    row_fn = lambda row: row + 7 - min_row
    col_fn = lambda col: [11, 10, 8, 7, 6, 5, 3, 2][col]

    window.addch(col_fn(my_seat), row_fn(my_row), ']')
    for seat in seats:
        window.addch(col_fn(seat[1]), row_fn(seat[0]), ']')

    window.move(7, 2)

    window.refresh()

    curses.delay_output(2000)

    color_red = curses.color_pair(curses.COLOR_RED)
    for seat in seats:
        window.addch(col_fn(seat[1]), row_fn(seat[0]), '#')
        window.refresh()
        curses.delay_output(50)

    color_green = curses.color_pair(curses.COLOR_GREEN)
    window.addch(col_fn(my_seat), row_fn(my_row), '@')
    window.refresh()
    curses.delay_output(2000)

    curses.endwin()

if __name__ == '__main__':
    _main()

