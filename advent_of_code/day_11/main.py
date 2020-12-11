import collections
import copy
import dataclasses
import enum
from typing import List, Optional


class State(enum.Enum):
    OCCUPIED = 1
    EMPTY = 2
    FLOOR = 3


@dataclasses.dataclass
class Seat:
    state: State
    x: int
    y: int
    neighbors: List["Seat"] = dataclasses.field(default_factory=list)
    new_state: Optional[State] = None

    def find_neighbors(self, seats: "Seats"):
        self.neighbors = list()
        grid = seats.grid
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y].state)
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1].state)
        if self.x < seats.x_max:
            self.neighbors.append(grid[self.x + 1][self.y].state)
        if self.y < seats.y_max:
            self.neighbors.append(grid[self.x][self.y + 1].state)
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x - 1][self.y - 1].state)
        if self.x < seats.x_max and self.y < seats.y_max:
            self.neighbors.append(grid[self.x + 1][self.y + 1].state)
        if self.x > 0 and self.y < seats.y_max:
            self.neighbors.append(grid[self.x - 1][self.y + 1].state)
        if self.x < seats.y_max and self.y > 0:
            self.neighbors.append(grid[self.x + 1][self.y - 1].state)

    def set_new_state(self):
        if self.state == State.EMPTY and State.OCCUPIED not in self.neighbors:
            self.new_state = State.OCCUPIED
        elif (
            self.state == State.OCCUPIED
            and collections.Counter(self.neighbors)[State.OCCUPIED] >= 4
        ):
            self.new_state = State.EMPTY
        else:
            self.new_state = copy.deepcopy(self.state)

    def transition_state(self):
        self.state = self.new_state
        self.new_state = None


@dataclasses.dataclass
class Seats:
    grid: collections.defaultdict(dict)
    x_max: int = dataclasses.field(init=False)
    y_max: int = dataclasses.field(init=False)

    def set_maxes(self):
        self.x_max = len(self.grid) - 1
        self.y_max = len(self.grid[0]) - 1

    def set_neighbors(self):
        for _, column in self.grid.items():
            for _, seat in column.items():
                seat.find_neighbors(self)
                seat.set_new_state()

    def state_transition(self):
        for _, column in self.grid.items():
            for _, seat in column.items():
                seat.transition_state()

    def simulate(self):
        steps = 0
        keep_going = True
        while keep_going:
            grid_copy = copy.deepcopy(self.grid)
            self.set_neighbors()
            self.state_transition()
            if self.grid == grid_copy:
                keep_going = False
            steps += 1
        print("Simulation halted after {} steps".format(steps))

    def count_occupied(self):
        num_occupied = 0
        for _, column in self.grid.items():
            for _, seat in column.items():
                if seat.state == State.OCCUPIED:
                    num_occupied += 1
        return num_occupied


if __name__ == "__main__":
    with open("input.txt") as file:
        seats = Seats(grid=collections.defaultdict(dict))
        for y, line in enumerate(file.readlines()):
            for x, character in enumerate(line):
                if character == "L":
                    new_seat = Seat(state=State.EMPTY, x=x, y=y)
                elif character == "#":
                    new_seat = Seat(state=State.OCCUPIED, x=x, y=y)
                elif character == ".":
                    new_seat = Seat(state=State.FLOOR, x=x, y=y)
                else:
                    continue
                seats.grid[x][y] = new_seat
    seats.set_maxes()
    seats.simulate()
    print(seats.count_occupied())
