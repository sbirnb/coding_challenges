from typing import Iterator, Tuple, Sequence, List
import re
from itertools import cycle
from math import ceil, floor


def parse_vote(vote: str) -> Tuple[Iterator[int], Iterator[int]]:
    return tuple((int(v) for v in seq) for seq in re.match(r'ISO-(\d+) (\d+)', vote).groups())


def part1(votes: Iterator[str]) -> int:
    return sum(sum(b * pow(a, 3 - i) for i, (a, b) in enumerate(zip(*parse_vote(vote)))) for vote in votes)


def part2(votes: Iterator[str]) -> int:
    def solve_vote(seq1: Sequence[int], seq2: Sequence[int]) -> int:
        return sum(b * pow(a, i) for i, (a, b) in enumerate(zip(cycle(reversed(seq1)), reversed(seq2))))
    return sum(solve_vote(tuple(seq1), tuple(seq2)) for seq1, seq2 in (parse_vote(vote) for vote in votes))


def part3(votes: Iterator[str]) -> int:

    def get_lowerbound(
            target: int,
            coeffs: Sequence[int],
    ) -> List[int]:
        total = 0
        vals = [0] * len(coeffs)
        index = len(coeffs) - 1
        while total < target:
            vals[index] = min(9, ceil((target - total) / coeffs[index]))
            total += coeffs[index] * vals[index]
            if total > target:
                for index2 in range(index + 1, len(coeffs)):
                    delta = min(vals[index2], floor((total - target) / coeffs[index2]))
                    total -= delta * coeffs[index2]
                    vals[index2] -= delta
            index -= 1
        return vals

    def increment(vals: List[int]):
        vals[-1] += 1
        for i in range(len(vals) - 1, 0, -1):
            if vals[i] > 9:
                vals[i - 1] += vals[i] - 9
                vals[i] -= 10
            else:
                break
        return vals


    def is_valid(vote: str):
        s1, vals = ([int(d) for d in s] for s in re.match(r'ISO2-(\d+) (\d+)', vote).groups())
        coeffs = []
        s1_iter = cycle(reversed(s1))
        while len(coeffs) < len(vals):
            coeffs.insert(0, pow(next(s1_iter), len(coeffs)))
        target = sum(v * c for v, c in zip(vals, coeffs))
        test = get_lowerbound(target, coeffs)
        while test != vals:
            if sum(v * c for v, c in zip(test, coeffs)) == target:
                return 0
            increment(test)
        return target
    return sum(is_valid(vote) for vote in votes)


if __name__ == '__main__':
    with open('inputs/q3p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q3p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q3p3.txt', 'r') as fi:
        print(part3(fi))
