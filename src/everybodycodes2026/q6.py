from collections import defaultdict
from typing import Iterable, Sequence, Mapping, Collection
import re


def parse_input(input_: Iterable[str]) -> Mapping[str, Sequence[str]]:
    return {item: recipe for item, *recipe in (re.findall(r'\w+', row) for row in input_)}


def traverse_recipes(
        recipes: Mapping[str, Sequence[str]],
        source: str
) -> Collection[str]:
    seen = {source}
    queue = [source]
    while queue:
        item = queue.pop(0)
        recipe = recipes.get(item, tuple())
        for ingredient in recipe:
            if ingredient not in seen:
                seen.add(ingredient)
                queue.append(ingredient)
    return seen


def part1(input_: Iterable[str]) -> int:
    recipes = parse_input(input_)
    return len(traverse_recipes(recipes, 'NULL')) - 1


def part2(input_: Iterable[str]) -> int:
    recipes = parse_input(input_)
    inverted = defaultdict(list)
    for item, ingredients in recipes.items():
        for ingredient in ingredients:
            inverted[ingredient].append(item)
    return len(traverse_recipes(inverted, 'NULL')) - 1


def part3(input_: Iterable[str]) -> int:
    recipes = parse_input(input_)
    inverted = defaultdict(list)
    for item, ingredients in recipes.items():
        for ingredient in ingredients:
            inverted[ingredient].append(item)
    null1 = set(traverse_recipes(inverted, 'NULLv1'))
    null2 = set(traverse_recipes(inverted, 'NULLv2'))
    null3 = set(traverse_recipes(inverted, 'NULLv3'))
    return len((null1 & null2) | (null1 & null3) | (null2 & null3))


if __name__ == '__main__':
    with open('inputs/q6p1.txt', 'r') as fi:
        print(part1(fi))
    with open('inputs/q6p2.txt', 'r') as fi:
        print(part2(fi))
    with open('inputs/q6p3.txt', 'r') as fi:
        print(part3(fi))