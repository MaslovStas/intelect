from __future__ import annotations

import random
from abc import ABC
from dataclasses import dataclass, field
from typing import Iterator

from swarm.utils import test_himm


@dataclass
class Abstract2DObject(ABC):
    x: float
    y: float


@dataclass
class Velocity(Abstract2DObject):

    def __add__(self, velocity: Velocity) -> Velocity:
        if not isinstance(velocity, Velocity):
            raise TypeError

        return Velocity(self.x + velocity.x, self.y + velocity.y)

    def __mul__(self, factor: float | int) -> Velocity:
        if not isinstance(factor, (float, int)):
            raise TypeError

        return Velocity(factor * self.x, factor * self.y)

    def __rmul__(self, factor: float | int) -> Velocity:
        return self.__mul__(factor)


@dataclass
class Point(Abstract2DObject):

    def __add__(self, velocity: Velocity) -> Point:
        if not isinstance(velocity, Velocity):
            raise TypeError

        return Point(self.x + velocity.x, self.y + velocity.y)

    def __sub__(self, point: Point) -> Distance:
        if not isinstance(point, Point):
            raise TypeError

        return Distance(self.x - point.x, self.y - point.y)


@dataclass
class Distance(Abstract2DObject):

    def __mul__(self, factor: float | int) -> Velocity:
        if not isinstance(factor, (float, int)):
            raise TypeError

        return Velocity(factor * self.x, factor * self.y)

    def __rmul__(self, factor: float | int) -> Velocity:
        return self.__mul__(factor)


class Particle:

    def __init__(self, location: Point, inertia: float, cognitive_const: float, social_const: float):
        self.fitness: float = 0.0
        self.best_fitness: float = float('inf')

        self.location = location
        self.best_location = location

        self._inertia = inertia
        self._cognitive_const = cognitive_const
        self._social_const = social_const

        self._velocity: Velocity = Velocity(0, 0)

    def __repr__(self):
        return f'<Particle(location={self.location}, fitness={self.fitness})>'

    def __lt__(self, other: Particle) -> bool:
        return self.fitness < other.fitness

    @property
    def location(self) -> Point:
        return self._location

    @location.setter
    def location(self, point: Point) -> None:
        if not isinstance(point, Point):
            raise TypeError

        self._location = point
        self._update_fitness()

    def _update_fitness(self) -> None:
        x, y = self.location.x, self.location.y
        self.fitness = test_himm(x, y)
        if self.fitness < self.best_fitness:
            self.best_fitness = self.fitness
            self.best_location = self.location

    def _move(self) -> None:
        self.location += self._velocity

    def _get_inertial_part(self) -> Velocity:
        return self._inertia * self._velocity

    def _get_cognitive_part(self) -> Velocity:
        cognitive_acceleration: float = self._cognitive_const * random.random()
        cognitive_distance: Distance = self.best_location - self.location
        return cognitive_acceleration * cognitive_distance

    def _get_social_part(self, swarm_best_location: Point) -> Velocity:
        social_acceleration: float = self._social_const * random.random()
        social_distance: Distance = swarm_best_location - self.location
        return social_acceleration * social_distance

    def _get_updated_velocity(self, swarm_best_location: Point) -> Velocity:
        return self._get_inertial_part() + self._get_cognitive_part() + self._get_social_part(swarm_best_location)

    def _update_velocity(self, swarm_best_location: Point) -> None:
        self._velocity = self._get_updated_velocity(swarm_best_location)

    def move_with_swarm(self, swarm_best_location: Point) -> None:
        self._update_velocity(swarm_best_location)
        self._move()


@dataclass
class Swarm:
    inertia: float
    cognitive_const: float
    social_const: float

    number_of_particles: int
    number_of_iterations: int
    value_limit: tuple[float, float]

    population: list[Particle] = field(init=False)
    best_location: Point = field(init=False)
    best_fitness: float = field(init=False)

    def __iter__(self) -> Iterator:
        return iter(self.population)

    def __post_init__(self) -> None:
        self._create_population()

        best_particle: Particle = min(self.population)
        self.best_location = best_particle.location
        self.best_fitness = best_particle.fitness

    def _create_population(self) -> None:
        left, right = self.value_limit
        self.population = [Particle(Point(random.uniform(left, right), random.uniform(left, right)),
                                    self.inertia, self.cognitive_const, self.social_const)
                           for _ in range(self.number_of_particles)]

    def move(self) -> None:
        for particle in self.population:
            particle.move_with_swarm(self.best_location)

            if particle.fitness < self.best_fitness:
                self.best_location = particle.location
                self.best_fitness = particle.fitness

    def search(self) -> None:
        for iteration in range(self.number_of_iterations):
            self.move()

            print(f'{iteration + 1}-> {self.best_location} = {self.best_fitness}')


if __name__ == '__main__':
    swarm: Swarm = Swarm(inertia=0.4,
                         cognitive_const=0.3,
                         social_const=0.7,
                         number_of_particles=15,
                         number_of_iterations=50,
                         value_limit=(-5, 5))
    swarm.search()
