import re
from collections import defaultdict
from typing import Iterable, Tuple, Iterator


def parse_row(row: str) -> Iterator[Tuple[str, str]]:
    return ((v1, v2) if cmp == '>' else (v2, v1) for v1, cmp, v2 in re.findall(r'(\d+)([<>])(\d+)', row))


def topological_sort(partials: Iterable[Tuple[str, str]]) -> Iterator[str]:
    outputs = defaultdict(list)
    inputs = defaultdict(int)
    for v1, v2 in partials:
        outputs[v1].append(v2)
        inputs[v2] += 1
    next_, = outputs.keys() - inputs.keys()
    while True:
        yield next_
        if next_ in outputs:
            for output in outputs[next_]:
                inputs[output] -= 1
                if inputs[output] == 0:
                    next_ = output
        else:
            break


def all_parts(inputs_: Iterable[str]) -> int:
    return sum(int(''.join(topological_sort(parse_row(row)))) for row in inputs_)


if __name__ == '__main__':
    with open('inputs/q2p1.txt', 'r') as fi:
        print(all_parts(fi))
    with open('inputs/q2p2.txt', 'r') as fi:
        print(all_parts(fi))
    with open('inputs/q2p3.txt', 'r') as fi:
        print(all_parts(fi))