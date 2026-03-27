from seally.common.heuristics import chebyshev_distance
from seally.env.gridmap import GridMap
from seally.planners.a_star import AStar
from seally.viz.vizualizer import InteractiveVisualizer2D

def main():
    # Create an enviroment from a map file
    env: GridMap = GridMap(False, './maps/map1.csv')

    # Create a planner and pass in the heuristic
    a_star = AStar(env, chebyshev_distance)

    # Visualize the path
    viz = InteractiveVisualizer2D(planner=a_star)
    viz.run_visualization(env)


if __name__ == "__main__":
    main()