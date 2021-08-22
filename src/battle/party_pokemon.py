from src.battle.move import Move


class PartyPokemon:
    def __init__(self, name: str, main_type: str, level: int, health: int,
                 status: str = None, secondary_type: str = None, **kwargs):
        self.name = name
        self.main_type = main_type
        self.secondary_type = secondary_type
        self.level = level
        self.health = health
        self.status = status
        if kwargs.get('move_1'):
            self.move_1 = Move(
                name=kwargs.get('move_1_name'),
                type=kwargs.get('move_1_type'),
                elemental_type=kwargs.get('move_1_elemental_type'),
                pp=kwargs.get('move_1_pp'),
                power=kwargs.get('move_1_power'),
                accuracy=kwargs.get('move_1_accuracy'),
                slot_position=1
            )
        else:
            self.move_1 = None

        if kwargs.get('move_2'):
            self.move_2 = Move(
                name=kwargs.get('move_2_name'),
                type=kwargs.get('move_2_type'),
                elemental_type=kwargs.get('move_2_elemental_type'),
                pp=kwargs.get('move_2_pp'),
                power=kwargs.get('move_2_power'),
                accuracy=kwargs.get('move_2_accuracy'),
                slot_position=2
            )
        else:
            self.move_2 = None

        if kwargs.get('move_3'):
            self.move_3 = Move(
                name=kwargs.get('move_3_name'),
                type=kwargs.get('move_3_type'),
                elemental_type=kwargs.get('move_3_elemental_type'),
                pp=kwargs.get('move_3_pp'),
                power=kwargs.get('move_3_power'),
                accuracy=kwargs.get('move_3_accuracy'),
                slot_position=3
            )
        else:
            self.move_3 = None

        if kwargs.get('move_4'):
            self.move_4 = Move(
                name=kwargs.get('move_4_name'),
                type=kwargs.get('move_4_type'),
                elemental_type=kwargs.get('move_4_elemental_type'),
                pp=kwargs.get('move_4_pp'),
                power=kwargs.get('move_4_power'),
                accuracy=kwargs.get('move_4_accuracy'),
                slot_position=4
            )
        else:
            self.move_4 = None

    def __str__(self):
        return f"Party pokemon {self.name}, level {self.level}"

    def change_status(self, status):
        self.status = status

    def change_health(self, hitpoints: int):
        self.health += hitpoints

    def increase_level(self):
        self.level += 1

    def change_move(self, move_slot: int, move):
        if move_slot == 1:
            self.move_1 = move
        elif move_slot == 2:
            self.move_2 = move
        elif move_slot == 3:
            self.move_3 = move
        elif move_slot == 4:
            self.move_4 = move

    def add_new_move(self, move):
        for idx, slot in enumerate([self.move_2, self.move_3, self.move_4], start=2):
            if slot is None:
                self.change_move(move_slot=idx, move=move)
