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
        # print('28', room_id)
        return self.rooms[room_id]

    # Navigate to next room given input of direction
    def take_exit(self, direction):
        print(f'{direction} exit unexplored, traveling {direction}')
        print('---')
        room_leaving = self.player.current_room
        self.player.travel(direction)
        self.traversal_path.append(direction)
        new_room = self.player.current_room
        self.add_room(new_room.id, new_room.get_exits())
        self.add_exits(room_leaving.id, new_room.id, direction)
        return new_room

    def dft_recursive(self, starting_room=None, finished=None):
        starting_room = starting_room or self.player.current_room
        finished = finished or set()
        # print('DFT_R', starting_room.id)

        if starting_room not in finished:
            self.add_room(starting_room.id, starting_room.get_exits())

            current_room_id = starting_room.id
            current_exits = self.get_exits(current_room_id)

            print('Current Room:', current_room_id)
            print('Exits:', current_exits)

            if 'n' in current_exits and current_exits['n'] == '?':
                new_room = self.take_exit('n')
                self.dft_recursive(new_room, finished)
            elif 'e' in current_exits and current_exits['e'] == '?':
                new_room = self.take_exit('e')
                self.dft_recursive(new_room, finished)
            elif 's' in current_exits and current_exits['s'] == '?':
                new_room = self.take_exit('s')
                self.dft_recursive(new_room, finished)
            elif 'w' in current_exits and current_exits['w'] == '?':
                new_room = self.take_exit('w')
                self.dft_recursive(new_room, finished)
            else:
                print('All exits explored!')
                finished.add(starting_room)

    def bfs(self, starting_room=None):
        # print('BFS RUN')
        starting_room = starting_room or self.player.current_room
        queue = Queue()
        queue.enqueue([starting_room.id])
        visited = set()

        while queue.size() > 0:
            # print('Q SIZE', queue.size())
            self.add_room(starting_room.id, starting_room.get_exits())

            current_path = queue.dequeue()
            current_room_id = current_path[-1]
            # print('LINE 80', current_room_id)
            current_exits = self.get_exits(current_room_id)

            # print('BFS current exits', current_exits)

            if '?' in current_exits.values():
                # print('?', current_path)
                # print('traversal_path', self.traversal_path)
                # print('XXXXXXX')
                self.convert_bfs_to_directions(current_path)
                return

            if current_room_id not in visited:
                visited.add(current_room_id)
                for exit in current_exits:
                    path_to_next_room = [*current_path, current_exits[exit]]
                    queue.enqueue(path_to_next_room)

    def convert_bfs_to_directions(self, list_rooms):
        # print('CURRENT ROOM', self.player.current_room.id)
        # print('LIST TO CONVERT', list_rooms)
        for index in range(len(list_rooms) - 1):
            # print(index, list_rooms[index], list_rooms[index + 1])
            # print('ROOM', list_rooms[index])
            # print('NEXT_ROOM', list_rooms[index + 1])
            # print('KEYS', self.get_exits(list_rooms[index]))
            key = next((key for key, value in self.get_exits(
                list_rooms[index]).items() if value == list_rooms[index + 1]), None)
            # print('KEY', key)
            # print('BFS CONVERSION')
            self.player.travel(key)
            self.traversal_path.append(key)
            # print(self.traversal_path)
