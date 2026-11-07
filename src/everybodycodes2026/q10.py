from collections import defaultdict
from itertools import count, chain
from typing import Set, Iterable, Tuple, Mapping, Sequence, Optional

DIRS = {c: pow(1j, i) for i, c in enumerate('v>^<')}
def parse_input(input_: Iterable[str]) -> Tuple[Set[complex], Mapping[complex, Mapping[complex, Sequence[int]]]]:
    walls = set()
    ghosts = defaultdict(lambda: defaultdict(list))
    ghost_counter = count()
    for row, cells in enumerate(input_):
        for col, cell in enumerate(cells.strip()):
            pos = row + 1j * col
            if cell == '#':
                walls.add(pos)
            elif cell in DIRS:
                ghosts[pos][DIRS[cell]].append(next(ghost_counter))
    return walls, ghosts

def advance(walls: Set[complex], ghosts: Mapping[complex, Mapping[complex, Sequence[int]]]) -> Tuple[Mapping[int, int], Mapping[complex, Sequence[int]]]:
    collisions = defaultdict(int)
    new_ghosts = defaultdict(lambda: defaultdict(list))
    for cell, cell_ghosts in ghosts.items():
        for ghost, ids in cell_ghosts.items():
            if len(ids) == 0:
                continue
            next_pos = cell + ghost
            if next_pos in walls:
                new_ghosts[cell][ghost * -1j].extend(ids)
                for id_ in ids:
                    collisions[id_] += 1
            else:
                new_ghosts[next_pos][ghost].extend(ids)
    for cell, cell_ghosts in tuple(new_ghosts.items()):
        if sum(len(ids) for ids in cell_ghosts.values()) > 1:
            for id_ in chain.from_iterable(cell_ghosts.values()):
                collisions[id_] += 1
            for d in (1, 1j):
                cell_ghosts[d], cell_ghosts[-d] = cell_ghosts[-d], cell_ghosts[d]
    return collisions, new_ghosts



def part1(input_: Iterable[str]) -> int:

    walls, ghosts = parse_input(input_)

    collisions = 0
    for _ in range(10):
        c, ghosts = advance(walls, ghosts)
        collisions += sum(c.values())
    return collisions


def part2(input_: Iterable[str], c_limit: int) -> int:
    walls, ghosts = parse_input(input_)
    collisions = {id_[0]: 0 for id_ in chain.from_iterable(c.values() for c in ghosts.values())}
    for t in count(1):
        new_ghosts = defaultdict(lambda: defaultdict(list))
        for cell, cell_ghosts in ghosts.items():
            for ghost, ids in cell_ghosts.items():
                if len(ids) == 0:
                    continue
                next_pos = cell + ghost
                if next_pos in walls:
                    for id_ in ids:
                        collisions[id_] += 1
                        if collisions[id_] < c_limit:
                            new_ghosts[cell][ghost * -1j].append(id_)
                        else:
                            del collisions[id_]
                else:
                    new_ghosts[next_pos][ghost].extend(ids)
        for cell, cell_ghosts in tuple(new_ghosts.items()):
            if sum(len(ids) for ids in cell_ghosts.values()) > 1:
                for d, ids in cell_ghosts.items():
                    for id_ in tuple(ids):
                        collisions[id_] += 1
                        if collisions[id_] >= c_limit:
                            ids.remove(id_)
                            del collisions[id_]
                for d in (1, 1j):
                    cell_ghosts[d], cell_ghosts[-d] = cell_ghosts[-d], cell_ghosts[d]
        ghosts = new_ghosts
        if len(collisions) == 0:
            return t

def part3(input_: Iterable[str], c_limit: int) -> int:
    walls, ghosts = parse_input(input_)

    def advance(
            states,
            collisions
    ):
        new_collisions = dict(collisions)
        new_states = dict()
        inverted = defaultdict(list)
        for id_, (pos, dir_) in states.items():
            forward_pos = pos + dir_
            delete = False
            if forward_pos in walls:
                new_pos, new_dir = pos, dir_ * -1j
                new_collisions[id_] += 1
                if new_collisions[id_] >= c_limit:
                    delete = True
            else:
                new_pos, new_dir = forward_pos, dir_
            if not delete:
                new_states[id_] = new_pos, new_dir
                inverted[new_pos].append(id_)
        for ids in inverted.values():
            if len(ids) <= 1:
                continue
            for id_ in ids:
                new_collisions[id_] += 1
                if new_collisions[id_] >= c_limit:
                    del new_states[id_]
                else:
                    pos, dir_ = new_states[id_]
                    new_states[id_] = pos, -dir_
        return new_states, new_collisions


    states = dict()
    for pos, pos_map in ghosts.items():
        for dir_, ids in pos_map.items():
            for id_ in ids:
                states[id_] = pos, dir_
    collisions = {id_: 0 for id_ in range(len(states))}

    cache = dict()

    t = 0
    ghosts_count = len(states)
    while ghosts_count > 0:

        states, collisions = advance(states, collisions)
        t += 1
        if len(states) < ghosts_count:
            ghosts_count = len(states)
            cache.clear()
        states_key = tuple(sorted(states.items()))
        if states_key not in cache:
            cache[states_key] = t, collisions
            continue

        t0, collisions0 = cache[states_key]
        dt = t - t0
        d_collisions = {id_: d_c for id_, c0 in collisions0.items() if (d_c := collisions[id_] - c0) > 0}
        max_cycles = max(0, min((c_limit - 1 - collisions[id_]) // d_c for id_, d_c in d_collisions.items()))
        for id_, d_c in d_collisions.items():
            collisions[id_] += max_cycles * d_c
        t += max_cycles * dt
    return t



if __name__ == '__main__':
    with open('inputs/q10p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q10p2.txt', 'r') as fi:
        print(part2(fi, 10000))
    with open('inputs/q10p3.txt', 'r') as fi:
        print(part3(fi, 1000000000000))