from collections import defaultdict
from typing import Dict, Iterable, Iterator, Set


def parse_input(input_: Iterable[str]) -> Dict[complex, int]:
    return {row + 1j * col: int(cell == '1') for row, cells in enumerate(input_) for col, cell in enumerate(cells.strip())}


def adjacent(cell: complex) -> Iterable[complex]:
    return (cell + 1, cell - 1, cell + 1j, cell - 1j, cell + 1 - 1j, cell + 1 + 1j, cell - 1 - 1j, cell - 1 + 1j)


def get_land(map_: Dict[complex, int]) -> Iterator[complex]:
    height = int(max(coord.real for coord in map_))
    width = int(max(coord.imag for coord in map_))
    center = height / 2 + 1j * width / 2
    queue = [center]
    adj_counts = {center: 10}
    landsize = 0
    while queue:
        landsize += 1
        cell = queue.pop(0)
        yield cell
        was_light = map_[cell] == 0
        for acell in adjacent(cell):
            if acell not in map_:
                continue
            if acell not in adj_counts:
                adj_counts[acell] = sum(map_.get(aacell, 0) == 1 for aacell in adjacent(acell))
                if adj_counts[acell] >= 5:
                    queue.append(acell)
            if was_light:
                adj_counts[acell] += 1
                if adj_counts[acell] == 5:
                    queue.append(acell)

def get_sand(land: Set[complex]) -> Iterator[complex]:
    queue = [cell for cell in land if not all(acell in land for acell in adjacent(cell))]
    adj_counts = defaultdict(int)
    for cell in queue:
        adj_counts[cell] = 10
    sand_size = 0
    while queue:
        sand_size += 1
        cell = queue.pop(0)
        yield cell
        for acell in adjacent(cell):
            if acell not in land:
                continue
            adj_counts[acell] += 1
            if adj_counts[acell] == 5:
                queue.append(acell)


def tree_near_cells(cell: complex) -> Iterator[complex]:
    yield from adjacent(cell)
    for offset in range(-1, 2):
        yield cell + 2 + 1j * offset
        yield cell - 2 + 1j * offset
        yield cell + 2j + offset
        yield cell - 2j + offset


def get_trees(land: Set[complex]) -> Iterator[complex]:
    return (cell for cell in land if all(ncell in land for ncell in tree_near_cells(cell)))


def grow_trees(land: Set[complex], trees: Set[complex]) -> Iterator[complex]:
    return (
        tree for tree in land
        if
            (tree not in trees)
            and (all(acell in land for acell in adjacent(tree)))
            and (sum(acell in trees for acell in adjacent(tree)) >= 4)
    )


def part1(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    return sum(1 for _ in get_land(map_))


def part2(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    land = set(get_land(map_))
    return sum(1 for _ in get_sand(land))


def part3(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    land = set(get_land(map_))
    sand = set(get_sand(land))
    land -= sand
    trees = set(get_trees(land))
    trees.update(tuple(grow_trees(land, trees)))
    trees.update(tuple(grow_trees(land, trees)))

    return len(trees)


if __name__ == '__main__':
    with open('inputs/q5p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q5p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q5p3.txt', 'r') as fi:
        print(part3(fi))