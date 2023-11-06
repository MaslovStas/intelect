import heapq
from search.maze_puzzle import MazePuzzle, Point


def run_astar(maze_puzzle: MazePuzzle, current_point: Point) -> Point | None:
    queue: list[Point] = [current_point]
    visited_points: set[Point] = set()
    while queue:
        current_point = heapq.heappop(queue)
        if current_point not in visited_points:
            visited_points.add(current_point)

            if maze_puzzle.point_is_goal(current_point):
                return current_point

            neighbors: list[Point] = maze_puzzle.get_neighbors(current_point)
            for neighbor in neighbors:
                neighbor.parent = current_point
                neighbor.cost = maze_puzzle.determine_cost(current_point, neighbor)
                heapq.heappush(queue, neighbor)

    return None


def main() -> None:
    print('---A-* Search---')
    maze_puzzle: MazePuzzle = MazePuzzle()
    starting_point: Point = Point(2, 2)

    outcome: Point | None = run_astar(maze_puzzle, starting_point)
    if outcome:
        path, length, cost = maze_puzzle.get_path(outcome)
        print(f'Path Length: {length}')
        print(f'Path Cost: {cost}')
        print(' => '.join(map(str, path[::-1])))
        print(maze_puzzle.overlay_points_on_map(path))


if __name__ == '__main__':
    main()
