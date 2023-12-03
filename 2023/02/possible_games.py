import re
import functools

def possible_games(**bag):
    id_sum = 0
    with open("input", "r") as f:
        for line in f:
            id_part, game = line.split(":", 1)
            game_id = int(id_part[5:])
            for cubes in re.finditer(r"(\d+) +([a-z]+)", game):
                num, colour = cubes.groups()
                if colour not in bag or int(num) > bag[colour]:
                    print(f"Game {game_id} is not possible")
                    break
            else:
                print(f"Game {game_id} *is* possible")
                id_sum += game_id

    return id_sum


def multiply(x, y):
    return x * y


def smallest_bag_per_game():
    total_power = 0
    with open("input", "r") as f:
        for line in f:
            id_part, game = line.split(":", 1)
            game_id = int(id_part[5:])
            bag = {}
            for cubes in re.finditer(r"(\d+) +([a-z]+)", game):
                num, colour = cubes.groups()
                if colour not in bag or int(num) > bag[colour]:
                    bag[colour] = int(num)
            # we now know the smallest possible bag that works for this game
            # calculate its power
            bag_power = functools.reduce(multiply, bag.values(), 1)
            total_power += bag_power

    return total_power




if __name__ == "__main__":
    print(possible_games(red=12, green=13, blue=14))

    print(f"Total power: {smallest_bag_per_game()}")
