from collections import deque

from search.maze_puzzle import MazePuzzle, Point


def run_bfs(maze_puzzle: MazePuzzle, current_point: Point) -> Point | None:
    queue: deque[Point] = deque([current_point])
    visited_points: set[Point] = {current_point}
    while queue:
        current_point = queue.popleft()
        neighbors: list[Point] = maze_puzzle.get_neighbors(current_point)
        for neighbor in neighbors:
            if neighbor not in visited_points:
                neighbor.parent = current_point
                queue.append(neighbor)
                visited_points.add(neighbor)

                if maze_puzzle.point_is_goal(neighbor):
                    return neighbor
    return None


def main() -> None:
    print('---Breadth-first Search---')
    maze_puzzle: MazePuzzle = MazePuzzle()
    starting_point: Point = Point(2, 2)

    outcome: Point | None = run_bfs(maze_puzzle, starting_point)
    if outcome:
        path, length, cost = maze_puzzle.get_path(outcome)
        print(f'Path Length: {length}')
        print(f'Path Cost: {cost}')
        print(' => '.join(map(str, path[::-1])))
        print(maze_puzzle.overlay_points_on_map(path))


if __name__ == '__main__':
    main()
