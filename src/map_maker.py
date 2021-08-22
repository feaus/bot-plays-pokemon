import json


class MapMaker:
    def __init__(self, **kwargs):
        self.location_name = kwargs.get("location_name")
        self.town_index = kwargs.get("town_index")
        self.last_movement = kwargs.get("last_movement")
        self.map = []

    def print_map(self) -> None:
        """
        Prints the map in a nice way. E.g.::
            ["?", "?", "?", "?"]
            ["?", "B", "P", "?"]
            ["?", "?", "?", "?"]
        """

        for row in self.map:
            print(row)

    def map_maker(self, safe: bool = False, block: bool = False,
                  interactive: bool = False, warp: bool = False):
        """

        :param safe:
        :param block:
        :param interactive:
        :param warp:
        :return:
        """

        if all(param is None for param in [safe, block, interactive, warp]):
            print("At least one parameter must be specified!!")
            raise Exception

        with open('src/json_files/locations.json', 'r+') as json_file:
            json_data: dict = json.load(json_file)

            current_map = json_data[self.town_index][self.location_name]["map"]

            if safe:
                current_map = self.mark_space_as_safe(current_map)
            elif block:
                current_map = self.mark_space_as_special(current_map, "B")
            elif interactive:
                current_map = self.mark_space_as_special(current_map, "I")
            elif warp:
                current_map = self.mark_space_as_special(current_map, "W")

            json_file.seek(0)
            json.dump(json_data, json_file, indent=2)
            json_file.truncate()

        self.map = current_map

    def mark_space_as_special(self, current_map: list, mark_as: str) -> list:
        row: list
        if self.last_movement[0] == "left":
            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index - 1] = mark_as

        elif self.last_movement[0] == "up":
            row_index = 0
            p_index = 0
            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    row_index = idx
                    break
            current_map[row_index - 1][p_index] = mark_as

        elif self.last_movement[0] == "right":
            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index + 1] = mark_as

        elif self.last_movement[0] == "down":
            row_index = 0
            p_index = 0
            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    row_index = idx
                    break
            current_map[row_index + 1][p_index] = mark_as

        return current_map

    def mark_space_as_safe(self, current_map: list) -> list:
        row: list
        if self.last_movement[0] == "left":
            for idx, row in enumerate(current_map):
                current_map[idx].insert(0, '?')

                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index] = "S"
                    current_map[idx][p_index - 1] = "P"

        elif self.last_movement[0] == "up":
            row_length = len(current_map[0])
            new_row = ["?" for _ in range(row_length)]
            current_map.insert(0, new_row)

            row_index = 0
            p_index = 0

            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index] = "S"

                    row_index = idx
            current_map[row_index - 1][p_index] = "P"

        elif self.last_movement[0] == "right":
            for idx, row in enumerate(current_map):
                current_map[idx].append('?')

                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index] = "S"
                    current_map[idx][p_index + 1] = "P"

        elif self.last_movement[0] == "down":
            row_length = len(current_map[0])
            new_row = ["?" for _ in range(row_length)]
            current_map.append(new_row)

            row_index = 0
            p_index = 0

            for idx, row in enumerate(current_map):
                if "P" in row:
                    p_index = row.index("P")
                    current_map[idx][p_index] = "S"

                    row_index = idx
            current_map[row_index + 1][p_index] = "P"

        return current_map
