from room import Room
from player import Player
from world import World

from graph import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = 'maps/test_loop_fork2.txt'
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# ------------------------------------------------------------------------

# # Single Trial

# # Instantiate Graph object
# traversal_graph = Graph(player)

# # Until the traversal graph matches the maze in size, run BFS algorithm to find nearest unexplored room, then run recursive DFT algorithm to traverse
# while len(traversal_graph.rooms) < len(room_graph):
#     traversal_graph.bfs()
#     traversal_graph.dft_recursive()

# # Replace traversal_path variable with traversal_path attribute in graph object
# traversal_path = traversal_graph.traversal_path

# ------------------------------------------------------------------------

# Multiple Trials

generated_paths = []

for i in range(700):
    player = Player(world.starting_room)
    traversal_graph = Graph(player)

    while len(traversal_graph.rooms) < len(room_graph):
        traversal_graph.bfs()
        traversal_graph.dft_recursive()

    generated_paths.append(traversal_graph.traversal_path)

shortest_path = generated_paths[0]
shortest_length = len(generated_paths[0])
for path in generated_paths:
    if len(path) < shortest_length:
        shortest_path = path
        shortest_length = len(shortest_path)

traversal_path = shortest_path

# ------------------------------------------------------------------------

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
