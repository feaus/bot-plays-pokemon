class WildPokemon:
    def __init__(self, name: str, main_type: str, level: int, health: int,
                 secondary_type: str = None, status: str = None, **kwargs):
        self.name = name
        self.main_type = main_type
        self.secondary_type = secondary_type
        self.level = level
        self.health = health
        self.status = status
        self.move_1 = kwargs.get('move_1')
        self.move_2 = kwargs.get('move_2')
        self.move_3 = kwargs.get('move_3')
        self.move_4 = kwargs.get('move_4')

    def __str__(self):
        return f"Wild pokemon {self.name}, level {self.level}"

    def change_status(self, status):
        self.status = status

    def change_health(self, hitpoints: int):
        self.health += hitpoints
