import random
import math
from src.type import Type

class Damage:
    def __init__(self):
        pass

    def calculate_modifier(self, stab, type_eff):
        return (random.randint(85, 101) / 100) \
            * (1.5 if stab == True else 1.0) \
            * type_eff

    def calculate_damage(self, move, pokemon1, pokemon2):
        # NOTE: ignore Status move for now
        if move.category == 'Physical':
            numerator = (((2 * pokemon1.lv) / 5) + 2) * move.power * (pokemon1.attack/pokemon2.defense)
        elif move.category == 'Special':
            numerator = (((2 * pokemon1.lv) / 5) + 2) * move.power * (pokemon1.sp_attack/pokemon2.sp_defense)

        if move.type in pokemon1.types:
            stab = True
        else:
            stab = False

        modifier = self.calculate_modifier(stab, Type().get_effectiveness(move.type, pokemon2.types))

        return math.floor( ((numerator / 50) + 2) * modifier )

def test():
    from src.move import Move
    from src.pokemon import Pokemon
    move = {
        'Index': '11',
        'Name': 'Vice Grip',
        'Type': 'Normal',
        'Category': 'Physical',
        'Contest': 'Tough',
        'PP': '30',
        'Power': '55',
        'Accuracy': '100',
        'Generation': '1'
    }

    damage = Damage()
    print(damage.calculate_damage(
            Move(move['Name'], move['Type'], move['Category'], move['Contest'], int(move['PP']), int(move['Power'])),
            Pokemon('Scizor', 50, ['Bug', 'Steel'], 70, 130, 100, 55, 80, 65, [31, 31, 31, 31, 31, 31], [74, 190, 91, 48, 84, 23], []),
            Pokemon('Scizor', 50, ['Bug', 'Steel'], 70, 130, 100, 55, 80, 65, [31, 31, 31, 31, 31, 31], [74, 190, 91, 48, 84, 23], [])
        )
    )

# test()
