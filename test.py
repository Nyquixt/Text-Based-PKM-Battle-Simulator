from src.game import Game

def test_fight():
    game = Game()
    print(game.pokemon2.hp)
    game.fight(game.pokemon1.moves[1], game.pokemon1, game.pokemon2)
    print(game.pokemon2.hp)

def test_generate_info():
    game = Game()
    game.print_pokemon_info(game.player1)
    game.print_pokemon_info(game.player2)

def test_game_loop():
    game = Game()
    game.game_loop()

# test_fight()
# test_generate_info()
# test_game_loop()