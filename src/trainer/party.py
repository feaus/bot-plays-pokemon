from src.battle.party_pokemon import PartyPokemon


class Party:
    def __init__(self):
        self.pokemon_1 = None
        self.pokemon_2 = None
        self.pokemon_3 = None
        self.pokemon_4 = None
        self.pokemon_5 = None
        self.pokemon_6 = None

    def __repr__(self):
        return "Pokemon party object"

    def modify_party(self, pokemon: PartyPokemon, slot: int):
        if slot == 1:
            self.pokemon_1 = pokemon
        elif slot == 2:
            self.pokemon_2 = pokemon
        elif slot == 3:
            self.pokemon_3 = pokemon
        elif slot == 4:
            self.pokemon_4 = pokemon
        elif slot == 5:
            self.pokemon_5 = pokemon
        elif slot == 6:
            self.pokemon_6 = pokemon

    def reorder_pokemon(self, origin_slot: int, destination_slot: int):
        list_of_slots = list(self.list_of_attributes())
        origin_pokemon = self.__dict__.get(list_of_slots[origin_slot])
        destination_pokemon = self.__dict__.get(list_of_slots[destination_slot])

        setattr(self, list_of_slots[origin_slot], destination_pokemon)
        setattr(self, list_of_slots[destination_slot], origin_pokemon)

    def list_of_attributes(self):
        return vars(self)

    def list_of_pokemon(self):
        return [self.pokemon_1, self.pokemon_2, self.pokemon_3, self.pokemon_4,
                self.pokemon_5, self.pokemon_6]
