import json
import pydirectinput
import time

from typing import Tuple

from src.map_maker import map_maker
from src.pipe import Pipe


def get_location_from_bank(bank) -> Tuple[int, dict]:
    """
    From the received bank parameter, it will return the info of the
    town/building/route.
    """

    with open('src/json_files/locations.json', 'r') as json_file:
        json_data: dict = json.load(json_file)

    for idx, town in enumerate(json_data):
        for key, value in town.items():
            if bank == value["memory_address"]:
                return idx, town


def start_roaming(pipe: Pipe):
    # This should get the bank
    current_bank = pipe.pipe_server()

    town_index, town = get_location_from_bank(current_bank)
    town_name: str = list(town.keys())[0]
    print(f"I am in {town_name.replace('_', ' ').title()}")

    # I should have the x and y coordinates for this bank
    x_coordinate: int
    y_coordinate: int
    print(f"Current coordinates: {x_coordinate}, {y_coordinate}")

    directions = [('left', 8), ('up', 4), ('right', 12), ('down', 0)]
    last_movement = directions[0]

    print(f"Trying to move {last_movement[0]}...")
    pydirectinput.press(directions[0])

    # I should now have the new coordinates, that may or may not be the same
    new_x_coordinate: int
    new_y_coordinate: int
    if x_coordinate == new_x_coordinate:
        print("Something is blocking the way")
    else:
        map_maker(location_name=town_name, town_index=town_index, last_movement=last_movement)




def coordinates(pipe: Pipe):
    visited_coordinates = []
    t_end = time.time() + 20
    movements = []
    directions = {'up': 4, 'right': 12, 'down': 0, 'left': 8}

    while time.time() < t_end:
        for message in pipe.pipe_server():
            for direction, val in directions.items():
                if direction not in movements:
                    pydirectinput.press(direction)
                    if message[3] != val:
                        pydirectinput.press(direction)
                    movements.append(direction)
                    break
            print(message)
            # if [message[0], message[1]] in visited_coordinates:
            #     if "left" in movements:
            #         if "down" in movements:
            #             if "right" in movements:
            #                 pydirectinput.press("up")
            #                 if message[3] != 4:
            #                     pydirectinput.press("up")
            #                 movements.append("up")
            #             else:
            #                 pydirectinput.press("right")
            #                 if message[3] != 12:
            #                     pydirectinput.press("right")
            #                 movements.append("right")
            #         else:
            #             pydirectinput.press("down")
            #             if message[3] != 0:
            #                 pydirectinput.press("down")
            #             movements.append("down")
            #     else:
            #         pydirectinput.press("left")
            #         if message[3] != 8:
            #             pydirectinput.press("left")
            #         movements.append("left")
            #     continue
            # movements = []
            # if message[2] != 4:
            #     pydirectinput.press("right", presses=2)
            if [message[0], message[1]] not in visited_coordinates:
                visited_coordinates.append([message[0], message[1]])

    return print(visited_coordinates)


if __name__ == "__main__":
    pipe_instance = Pipe(server=True)
    coordinates(pipe_instance)
    pipe_instance.close_handle()
