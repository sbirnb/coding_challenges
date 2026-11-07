import re
from functools import lru_cache
from math import ceil
from typing import Iterable, Tuple, Iterator, Sequence


def parse_input(input_: Iterable[str]) -> Iterator[Tuple[int, int, int]]:
    for line in input_:
        id_, growth, limit = re.match(r'id=(\d+), growth=(\d+), limit=(\d+)', line).groups()
        yield int(id_), int(growth), int(limit)


def iter_growth(growth: int) -> Iterator[Sequence[int]]:
    elements = [1] + [0] * (growth - 1)
    while True:
        *elements, splitting = [0, *elements]
        elements[1] += splitting
        elements[growth // 2] += 2 * splitting
        yield elements


def growth_search(growth: int, limit: int) -> int:

    @lru_cache(maxsize=None)
    def recurse(steps: int, l: int):
        if steps == 0:
            return 1
        if l == growth:
            return 2 * recurse(steps - 1, l // 2 + 1) + recurse(steps - 1, 2)
        delta = min(steps, growth - l)
        return recurse(steps - delta, l + delta)

    def get_growth(steps: int, l: int):
        return (recurse(steps, l) - 1) // 2 + 1

    def binary_search(lb: int, ub: int):
        while ub - lb > 1:
            mid = ceil((lb + ub) / 2)
            v = get_growth(mid, 1)
            if v >= limit:
                ub = mid
            else:
                lb = mid
        return ub

    def find_ub():
        steps = 1
        while get_growth(steps, 1) < limit:
            steps *= 2
        return steps
    ub = find_ub()
    steps = binary_search(ub // 2, ub)
    return steps


def part1(input_: Iterable[str]) -> int:

    def time(growth: int, limit: int) -> int:
        elements = [1] + [0] * (growth - 1)
        size = 0
        seconds = 0
        while size < limit:
            seconds += 1
            *next_elements, splitting = [0] + elements
            size += sum(elements) + splitting
            next_elements[1] += splitting
            next_elements[growth // 2] += 2 * splitting
            elements = next_elements
        return seconds

    return sum(time(growth, limit) for _, growth, limit in parse_input(input_))


def part2(input_: Iterable[str]) -> int:

    def time(growth: int, limit: int) -> int:
        leaves = 1
        for seconds, elements in enumerate(iter_growth(growth), 1):
            if leaves >= limit:
                return seconds
            leaves += elements[-1]

    return sum(time(growth, limit) for _, growth, limit in parse_input(input_))


def part3(input_: Iterable[str]) -> int:
    return sum(growth_search(growth, limit) for _, growth, limit in parse_input(input_))


if __name__ == '__main__':
    with open('inputs/q9p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q9p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q9p3.txt', 'r') as fi:
        print(part3(fi))