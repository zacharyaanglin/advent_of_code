import collections
import io

import advent_of_code.day_11.main as day_11


def test_day_11():
    input_text = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""
    buf = io.StringIO(input_text)
    seats = day_11.Seats(grid=collections.defaultdict(dict))
    for y, line in enumerate(buf.readlines()):
        for x, character in enumerate(line):
            if character == "L":
                new_seat = day_11.Seat(state=day_11.State.EMPTY, x=x, y=y)
            elif character == "#":
                new_seat = day_11.Seat(state=day_11.State.OCCUPIED, x=x, y=y)
            elif character == ".":
                new_seat = day_11.Seat(state=day_11.State.FLOOR, x=x, y=y)
            else:
                continue
            seats.grid[x][y] = new_seat
    seats.set_maxes()
    breakpoint()
    seats.simulate()

    assert seats.count_occupied() == 37

