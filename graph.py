from utils import Queue


class Graph():
    def __init__(self, player):
        self.rooms = {}
        self.player = player
        self.traversal_path = []

    # Add a room (vertex) to graph
    def add_room(self, room_id, exits):
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
            for exit in exits:
                self.rooms[room_id][exit] = '?'

    # Add directed exits (edges) to graph
    def add_exits(self, room1, room2, direction):
        opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        if room1 in self.rooms and room2 in self.rooms:
            self.rooms[room1][direction] = room2
            self.rooms[room2][opposite_direction[direction]] = room1
        else:
            raise IndexError('That room does not exist!')

    # Get all exits (edges) of a room (vertex)
    def get_exits(self, room_id):
        return self.rooms[room_id]

    # Navigate to next room and update graph
    def take_exit(self, direction):
        room_leaving = self.player.current_room
        self.player.travel(direction)
        self.traversal_path.append(direction)
        new_room = self.player.current_room
        self.add_room(new_room.id, new_room.get_exits())
        self.add_exits(room_leaving.id, new_room.id, direction)
        return new_room

    # Navigate to each room in depth-first order beginning from starting room, done using recursion
    def dft_recursive(self, starting_room=None, finished=None):
        starting_room = starting_room or self.player.current_room
        finished = finished or set()

        if starting_room not in finished:
            self.add_room(starting_room.id, starting_room.get_exits())

            current_room_id = starting_room.id
            current_exits = self.get_exits(current_room_id)

            d1 = 's'
            d2 = 'w'
            d3 = 'n'
            d4 = 'e'

            if d1 in current_exits and current_exits[d1] == '?':
                new_room = self.take_exit(d1)
                self.dft_recursive(new_room, finished)
            elif d2 in current_exits and current_exits[d2] == '?':
                new_room = self.take_exit(d2)
                self.dft_recursive(new_room, finished)
            elif d3 in current_exits and current_exits[d3] == '?':
                new_room = self.take_exit(d3)
                self.dft_recursive(new_room, finished)
            elif d4 in current_exits and current_exits[d4] == '?':
                new_room = self.take_exit(d4)
                self.dft_recursive(new_room, finished)
            else:
                finished.add(starting_room)

    # Find path to shortest unexplored room using breadth-first search
    def bfs(self, starting_room=None):
        starting_room = starting_room or self.player.current_room
        queue = Queue()
        queue.enqueue([starting_room.id])
        visited = set()

        while queue.size() > 0:
            self.add_room(starting_room.id, starting_room.get_exits())

            current_path = queue.dequeue()
            current_room_id = current_path[-1]
            current_exits = self.get_exits(current_room_id)

            if '?' in current_exits.values():
                self.convert_bfs_to_directions(current_path)
                return

            if current_room_id not in visited:
                visited.add(current_room_id)
                for exit in current_exits:
                    path_to_next_room = [*current_path, current_exits[exit]]
                    queue.enqueue(path_to_next_room)

    # Convert list of room IDs to lists of directions to add to traversal path
    def convert_bfs_to_directions(self, list_rooms):
        steps = len(list_rooms) - 1
        for index in range(steps):
            exits = self.get_exits(list_rooms[index]).items()
            next_room = list_rooms[index + 1]
            direction = next(
                (direction for direction, room in exits if room == next_room), None)
            self.player.travel(direction)
            self.traversal_path.append(direction)
