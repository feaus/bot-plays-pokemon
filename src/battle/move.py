class Move:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.elemental_type = kwargs.get('elemental_type')
        self.pp = kwargs.get('pp')
        self.power = kwargs.get('power')
        self.accuracy = kwargs.get('accuracy')
        self.slot_position = kwargs.get('slot_position')

    def __repr__(self):
        return f"Move {self.name}"

    def reduce_pp_after_attacking(self):
        self.pp -= 1

