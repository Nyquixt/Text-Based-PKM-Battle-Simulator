# Text-Based Pokemon Battle Simulator

A simple Gen I Pokemon Battle Simulator in Python. Only Physical and Special moves with numeric Power and Accuracy moves are used in the game, so far. Pokemon data is taken from [here](https://www.kaggle.com/n2cholas/competitive-pokemon-dataset). Program is still buggy.

## TODO:
- Input validation
- Status moves
- AI players
- Socket for online multi-players(maybe)

## Implementation Details

### Statistics
HP is calculated as:

```py
hp = floor(((2 * (base_hp + iv) + floor(ev / 4)) * level)/100)
```

Other stats are calculated as:

```py
stat = floor(floor(((2 * (base_stat + iv) + floor(ev / 4)) * level)/100) + 5)
```

For simplicity, IVs are all set to 31, and EVs are all set to 0

### Damage
Damage is calculated as:

```py
modifier = (random[0.85, 1.00] * stab * type_effectiveness

floor( (((((2 * pokemon1.level) / 5) + 2) * move1.power * (pokemon1.attack/pokemon2.defense) / 50) + 2) * modifier )
```
where `stab = 1.5` if `True` and `1.0` if `False`, `Attack` and `Defense` stats are used for `Physical` moves, `Sp_Attack` and `Sp_Defense` for `Special`.

### Accuracy
Accuracy is determined by generating a random number `R` between 1 and 100. If `R > 100`, then attack misses.