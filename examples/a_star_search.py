from seally.common.path import Path
from seally.common.heuristics import chebyshev_distance
from seally.env.grid_map import GridMap, GridCell
from seally.planners.a_star import AStar
from seally.viz.vizualizer import Visualizer2D

def main():
    # Create an enviroment from a map file
    env: GridMap = GridMap(False, './maps/map2.csv')

    # Create a planner and pass in the heuristic
    a_star = AStar(env, chebyshev_distance)

    # Define the source and goal positions
    source = GridCell(0, 4)
    goal = GridCell(11, 2)

    # Find the shortest path from the start to the goal
    path: Path = a_star.compute_path(source, goal)

    # Visualize the path
    viz = Visualizer2D(screen_size=(env.x_dim, env.y_dim))
    viz.run_visualization(path, env)


if __name__ == "__main__":
    main()