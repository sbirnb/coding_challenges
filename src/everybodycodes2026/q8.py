from collections import defaultdict
from itertools import count, takewhile, cycle
from typing import Iterable, Dict

DIRS = (1 + 1j, 1 - 1j, -2j, -1 - 1j, -1 + 1j, 2j)


def parse_input(input_: Iterable[str]) -> Dict[complex, int]:
    return {row + 1j * col: int(h) for row, cells in enumerate(input_) for col, h in enumerate(cells.strip()) if h != '.'}


def get_line(cell: complex, map_: Dict[complex, int], dir_: complex) -> Iterable[complex]:
    return takewhile(map_.__contains__, (cell + dir_ * i for i in count()))


def iter_line(cell: complex, map_: Dict[complex, int], dir_: complex) -> Iterable[complex]:
    h = 0
    for tree in get_line(cell, map_, dir_):
        if map_[tree] != -1 and map_[tree] > h:
            yield tree
            h = map_[tree]
        h -= 1


def count_line(cell: complex, map_: Dict[complex, int], dir_: complex) -> int:
    return sum(1 for _ in iter_line(cell, map_, dir_))


def part1(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    col0 = next(col for col in count() if 1j * col in map_)
    return sum(count_line(cell, map_, 1 + 1j) for cell in get_line(col0 * 1j, map_, 1 - 1j)) + \
        sum(count_line(cell, map_, 1 + 1j) for cell in get_line(col0 * 1j + 2j, map_, 2j))


def part2(input_: Iterable[str]) -> int:
    total = 0
    map_ = parse_input(input_)
    for cell in map_:
        for dir_ in DIRS:
            if cell - dir_ not in map_:
                total += count_line(cell, map_, dir_)
    return total


def part3(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    lines = defaultdict(list)
    growth = [[], [], [], []]
    for cell in map_:
        for dir_ in DIRS:
            if cell - dir_ not in map_:
                lines[dir_].append(cell)

    def update(dir_: complex):
        for cell in growth.pop(0):
            map_[cell] = 1
        new_growths = []
        e = 0
        for c0 in lines[dir_]:
            for cell in tuple(iter_line(c0, map_, dir_)):
                map_[cell] += 1
                e += 1
                if map_[cell] > 9:
                    map_[cell] = -1
                    new_growths.append(cell)
        growth.append(new_growths)
        return len(new_growths), e

    size = 0
    e_total = 0
    for dir_ in cycle(DIRS):
        ng, e = update(dir_)
        size += ng
        e_total += e
        if size >= 100000:
            return e_total


if __name__ == '__main__':
    with open('inputs/q8p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q8p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q8p3.txt', 'r') as fi:
        print(part3(fi))