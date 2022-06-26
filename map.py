import numpy as np
import random
import sys


class Map:
    def __init__(self):
        self.walls = []
        self.wall_width = 5
        self.create_level()

    def create_level(self):
        # 0 = wall
        # 1 = floor
        # 2 = doorway
        # 3 = courtyard
        self.MAP_HEIGHT = 20
        self.MAP_WIDTH = 30
        self.min_room_length = 2
        self.max_room_length = 5
        self.count = 0
        rooms = (self.map_generator(4, 7))
        rooms = rooms.tolist()
        room_corners = []
        for c in range(self.count):
            room_corners.append([])
        for row, line in enumerate(rooms):
            for col, char in enumerate(line):
                if char != 0 and char != 9:
                    if len(room_corners[char]) == 0:
                        room_corners[char].append((row, col))
                    elif len(room_corners[char]) == 1:
                        if room_corners[0][0] == row:
                            room_corners[0][1] = (row, col)


    def map_generator(self, min_rooms, max_rooms):
        map_structure = np.zeros((self.MAP_HEIGHT, self.MAP_WIDTH), dtype=int)
        count = random.randint(min_rooms, max_rooms)
        self.count = count
        rooms = []
        while count > 0:
            new_room = self.single_room_generator(self.min_room_length, self.max_room_length, len(rooms) + 1)
            x_placement = random.randrange(0, self.MAP_WIDTH - len(new_room[0]))
            y_placement = random.randrange(0, self.MAP_HEIGHT - len(new_room))
            placement_size = map_structure[y_placement:y_placement + len(new_room),
                             x_placement:x_placement + len(new_room[0])]
            if placement_size.any() == 0:
                map_structure[y_placement:y_placement + len(new_room),
                x_placement:x_placement + len(new_room[0])] += new_room
                rooms.append(
                    (y_placement, y_placement + len(new_room), x_placement, x_placement + len(new_room[0])))
                count -= 1
            else:
                pass
        # add corridors
        indexs = [0] * len(rooms)
        # enumerate over rooms and find room which is the closest... record coordinates into list called
        # index where shape is ((y1, x1), (y2, x2))
        groups = [0] * len(rooms)
        for i, room_1 in enumerate(rooms):
            distance = max(self.MAP_WIDTH, self.MAP_HEIGHT) * 2
            for j, room_2 in enumerate(rooms.copy()):
                if room_2 == room_1:
                    continue
                # find minimum distance
                for tuple_1 in ((y, x) for y in range(min(room_1[:2]), max(room_1[:2])) for x in
                                range(min(room_1[2:]), max(room_1[2:]))):
                    for tuple_2 in ((y, x) for y in range(min(room_2[:2]), max(room_2[:2])) for x in
                                    range(min(room_2[2:]), max(room_2[2:]))):
                        d = abs(tuple_1[0] - tuple_2[0]) + abs(tuple_1[1] - tuple_2[1])
                        if d < distance:
                            distance = d
                            indexs[i] = (tuple_1, tuple_2)
                            groups[i] = j

        # join groups into sets. calculate index to do so
        group_sets = []
        for room_1, room_2 in enumerate(groups):
            found = False
            for group_set in group_sets:
                if room_1 in group_set:
                    group_set.add(room_2)
                    found = True
                    break
                elif room_2 in group_set:
                    group_set.add(room_1)
                    found = True
                    break
            if not found:
                group_sets.append({room_1, room_2})
        if len(group_sets) > 1:
            for count, group_set in enumerate(group_sets):
                distance = max(self.MAP_WIDTH, self.MAP_HEIGHT) * 2
                indexs.append(0)
                for count_2, group_set_2 in enumerate(group_sets.copy()):
                    if count != count_2:
                        # find minimum distance
                        for g in group_set:
                            for g2 in group_set_2:
                                for tuple_1 in ((y, x) for y in range(min(rooms[g][:2]), max(rooms[g][:2])) for x in
                                                range(min(rooms[g][2:]), max(rooms[g][2:]))):
                                    for tuple_2 in ((y, x) for y in range(min(rooms[g2][:2]), max(rooms[g2][:2]))
                                                    for x in
                                                    range(min(rooms[g2][2:]), max(rooms[g2][2:]))):
                                        d = abs(tuple_1[0] - tuple_2[0]) + abs(tuple_1[1] - tuple_2[1])
                                        if d < distance:
                                            distance = d
                                            indexs[-1] = (tuple_1, tuple_2)
                                        elif d == distance:
                                            if random.randint(0, 2) == 1:
                                                indexs[-1] = (tuple_1, tuple_2)

        # remove indexs where they are just the backwards of the first... this can occur where, for example, room 2 is the
        # closest to room 1 and it so happens that room 1 is also the closest to room 2.
        for ((r1, c1), (r2, c2)) in indexs.copy():
            if ((r2, c2), (r1, c1)) in indexs:
                indexs.remove(((r1, c1), (r2, c2)))

        for ((r1, c1), (r2, c2)) in indexs:
            # find max and min of x and y values so range() works correctly
            r_max = max(r1, r2)
            r_min = min(r1, r2)
            c_max = max(c1, c2)
            c_min = min(c1, c2)
            # if rooms are diagonal to each other in which a horizontal or vertical path cannot be connected
            if r1 != r2 and c1 != c2:
                # choose random direction from: row or col first
                condition = (r1 < r2 and c1 < c2) or (r2 < r1 and c2 < c1)
                if random.randint(0, 1) == 0:
                    for r in range(r_min, r_max):
                        if map_structure[r][c_max if condition else c_min] != 0:
                            continue
                        map_structure[r][c_max if condition else c_min] = 9
                    for c in range(c_min, c_max):
                        if map_structure[r_min][c] != 0:
                            continue
                        map_structure[r_min][c] = 9
                else:
                    for c in range(c_min, c_max):
                        if map_structure[r_min][c] != 0:
                            continue
                        map_structure[r_min][c] = 9
                    for r in range(r_min, r_max):
                        if map_structure[r][c_max if condition else c_min] != 0:
                            continue
                        map_structure[r][c_max if condition else c_min] = 9
            # horizontal path can be connected
            elif r1 == r2:
                for c in range(c_min + 1, c_max):
                    map_structure[r_min][c] = 9
            # vertical path can be connected
            else:
                for r in range(r_min + 1, r_max):
                    map_structure[r][c_max] = 9

        return map_structure

    def single_room_generator(self, min_length, max_length, number):
        width = random.randint(min_length, max_length)
        height = random.randint(min_length, max_length)
        room = np.ones((height, width), dtype=int) * number
        return room

