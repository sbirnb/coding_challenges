from math import ceil
from typing import Iterable


def parse_input(input_: str) -> Iterable[int]:
    return (int(i) for i in input_.strip().split(','))


def part1(input_: str):
    return sum(pow(ceil(pow(pinecones, .5)), 2) - pinecones for pinecones in parse_input(input_))


def part2(input_: str):
    return sum( (max(ceil(pinecones / 4), 2)) * 4 - pinecones for pinecones in parse_input(input_))


def part3(input_: str):
    return sum(max(pow((v := ceil(pow(pinecones + 1, .5))) + (1 - v&1), 2) - 1, 8) - pinecones for pinecones in parse_input(input_))


if __name__ == '__main__':
    with open('inputs/q1p1.txt') as fi:
        print(part1(fi.read()))
    with open('inputs/q1p2.txt') as fi:
        print(part2(fi.read()))
    with open('inputs/q1p3.txt') as fi:
        print(part3(fi.read()))
