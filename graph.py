from utils import Queue


class Graph():
    def __init__(self, player, room_graph):
        self.rooms = {}
        self.player = player
        self.room_graph = room_graph
        self.traversal_path = []

    # Add a room (vertex) to graph
    def add_room(self, room_id, exits):
        if room_id not in self.rooms:
            # self.rooms[room_id] = {}
            # ***
            self.rooms[room_id] = [{}]
            # self.rooms[room_id][0] = {}
            # ***
            for exit in exits:
                # self.rooms[room_id][exit] = '?'
                # ***
                self.rooms[room_id][0][exit] = '?'
                # ***
            # self.rooms[room_id]['coordinates'] = ()

    # Add directed exits (edges) to graph
    def add_exits(self, room1, room2, direction):
        opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        if room1 in self.rooms and room2 in self.rooms:
            # self.rooms[room1][direction] = room2
            # self.rooms[room2][opposite_direction[direction]] = room1
            # ***
            self.rooms[room1][0][direction] = room2
            self.rooms[room2][0][opposite_direction[direction]] = room1
            # ***
        else:
            raise IndexError('That room does not exist!')

    # Get all exits (edges) of a room (vertex)
    def get_exits(self, room_id):
        # return self.rooms[room_id]
        # ***
        return self.rooms[room_id][0]
        # ***

    # Navigate to next room and update graph
    def take_exit(self, direction):
        previous_room = self.player.current_room
        self.player.travel(direction)
        self.traversal_path.append(direction)

        new_room = self.player.current_room
        self.add_room(new_room.id, new_room.get_exits())
        self.add_exits(previous_room.id, new_room.id, direction)

        print('NEW ROOM', new_room.id)
        print('ROOM GRAPH', self.room_graph[new_room.id][0])

        return new_room

    # Navigate to each room in depth-first order beginning from starting room, done using recursion
    def dft_recursive(self, starting_room=None, finished=None):
        starting_room = starting_room or self.player.current_room
        finished = finished or set()

        if starting_room not in finished:
            self.add_room(starting_room.id, starting_room.get_exits())

            current_room_id = starting_room.id
            current_exits = self.get_exits(current_room_id)

            directions = ['s', 'w', 'n', 'e']
            # directions = ['s', 'e', 'w', 'n']

            if directions[0] in current_exits and current_exits[directions[0]] == '?':
                new_room = self.take_exit(directions[0])
                self.dft_recursive(new_room, finished)
            elif directions[1] in current_exits and current_exits[directions[1]] == '?':
                new_room = self.take_exit(directions[1])
                self.dft_recursive(new_room, finished)
            elif directions[2] in current_exits and current_exits[directions[2]] == '?':
                new_room = self.take_exit(directions[2])
                self.dft_recursive(new_room, finished)
            elif directions[3] in current_exits and current_exits[directions[3]] == '?':
                new_room = self.take_exit(directions[3])
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

            # print('Path', self.traversal_path)
            # print('BFS', current_room_id)

            if '?' in current_exits.values():
                self.convert_path_to_directions(current_path)
                return

            if current_room_id not in visited:
                visited.add(current_room_id)
                for exit in current_exits:
                    path_to_next_room = [*current_path, current_exits[exit]]
                    queue.enqueue(path_to_next_room)

    # Convert list of room IDs to lists of directions to add to traversal path
    def convert_path_to_directions(self, list_rooms):
        steps_in_path = len(list_rooms) - 1
        for index in range(steps_in_path):
            current_exits = self.get_exits(list_rooms[index]).items()
            next_room = list_rooms[index + 1]
            direction = next(
                (direction for direction, room in current_exits if room == next_room), None)
            self.player.travel(direction)
            self.traversal_path.append(direction)
