import json


class PlayerMovement:
    def __init__(self, current_bank_code):
        self._current_bank_code = current_bank_code
        self._previous_bank_code = None
        self._current_town = self.get_location_from_bank()
        self._previous_town = None

    def __repr__(self):
        return (f"PlayerMovement object, currently in"
                f" {list(self._current_town)[0]}")

    @property
    def previous_bank_code(self):
        return self._previous_bank_code

    @property
    def current_bank_code(self):
        return self._current_bank_code

    @current_bank_code.setter
    def current_bank_code(self, new_bank_code):
        if self._current_bank_code is not None:
            self._previous_bank_code = self._current_bank_code
        self._current_bank_code = new_bank_code

        if self._current_town is not None:
            self._previous_town = self._current_town
        self._current_town = self.get_location_from_bank()

    def get_location_from_bank(self) -> dict:
        """
        From the received bank parameter, it will return the info of
        the town/building/route.
        """

        with open('src/json_files/locations.json', 'r') as json_file:
            json_data: dict = json.load(json_file)

        for idx, town in enumerate(json_data):
            for key, value in town.items():
                if self._current_bank_code == value["memory_address"]:
                    return town
