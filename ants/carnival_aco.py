import csv
import random

ATTRACTION_COUNT: int = 48
RANDOM_ATTRACTION_FACTOR: float = 0.0
ALPHA: int = 1
BETA: int = 4

file_name: str = f'attractions-{ATTRACTION_COUNT}.csv'
with open(file_name) as file:
    attraction_distances: list[list[int]] = [list(map(int, row)) for row in csv.reader(file)]


class Ant:
    def __init__(self) -> None:
        self.visited_attractions: list[int] = []
        self.visited_attractions.append(random.randint(0, ATTRACTION_COUNT - 1))

    @property
    def distance_travelled(self) -> int:
        distance: int = 0
        for i in range(len(self.visited_attractions) - 1):
            curr_attr, next_attr = self.visited_attractions[i:i + 2]
            distance += attraction_distances[curr_attr][next_attr]
        return distance

    @property
    def possible_attractions(self) -> list[int]:
        all_attractions: set[int] = set(range(ATTRACTION_COUNT))
        return list(all_attractions - set(self.visited_attractions))

    def visit_attraction(self, pheromone_trails: list[list[float]]) -> None:
        if random.random() < RANDOM_ATTRACTION_FACTOR:
            self.visit_random_attraction()
        else:
            self.visit_probabilistic_attraction(pheromone_trails)

    def visit_random_attraction(self) -> None:
        next_attr: int = self.get_random_attraction()
        self.visited_attractions.append(next_attr)

    def visit_probabilistic_attraction(self, pheromone_trails: list[list[float]]) -> None:
        probabilities: list[tuple[int, float]] = self.get_probabilities_attractions(pheromone_trails)
        next_attr: int = self.roulette_wheel_selection(probabilities)
        self.visited_attractions.append(next_attr)

    def get_random_attraction(self) -> int:
        next_attr: int = random.choice(self.possible_attractions)
        return next_attr

    def get_probabilities_attractions(self, pheromone_trails: list[list[float]]) -> list[tuple[int, float]]:
        curr_attr: int = self.visited_attractions[-1]
        heuristics: list[tuple[int, float]] = []
        total_heuristics: float = 0
        for attr in self.possible_attractions:
            heuristic_for_pheromones: float = pheromone_trails[curr_attr][attr] ** ALPHA
            heuristic_for_path: int = attraction_distances[curr_attr][attr] ** BETA
            heuristic: float = heuristic_for_pheromones / heuristic_for_path
            heuristics.append((attr, heuristic))
            total_heuristics += heuristic

        probabilities: list[tuple[int, float]] = [(attr, heuristic / total_heuristics)
                                                  for attr, heuristic in heuristics]
        return probabilities

    @staticmethod
    def roulette_wheel_selection(probabilities: list[tuple[int, float]]) -> int:
        total_probability: float = 0
        slices: list[tuple[int, float, float]] = []
        for attr, probability in probabilities:
            slices.append((attr, total_probability, total_probability + probability))
            total_probability += probability

        spin: float = random.random()
        for attr, left_border, right_border in slices:
            if left_border <= spin < right_border:
                return attr
        return -1

    def __str__(self):
        return (f'Ant, {id(self)}\n'
                f'Total attractions: {len(self.visited_attractions)}\n'
                f'Total distance: {self.distance_travelled}\n')


class ACO:
    def __init__(self, number_of_ants_factor: float) -> None:
        self.number_of_ants_factor = number_of_ants_factor
        self.ant_colony: list[Ant] = []
        self.pheromone_trails: list[list[float]] = []
        self.best_distance: float = float('inf')
        self.best_ant: Ant | None = None

    def setup_ants(self) -> None:
        number_of_ants: int = round(self.number_of_ants_factor * ATTRACTION_COUNT)
        self.ant_colony = [Ant() for _ in range(number_of_ants)]

    def move_ants(self) -> None:
        for ant in self.ant_colony:
            ant.visit_attraction(self.pheromone_trails)

    def get_best_ant(self) -> Ant | None:
        for ant in self.ant_colony:
            if ant.distance_travelled < self.best_distance:
                self.best_ant, self.best_distance = ant, ant.distance_travelled
        return self.best_ant

    def update_pheromones(self, evaporation: float) -> None:
        self.pheromone_trails = list(map(lambda row: list(map(lambda x: x * evaporation, row)), self.pheromone_trails))

        for ant in self.ant_colony:
            ant_fitness: float = 1 / ant.distance_travelled
            for i in range(len(ant.visited_attractions) - 1):
                curr_attr, next_attr = ant.visited_attractions[i:i + 2]
                self.pheromone_trails[curr_attr][next_attr] += ant_fitness
                self.pheromone_trails[next_attr][curr_attr] += ant_fitness

    def __call__(self, total_iterations: int, evaporation: float):
        self.pheromone_trails = [[1] * ATTRACTION_COUNT for _ in range(ATTRACTION_COUNT)]
        for iteration in range(total_iterations):
            self.setup_ants()

            for _ in range(ATTRACTION_COUNT):
                self.move_ants()

            self.update_pheromones(evaporation)
            best_ant: Ant | None = self.get_best_ant()
            if best_ant:
                print(f'{iteration + 1} -> Best distance: {best_ant.distance_travelled}')


NUMBER_OF_ANTS_FACTOR: float = 0.7
TOTAL_ITERATIONS: int = 1000
EVAPORATION_RATE: float = 0.9

aco = ACO(NUMBER_OF_ANTS_FACTOR)
aco(TOTAL_ITERATIONS, EVAPORATION_RATE)
