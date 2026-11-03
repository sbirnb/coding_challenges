import re
from collections import defaultdict
from itertools import groupby
from typing import Iterable, Tuple


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[int, int, int, int]]:
    for row in input_:
        yield tuple(int(v) for v in re.match(r'id=(\d+) quest=(\d+) part=(\d+) time=(\d+)', row).groups())


def part1(input_: Iterable[str]) -> int:
    times = defaultdict(int)
    for id_, _, _, time in parse_input(input_):
        times[id_] += time
    return sum(i * t for i, t in enumerate(sorted(times.values()), 1))


def part2(input_: Iterable[str]) -> int:
    times = defaultdict(lambda: [0, 0])
    for id_, _, _, time in parse_input(input_):
        participant = times[id_]
        participant[0] -= 1
        participant[1] += time
    return sum(i * t for i, (_, t) in enumerate(sorted(times.values()), 1))


def part3(input_: Iterable[str]) -> int:
    times = defaultdict(lambda: defaultdict(int))
    quests = set()
    for id_, quest, part, time in parse_input(input_):
        quests.add(quest)
        times[(quest, part)][id_] = time
    for quest in quests:
        for part in (1, 2):
            qp_times = times[(quest, part)]
            next_qp_times = times[(quest, part + 1)]
            for id_ in next_qp_times:
                next_qp_times[id_] += qp_times[id_]
    scores = defaultdict(int)
    for (quest, part), qp_times in sorted(times.items()):
        reduce = 0
        for t, ids_ in groupby(sorted(qp_times.items(), key=lambda x: x[1]), key=lambda x: x[1]):
            score = max(0, 50 * part - reduce)
            for id_, _ in ids_:
                scores[id_] += score
                reduce += 1
    checksum = 0
    coeff = 1
    for score, scores in groupby(sorted(scores.values(), key=lambda x: -x)):
        count = sum(1 for _ in scores)
        checksum += coeff * count * score
        coeff += count
    return checksum


if __name__ == '__main__':
    with open('inputs/q4p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q4p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q4p3.txt', 'r') as fi:
        print(part3(fi))