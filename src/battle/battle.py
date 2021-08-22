import json
import os
import requests

from dotenv import load_dotenv
from pathlib import Path
from typing import List, Optional, Tuple

from src.battle.move import Move
from src.battle.party_pokemon import PartyPokemon
from src.battle.wild_pokemon import WildPokemon
from src.trainer.party import Party

load_dotenv(f"{Path(__file__).parents[1]}\constants\.env")


class Battle:
    CURSOR_POSITION = 0
    TURN = 0

    def __init__(self, type_of_battle):
        self.cursor_position = self.CURSOR_POSITION
        self.cursor_position_moveset = self.CURSOR_POSITION
        self.turn = self.TURN
        self.type_of_battle = type_of_battle
        self.battle_ended = False
        if self.type_of_battle == "wild":
            self.can_run = True
        else:
            self.can_run = False

    def __repr__(self):
        return f"{self.type_of_battle.title()} battle"

    def battle(self, wild_pk: WildPokemon, party: Party):
        super_effective_moves, effective_moves = Battle.are_moves_effective(
            wild_pk=wild_pk,
            party_pk=party.pokemon_1
        )

        if wild_pk.level > party.pokemon_1.level + 2:
            self.run()
            return

        if all(moves is None for moves in
               [super_effective_moves, effective_moves]):
            self.run()
            return

        while not self.battle_ended:
            wild_pk, super_effective_moves, effective_moves = self.attack(
                wild_pk, super_effective_moves, effective_moves)

    def run(self) -> None:
        """
        Moves the cursor to the 'run' position.
        """

        if self.cursor_position == 0:
            print("move right")
            self.cursor_position = 1

        if self.cursor_position == 1:
            print("move down")
            self.cursor_position = 3

        if self.cursor_position == 2:
            print("move right")
            self.cursor_position = 3
        print("press a")
        self.battle_ended = True

    def attack(self, wild_pk: WildPokemon,
               super_eff_moves: List[Optional[Move]],
               effective_moves: List[Optional[Move]]):
        if super_eff_moves and any(x.pp for x in super_eff_moves):
            super_eff_moves = sorted(
                super_eff_moves,
                key=lambda a: (a.power, a.accuracy, a.pp),
                reverse=True
            )
            idx = 0
            for move in super_eff_moves:
                while move.pp > 0:
                    print("attack")
                    move.reduce_pp_after_attacking()

        if effective_moves and any(x.pp for x in effective_moves):
            effective_moves = sorted(
                effective_moves,
                key=lambda a: (a.power, a.accuracy, a.pp),
                reverse=True
            )

            for move in effective_moves:
                while move.pp > 0:
                    print("attack")
                    move.reduce_pp_after_attacking()

        return super_eff_moves, effective_moves

    @staticmethod
    def kind_of_damage(response: dict, wild_pokemon_types: list,
                       type_of_damage: str):
        for element_type in response[type_of_damage]:
            if element_type['name'] in wild_pokemon_types:
                return True
        return False

    @staticmethod
    def are_moves_effective(wild_pk: WildPokemon, party_pk: PartyPokemon
                            ) -> Tuple[List[Optional[Move]], List[Optional[Move]]]:
        moves = []
        for move in [party_pk.move_1, party_pk.move_2, party_pk.move_3,
                     party_pk.move_4]:
            if move is not None and move.type in ["physical", "special"]:
                moves.append(move)

        with open('../json_files/pokeapi.json', 'r') as json_file:
            json_data = json.load(json_file)

        wild_pokemon_types = [wild_pk.main_type, wild_pk.secondary_type]
        effective_moves = []
        super_effective_moves = []

        for move in moves:
            type_index = json_data["types"][move.elemental_type]
            url = f"{os.environ.get('POKEAPI_URL')}/type/{type_index}"
            response = requests.get(url)
            response_json = response.json()['damage_relations']

            move_does_no_damage = Battle.kind_of_damage(
                response_json, wild_pokemon_types, 'no_damage_to')
            if move_does_no_damage:
                continue

            move_does_half_damage = Battle.kind_of_damage(
                response_json, wild_pokemon_types, "half_damage_to")
            if move_does_half_damage:
                continue

            move_does_double_damage = Battle.kind_of_damage(
                response_json, wild_pokemon_types, "double_damage_to")
            if move_does_double_damage:
                super_effective_moves.append(move)
                continue
            effective_moves.append(move)
        return super_effective_moves, effective_moves


if __name__ == '__main__':
    party = Party()
    pokemon = PartyPokemon(
        name='cyndaquil',
        main_type='fire',
        level=5,
        health=20,
        status=None,
        move_1=True,
        move_1_name='scratch',
        move_1_type='physical',
        move_1_elemental_type='normal',
        move_1_pp=35,
        move_1_power=35,
        move_1_accuracy=100,
        move_2=True,
        move_2_name='ember',
        move_2_type='special',
        move_2_elemental_type='fire',
        move_2_pp=25,
        move_2_power=45,
        move_2_accuracy=100,
    )
    party.modify_party(pokemon, 1)
    wild_pokemon = WildPokemon(
        name='rattata',
        main_type='normal',
        secondary_type=None,
        level=3,
        health=15,
        status=None,
        move_1=None,
        move_2=None,
        move_3=None,
        move_4=None,
    )

    battle = Battle(type_of_battle='wild')
    while not battle.battle_ended:
        battle.battle(wild_pk=wild_pokemon, party=party)
