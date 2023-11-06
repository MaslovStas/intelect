import time
from collections import namedtuple
from itertools import product

Item = namedtuple('Item', 'name weight price')

knapsack_items: list[list[str, int, int]] = [
    ['Axe', 32252, 68674],
    ['Bronze coin', 225790, 471010],
    ['Crown', 468164, 944620],
    ['Diamond statue', 489494, 962094],
    ['Emerald belt', 35384, 78344],
    ['Fossil', 265590, 579152],
    ['Gold coin', 497911, 902698],
    ['Helmet', 800493, 1686515],
    ['Ink', 823576, 1688691],
    ['Jewel box', 552202, 1056157],
    ['Knife', 323618, 677562],
    ['Long sword', 382846, 833132],
    ['Mask', 44676, 99192],
    ['Necklace', 169738, 376418],
    ['Opal badge', 610876, 1253986],
    ['Pearls', 854190, 1853562],
    ['Quiver', 671123, 1320297],
    ['Ruby ring', 698180, 1301637],
    ['Silver bracelet', 446517, 859835],
    ['Timepiece', 909620, 1677534],
    ['Uniform', 904818, 1910501],
    ['Venom potion', 730061, 1528646],
    ['Wool scarf', 931932, 1827477],
    ['Cross bow', 952360, 2068204],
    ['Yesteryear book', 926023, 1746556],
    ['Zinc cup', 978724, 2100851]
]

items: list[Item] = [Item(name, weight, price) for name, weight, price in knapsack_items]


def fitness_value(individual: list[int], max_weight: int) -> int:
    total_weight: int = 0
    total_price: int = 0
    for i, gene in enumerate(individual):
        if gene:
            item: Item = items[i]
            total_weight += item.weight
            total_price += item.price

            if total_weight > max_weight:
                return 0
    return total_price


def brute_force():
    bit_string_size: int = len(items)
    best_price: int = 0
    best_individual: list[int] = []
    max_weight: int = 6404180
    for i, ind in enumerate(product([0, 1], repeat=bit_string_size)):
        price: int = fitness_value(ind, max_weight)
        if price > best_price:
            best_price = price
            best_individual = ind
            print('Iteration: ', i)
            print('Best score: ', best_price)
            print('Best individual: ', best_individual)

    print(best_individual)


start_time: float = time.time()
brute_force()
end_time: float = time.time()
print('total time:', end_time - start_time)