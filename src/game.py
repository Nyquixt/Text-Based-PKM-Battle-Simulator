# NOTE: 1v1 game for now

from src.pokemon import Pokemon
from src.move import Move
from src.type import Type
from src.damage import Damage
from src.player import Player, EffectivenessPlayer
from src.utils import print_slow
import json
import random


class Game:
    def __init__(self):
        with open('data/pokemon.json', 'r') as infile:
            data = json.load(infile)
            self.pokemons = data['pokemons']
        
        with open('data/data.json', 'r') as infile:
            data = json.load(infile)
            self.moves = data['moves']
        
        self.player1 = Player('Red', self.generate_random_pokemons())
        self.player2 = Player('Blue', self.generate_random_pokemons())

        self.damage = Damage()

    def generate_random_pokemons(self):
        random_pokemons = random.sample(self.pokemons, 3)
        pokemons = []
        for p in random_pokemons:
            learnable_moves = p['Moves']
            selected_moves = self.generate_random_moves(learnable_moves)
            pokemon = Pokemon(moves=selected_moves, json_data=p)
            pokemons.append(pokemon)
        
        return pokemons

    def generate_random_moves(self, learnable_moves):
        physical_moves = []
        special_moves = []
        for m in self.moves:
            if m['Name'] in learnable_moves:
                if m['Category'] == 'Physical' and m['Power'] != 'None': # ignore move with None power
                    physical_moves.append(m)
                elif m['Category'] == 'Special' and m['Power'] != 'None':
                    special_moves.append(m)
        # NOTE: status move is not implemented for now, choose 2 physical and 2 special
        if len(physical_moves) > 2:
            random_physical_moves = random.sample(physical_moves, 2)
        else:
            random_physical_moves = physical_moves
        if len(special_moves) > (4 - len(random_physical_moves)):
            random_special_moves = random.sample(special_moves, 4 - len(random_physical_moves))
        else:
            random_special_moves = special_moves

        move_list = random_physical_moves + random_special_moves
        
        output = []
        for m in move_list:
            output.append(Move(m))
        
        return output
        
    def print_pokemon_info(self, player):
        print('Team: {}'.format(player.name))
        for p in player.pokemons:
            print(p.name)
            for m in p.moves:
                print(m.name)
            print('---------------')

    def fight(self, move, pokemon1, pokemon2):
        if move.accuracy == 100 or move.accuracy == 'None':
            damage_dealt = self.damage.calculate_damage(move, pokemon1, pokemon2)
        else:
            r = random.randint(1, 100)
            if r <= move.accuracy:
                damage_dealt = self.damage.calculate_damage(move, pokemon1, pokemon2)
            else:
                damage_dealt = 0

        # update PP of pokemon1
        move.update_pp(-1)
        # update HP of pokemon2
        pokemon2.update_hp(-damage_dealt)
        print_slow("{} used {}...".format(pokemon1.name, move.name))
        if damage_dealt == 0:
            print_slow("{} avoided the attack...".format(pokemon2.name))

    def switch(self, player, pokemon_index):
        player.current_pokemon = player.pokemons[pokemon_index]
        player.current_pokemon_index = pokemon_index
        print_slow("Player {}: {} is switched out...".format(player.name, player.current_pokemon.name))
        

    def print_basic_info(self, turn, pokemon1, pokemon2):
        print('Turn {}'.format(turn))
        print('{}\'s HP: {}'.format(pokemon1.name, pokemon1.hp))
        print('{}\'s HP: {}'.format(pokemon2.name, pokemon2.hp))

    def check_fainting(self, pokemon):
        if pokemon.hp <= 0:
            print('{} fainted...'.format(pokemon.name)) 
            return True
        return False

    # TODO: refactor this function
    def handle_fight_fight(self, player1, player2, move_index1, move_index2):
        pokemon1 = player1.current_pokemon
        pokemon2 = player2.current_pokemon
        move1 = pokemon1.moves[move_index1]
        move2 = pokemon2.moves[move_index2]

        # move order
        if pokemon1.speed > pokemon2.speed:
            self.fight(move1, pokemon1, pokemon2)
            if self.check_fainting(pokemon2):
                player2.remaining_pokemons -= 1
                return 'player2'
            self.fight(move2, pokemon2, pokemon1)
            if self.check_fainting(pokemon1):
                player1.remaining_pokemons -= 1
                return 'player1'
        elif pokemon1.speed < pokemon2.speed:
            self.fight(move2, pokemon2, pokemon1)
            if self.check_fainting(pokemon1):
                player1.remaining_pokemons -= 1
                return 'player1'
            self.fight(move1, pokemon1, pokemon2)
            if self.check_fainting(pokemon2):
                player2.remaining_pokemons -= 1
                return 'player2'
        else:
            random_pokemon = random.randint(1, 2)
            if random_pokemon == 1:
                self.fight(move1, pokemon1, pokemon2)
                if self.check_fainting(pokemon2):
                    player2.remaining_pokemons -= 1
                    return 'player2'
                self.fight(move2, pokemon2, pokemon1)
                if self.check_fainting(pokemon1):
                    player1.remaining_pokemons -= 1
                    return 'player1'
            else:
                self.fight(move2, pokemon2, pokemon1)
                if self.check_fainting(pokemon1):
                    player1.remaining_pokemons -= 1
                    return 'player1'
                self.fight(move1, pokemon1, pokemon2)
                if self.check_fainting(pokemon2):
                    player2.remaining_pokemons -= 1
                    return 'player2'
        
        return 'None'

    def handle_switch_switch(self, player1, switched_pokemon1, player2, switched_pokemon2):
        self.switch(player1, switched_pokemon1)
        self.switch(player2, switched_pokemon2)

    def handle_switch_fight(self, player1, action1, player2, action2):
        # if player1 issue switch, player1 switch first and then player2 fight
        if action1[0] == 'switch':
            self.switch(player1, action1[2])
            # player2 fight
            move2 = player2.current_pokemon.moves[action2[2]]
            self.fight(move2, player2.current_pokemon, player1.current_pokemon)
            if self.check_fainting(player1.current_pokemon):
                player1.remaining_pokemons -= 1
                return 'player1'
        elif action2[0] == 'switch':
            self.switch(player2, action2[2])
            # player1 fight
            move1 = player1.current_pokemon.moves[action1[2]]
            self.fight(move1, player1.current_pokemon, player2.current_pokemon)
            if self.check_fainting(player2.current_pokemon):
                player2.remaining_pokemons -= 1
                return 'player2'

    def game_loop(self):
        
        gameOver = False
        turn = 1
        while(not gameOver):
            self.print_basic_info(turn, self.player1.current_pokemon, self.player2.current_pokemon)
            command = input('Player1 - Enter a command (fight, switch, exit): ')
            while command == 'list':
                action1 = self.player1.handle_command(command)
                command = input('Player1 - Enter a command (fight, switch, exit): ')
            action1 = self.player1.handle_command(command)
            if action1[0] == 'exit':
                print('Bye...')
                break

            command = input('Player2 - Enter a command (fight, switch, exit): ')
            while command == 'list':
                action2 = self.player2.handle_command(command)
                command = input('Player1 - Enter a command (fight, switch, exit): ')
            action2 = self.player2.handle_command(command)
            if action2[0] == 'exit':
                print('Bye...')
                break

            if action1[0] == 'fight' and action2[0] == 'fight':
                player_to_switch = self.handle_fight_fight(self.player1, self.player2, action1[2], action2[2])
            elif action1[0] == 'switch' and action2[0] == 'switch':
                self.handle_switch_switch(self.player1, action1[2], self.player2, action2[2])
            else:
                player_to_switch = self.handle_switch_fight(self.player1, action1, self.player2, action2)

            # check game over
            if self.player1.remaining_pokemons == 0 or self.player2.remaining_pokemons == 0:
                gameOver = True

            # handle switch if a pokemon faints
            if player_to_switch == 'player1' or 'player2':
                if player_to_switch == 'player1':
                    action = self.player1.handle_command('switch')
                    self.switch(self.player1, action[2])
                elif player_to_switch == 'player2':
                    action = self.player2.handle_command('switch')
                    self.switch(self.player2, action[2])
                    
            turn += 1