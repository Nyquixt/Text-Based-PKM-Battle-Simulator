import math

class Pokemon:
    def __init__(self, moves, json_data, lv=50, iv=[31, 31, 31, 31, 31, 31], ev=[0, 0, 0 ,0, 0, 0]):

        '''
            lv: level of pokemon (default 50)
            iv: ivs of base stats, an array like [hp_iv, attack_iv, defense_iv, sp_attack_iv, sp_defense_iv, speed_iv]
            ev: evs of base stats, an array like [hp_ev, attack_ev, defense_ev, sp_attack_ev, sp_defense_ev, speed_ev]
            moves: a list of 4 moves used in battle
            json_data: data get parsed into stats
        '''
        self.lv = lv
        self.iv = iv
        self.ev = ev
        self.moves = moves

        self.name = json_data['Name']
        self.types = json_data['Types'].strip('][').split(', ') # convert str to list
        self.hp = self.calculate_hp(int(json_data['HP']), self.iv[0], self.ev[0])
        self.attack = self.calculate_other(int(json_data['Attack']), self.iv[1], self.ev[1])
        self.defense = self.calculate_other(int(json_data['Defense']), self.iv[2], self.ev[2])
        self.sp_attack = self.calculate_other(int(json_data['Special Attack']), self.iv[3], self.ev[3])
        self.sp_defense = self.calculate_other(int(json_data['Special Defense']), self.iv[4], self.ev[4])
        self.speed = self.calculate_other(int(json_data['Speed']), self.iv[5], self.ev[5])

    # Calculation based on Gen I and II on Bulbapedia
    def calculate_hp(self, base, iv, ev):
        return math.floor(((2 * (base + iv) + math.floor(ev / 4)) * self.lv)/100) + self.lv + 10

    def calculate_other(self, base, iv, ev):
        return math.floor(math.floor(((2 * (base + iv) + math.floor(ev / 4)) * self.lv)/100) + 5)

    def update_hp(self, delta):
        self.hp += delta


def test():
    json_data = {
        "Name": "Aerodactyl",
        "Types": "[Rock, Flying]",
        "Abilities": "[Pressure, Rock Head, Unnerve]",
        "Tier": "RU",
        "HP": "80",
        "Attack": "105",
        "Defense": "65",
        "Special Attack": "60",
        "Special Defense": "75",
        "Speed": "130",
        "Next Evolution(s)": "[]",
        "Moves": "[Iron Head, Ice Fang, Fire Fang, Thunder Fang, Wing Attack, Supersonic, Bite, Scary Face, Roar, Agility, Bite, Supersonic, Bite, Ancient Power, Scary Face, Crunch, Take Down, Iron Head, Sky Drop, Iron Head, Hyper Beam, Rock Slide, Giga Impact, Assurance, Curse, Dragon Breath, Foresight, Pursuit, Roost, Steel Wing, Tailwind, Whirlwind, Wide Guard, Air Cutter, Ancient Power, Aqua Tail, DoubleEdge, Dragon Pulse, Earth Power, Endure, Flamethrower, Headbutt, Heat Wave, Iron Head, Iron Tail, Mimic, Ominous Wind, Rock Slide, Roost, Sky Attack, Sleep Talk, Snore, Stealth Rock, Substitute, Swagger, Swift, Tailwind, Twister, Headbutt, Curse, Razor Wind, Whirlwind, Hone Claws, Dragon Claw, Roar, Toxic, Take Down, DoubleEdge, Rock Smash, Hidden Power, Snore, Sunny Day, Taunt, Hyper Beam, Rage, Dragon Rage, Mimic, Protect, Rain Dance, Endure, Roost, Frustration, Smack Down, Iron Tail, Dragon Breath, Earthquake, Return, Double Team, Flamethrower, Swagger, Sleep Talk, Sandstorm, Reflect, Bide, Fire Blast, Rock Tomb, Aerial Ace, Torment, Facade, Secret Power, Swift, Detect, Sky Attack, Rest, Attract, Thief, Round, Steel Wing, Roost, Sky Drop, Brutal Swing, Incinerate, Endure, Dragon Pulse, Payback, Giga Impact, Rock Polish, Stone Edge, Fly, Stealth Rock, Bulldoze, Captivate, Rock Slide, Sleep Talk, Natural Gift, Swagger, Sleep Talk, Substitute, Secret Power, Rock Smash, Confide, Fly, Strength, Defog, Rock Smash]"
    }
    pokemon = Pokemon(50, [31, 31, 31, 31, 31, 31], [74, 190, 91, 48, 84, 23], [], json_data)
    print(pokemon.name)
    print("Types", pokemon.types)
    print("HP", pokemon.hp)
    print("Atk", pokemon.attack)
    print("Def", pokemon.defense)
    print("Sp.Atk", pokemon.sp_attack)
    print("Sp.Def", pokemon.sp_defense)
    print("Speed", pokemon.speed)

# test()