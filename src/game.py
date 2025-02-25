from .grid import Grid
from .player import Player
from . import pickups



player = Player(16, 5)
score = 0
inventory = []
directions = {
    "d": (1, 0),   # Right
    "a": (-1, 0),  # Left
    "w": (0, -1),  # Up
    "s": (0, 1)    # Down
}

g = Grid()
g.set_player(player)
g.make_walls()
pickups.randomize(g)


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)


command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]

    if command == "d" and player.can_move(1, 0, g):  # move right
        # TODO: skapa funktioner, så vi inte behöver upprepa så mycket kod för riktningarna "W,A,S"
        maybe_item = g.get(player.pos_x + 1, player.pos_y)
        player.move(1, 0)
    # jahirul-move
    elif command == "a" and player.can_move(-1, 0, g):  # Move Left
        maybe_item = g.get(player.pos_x - 1, player.pos_y)
        player.move(-1, 0)

    elif command == "w" and player.can_move(0, -1, g):  # Move Up
        maybe_item = g.get(player.pos_x, player.pos_y - 1)
        player.move(0, -1)

    elif command == "s" and player.can_move(0, 1, g):  # Move Down
        maybe_item = g.get(player.pos_x, player.pos_y + 1)
        player.move(0, 1)

    if command in directions:
        dx, dy = directions[command]
        if player.can_move(dx, dy, g):  # Only move if not a wall
            maybe_item = g.get(player.pos_x + dx, player.pos_y + dy)
            player.move(dx, dy)

            if isinstance(maybe_item, pickups.Item):
                # We found an item
                score += maybe_item.value
                inventory.append(maybe_item.name)  # Add to inventory
                print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
                g.clear(player.pos_x, player.pos_y)  # Remove item from grid

        else:
            print("You hit a wall! Move towards others Direction")  # Feedback to player


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
