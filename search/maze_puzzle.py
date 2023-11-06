from __future__ import annotations

import copy
from enum import Enum


class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x
        self.y: int = y
        self.parent: Point | None = None
        self.cost: float = float('inf')

    def __add__(self, other: Point) -> Point:
        return self.__class__(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return self.__class__(x=self.x - other.x, y=self.y - other.y)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(x={self.x}, y={self.y})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.cost < other.cost


class CostMove(Enum):
    STANDARD: int = 1
    GRAVITY: int = 5


class MazePuzzle:
    WALL: str = '#'
    EMPTY: str = '_'
    GOAL: str = '*'

    DIRECTIONS = {Point(0, 1): 'NORTH',
                  Point(0, -1): 'SOUTH',
                  Point(1, 0): 'EAST',
                  Point(-1, 0): 'WEST'}

    def __init__(self) -> None:
        self.maze: list[str] = ['*0000',
                                '0###0',
                                '0#0#0',
                                '0#000',
                                '00000']

    def __str__(self) -> str:
        return '\n'.join(self.maze)

    def __getitem__(self, point: Point) -> str:
        return self.maze[point.x][point.y]

    def get_neighbors(self, current_point: Point) -> list[Point]:
        neighbors: list[Point] = []
        for direction in self.DIRECTIONS:
            target_point: Point = current_point + direction
            try:
                if self[target_point] != self.WALL:
                    neighbors.append(target_point)
            except IndexError:
                pass
        return neighbors

    def point_is_goal(self, point: Point) -> bool:
        return self[point] == self.GOAL

    def overlay_points_on_map(self, points: list[Point]) -> str:
        overlay_map: list[str] = copy.deepcopy(self.maze)
        for point in points:
            old_row: str = overlay_map[point.x]
            overlay_map[point.x] = old_row[:point.y] + 'X' + old_row[point.y + 1:]
        return '\n'.join(overlay_map)

    def get_path(self, point: Point) -> tuple[list[Point], int, float]:
        path: list[Point] = []
        total_length: int = 0
        total_cost: float = 0
        while point.parent:
            path.append(point)
            total_length += 1
            total_cost += self.get_move_cost(point.parent, point)
            point = point.parent
        return path, total_length, total_cost

    def get_move_cost(self, origin: Point, target: Point) -> int:
        move: Point = target - origin
        direction: str = self.DIRECTIONS[move]
        return CostMove.GRAVITY.value if direction in ('NORTH', 'SOUTH') else CostMove.STANDARD.value

    def determine_cost(self, origin: Point, target: Point) -> int:
        cost: int = self.get_move_cost(origin, target)
        _, distance_to_root, _ = self.get_path(target)
        return distance_to_root + cost
