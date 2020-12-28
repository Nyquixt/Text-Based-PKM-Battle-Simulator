class Player:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons
        self.current_pokemon = pokemons[0]
        self.current_pokemon_index = 0
        self.remaining_pokemons = 3
    
    def handle_command(self, command):
        if command.lower() == 'fight':
            # choose a move
            for i, m in enumerate(self.current_pokemon.moves):
                print('({}): {} ({}/{})'.format(i, m.name, m.pp, m.max_pp))
            issued_move = int(input('Choose a move number (0-3): '))
            return (command.lower(), self.current_pokemon, issued_move)
        elif command.lower() == 'switch':
            # display possible options of pokemons
            valid_switching_pokemons = [] # index of valid pokemons for switching
            for i, p in enumerate(self.pokemons):
                if p.hp <= 0:
                    print('({}): {} (Fainted)'.format(i, p.name))
                else:
                    valid_switching_pokemons.append(i)
                    print('({}): {}'.format(i, p.name))
            # switch current pokemon out for a pokemon on the bench
            
            while True:
                switched_pokemon = int(input('Choose a pokemon to switch out (0-2): '))
                if switched_pokemon in valid_switching_pokemons:
                    break

            return (command.lower(), self.current_pokemon_index, switched_pokemon)
        elif command.lower() == 'exit':
            return (command.lower(), None, None)

class EffectivenessPlayer:
    '''
        AI Player that chooses move depending on the effectiveness against the opponent's 
        current pokemon
    '''
    def __init__(self, name, pokemons, opp_current_pokemon):
        self.name = name
        self.pokemons = pokemons
        self.opp_current_pokemon = opp_current_pokemon
        self.current_pokemon = pokemons[0]

    def choose_move(self):
        pass