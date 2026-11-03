from collections import defaultdict
from typing import Iterable, Mapping, Sequence, Tuple
import re

def parse_input(input_: Iterable[str]) -> Mapping[int, Tuple[int, Sequence[int]]]:
    return {int(id_): (int(e), tuple(int(c) for c in cons.split(','))) for id_, e, cons in (re.match(r'id=(\d+), energy=(\d+), connections=([\d,]+)', line).groups() for line in input_)}


def part1(input_: Iterable[str]) -> int:
    start_energy = 5
    mapping = parse_input(input_)
    start = max(mapping.items(), key=lambda x: len(x[1][1]))[0]
    step = [start]
    energy = defaultdict(int)
    energy[start] = start_energy
    for impulse in range(start_energy - 1, 0, -1):
        next_step = []
        for id_ in step:
            for next_id in mapping[id_][1]:
                next_step.append(next_id)
                energy[next_id] += impulse
        step = next_step

    return sum(energy.get(id_, 0) + base_energy for id_, (base_energy, _) in mapping.items())

def part2(input_: Iterable[str]) -> int:
    start_energy = 10
    mapping = parse_input(input_)
    start = max(mapping.items(), key=lambda x: len(x[1][1]))[0]
    step = [(start, 1)]
    energy = defaultdict(int)
    energy[start] = start_energy
    for impulse in range(start_energy - 1, 0, -1):
        impulse_counts = defaultdict(int)
        for id_, n in step:
            for next_id in mapping[id_][1]:
                impulse_counts[next_id] += n
                energy[next_id] += impulse * n
        step = list(impulse_counts.items())

    return sum(energy.get(id_, 0) + base_energy for id_, (base_energy, _) in mapping.items())

def part3(input_: Iterable[str]) -> int:
    start_energy = 10
    mapping = parse_input(input_)
    limit = 1000000
    def test_cloud(start: int) -> int:
        step = [(start, (1, start_energy - 1))]
        energy = {id_: e for id_, (e, _) in mapping.items()}
        energy[start] += start_energy
        exploded = set()
        while True:
            if not step:
                break
            impulse_counts = defaultdict(lambda: defaultdict(int))
            for id_, (n, impulse) in step:
                for next_id in mapping[id_][1]:
                    if impulse > 1 and next_id not in exploded:
                        impulse_counts[next_id][impulse - 1] += n
                    energy[next_id] += impulse * n
            for id_, e in energy.items():
                if e >= limit and id_ not in exploded:
                    exploded.add(id_)
                    impulse_counts[id_][start_energy] = 1
            step = [(id_, (n, i)) for id_, counts in impulse_counts.items() for i, n in counts.items()]
        return sum(e for id_, e in energy.items() if id_ not in exploded)
    return max(test_cloud(id_) for id_ in mapping)


if __name__ == '__main__':
    with open('inputs/q7p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q7p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q7p3.txt', 'r') as fi:
        print(part3(fi))