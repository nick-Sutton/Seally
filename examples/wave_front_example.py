from seally.env.grid_map import GridMap, GridCell
from seally.planners.wave_front import WaveFront
from seally.viz.vizualizer import Visualizer2D

def main():
    # Create an enviroment from a map file
    env: GridMap = GridMap(gen_random=False, file_path='./maps/map7.csv', move_4d = False)

    # Create a planner and pass in the heuristic
    wave_front = WaveFront(env)

    # Define the source and goal positions
    source = GridCell((1, 0))
    goal = GridCell((26, 26))

    # Find the shortest path from the start to the goal
    path = wave_front.compute_path(source, goal)

    # Visualize the path
    viz = Visualizer2D()
    viz.run_visualization(path, env)


if __name__ == "__main__":
    main()