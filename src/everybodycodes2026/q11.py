from collections import defaultdict
from typing import Tuple, Iterator, Sequence, Mapping, Iterable, Set, FrozenSet
import re
from itertools import combinations


def parse_input(input_: Iterator[str]) -> Tuple[int, Iterator[Tuple[int, int]]]:
    portals = int(re.search(r'(?<=portals: ).*', next(input_)).group())
    return portals, (tuple(pid if (pid := int(p)) < portals else 0 for p in line.strip().split(' ')) for line in input_ if line.strip())


def get_adjacent(p: int, c: int, adjacencies: Mapping[int, Sequence[int]], portals: int) -> Iterator[int]:
    for d in range(1, c + 1):
        yield (p + d) % portals
        yield (p - d) % portals
    yield from adjacencies.get(p, tuple())


def get_dists_from(start: int, c: int, adjacencies: Mapping[int, Sequence[int]], portals: int) -> Iterable[Tuple[int, int]]:
    queue = [(start, 0)]
    seen = {start}
    while queue:
        portal, dist = queue.pop(0)
        for adj_p in get_adjacent(portal, c, adjacencies, portals):
            if adj_p not in seen:
                seen.add(adj_p)
                queue.append((adj_p, dist + 1))
                yield adj_p, dist + 1


def part1(input_: Iterator[str]) -> int:
    portals, connections = parse_input(input_)
    adjacencies = defaultdict(list)
    for p1, p2 in connections:
        adjacencies[p1].append(p2)
        adjacencies[p2].append(p1)


    def get_dists_from_nojumps() -> int:
        longest = portals // 2
        if portals % 2 == 0:
            return ((longest - 1) * longest) + longest
        else:
            return (longest + 1) * longest

    dist_total = sum(sum(dist for _, dist in get_dists_from(start, 1, adjacencies, portals)) for start in range(portals))
    dist_total_nojumps = portals * get_dists_from_nojumps()

    return dist_total_nojumps - dist_total


def part2(input_: Iterator[str]) -> int:
    portals, connections = parse_input(input_)
    adjacencies = defaultdict(list)

    for p1, p2 in connections:
        adjacencies[p1].append(p2)
        adjacencies[p2].append(p1)

    def get_dist_with_jump(start: int, end: int, distances: Mapping[FrozenSet[int], int], extra: Tuple[int, int]) -> int:
        return min(
            distances[frozenset((start, end))],
            1 + distances[frozenset((start, extra[0]))] + distances[frozenset((extra[1], end))],
            1 + distances[frozenset((start, extra[1]))] + distances[frozenset((extra[0], end))],
        )

    base_distances = {
        **{frozenset((p,)): 0 for p in range(portals)},
        **{frozenset((start, end)): dist for start in range(portals) for end, dist in get_dists_from(start, 3, adjacencies, portals)}
    }
    return portals * sum(dist for _, dist in get_dists_from(1, 3, dict(), portals)) - \
        2 * min(sum(get_dist_with_jump(start, end, base_distances, extra) for start, end in combinations(range(portals), 2)) for extra in combinations(range(portals), 2))


def part3(input_: Iterable[str]) -> int:
    portals, connections = parse_input(input_)
    adjacencies = defaultdict(list)

    for p1, p2 in connections:
        adjacencies[p1].append(p2)
        adjacencies[p2].append(p1)

    def get_portal_pairs(n: int) -> Iterator[Sequence[Tuple[int, int]]]:

        def recurse(next_portal: int, edges: Sequence[Tuple[int, int]], seen: Set[int]) -> Iterator[
            Sequence[Tuple[int, int]]]:
            for tail in range(next_portal + 1, n):
                if tail not in seen:
                    try:
                        yield from recurse(
                            next(h2 for h2 in range(next_portal + 1, n) if h2 not in seen and h2 != tail),
                            (*edges, (next_portal, tail)), {*seen, next_portal, tail})
                    except StopIteration:
                        yield *edges, (next_portal, tail)

        return recurse(0, tuple(), set())

    min_dists = float('inf')
    segment_sizes = portals // 8
    for offset in range(segment_sizes):
        for pairs in get_portal_pairs(8):
            ext_adjacencies = defaultdict(list, {k: list(v) for k, v in adjacencies.items()})
            for p1, p2 in ((offset + p * segment_sizes, offset + q * segment_sizes) for p, q in pairs):
                ext_adjacencies[p1].append(p2)
                ext_adjacencies[p2].append(p1)
            dists = sum(sum(dist for _, dist in get_dists_from(start, 3, ext_adjacencies, portals)) for start in range(portals))
            min_dists = min(min_dists, dists)
    return portals * sum(dist for _, dist in get_dists_from(1, 3, dict(), portals)) - min_dists


if __name__ == '__main__':
    with open('inputs/q11p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q11p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q11p3.txt', 'r') as fi:
        print(part3(fi))