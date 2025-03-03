from pyexpat.errors import messages

from .grid import Grid
from .player import Player
from . import pickups



player = Player(16, 5)
score = 0
inventory = []
new_command =[]
content_message=""
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

# The floor is lava - for every step you take, you must lose 1 point.--by jahirul
def losse_point(new_comm,current_score):
    init_value = {"d": 0, "a": 0, "w": 0, "s": 0}  # Dictionary to store key counts

    # Count occurrences of each command letter
    for com in new_comm:
        if com in init_value:  # Check if it's a valid key
            init_value[com] += 1

    total_move = sum(init_value.values())  # Calculate total moves
    total_point = current_score - total_move   # Calculate total score points

    print(f"you have total {total_point} score with {total_move}  move")


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print(game_grid)
    print("--------------------------------------")
    print(f"You have {score} points.")

    if command == "i":
        print(content_message)



command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]
    new_command.append(command)
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
   # losse_point(new_command)
    if command in directions:
        dx, dy = directions[command]
        if player.can_move(dx, dy, g):  # Only move if not a wall
            maybe_item = g.get(player.pos_x + dx, player.pos_y + dy)
            player.move(dx, dy)

            if isinstance(maybe_item, pickups.Item):
                # We found an item
                score += maybe_item.value
                inventory.append(maybe_item.name)  # Add to inventory
                if not inventory: # Add to inventory by Jahirul
                    content_message = "There are no items."
                elif len(inventory) == 1:
                    content_message = f"There is 1 item named {inventory[0]}."
                elif len(inventory) == 2:
                    content_message = f"There are 2 items named {inventory[0]} and {inventory[1]}."
                else:
                    content_message = f"There are {len(inventory)} items named {', '.join(inventory[:-1])}, and {inventory[-1]}."


                print(f"You found a {', '.join(inventory[:-1])}, and {inventory[-1]}, with +{score} points.")
                g.clear(player.pos_x, player.pos_y)  # Remove item from grid

        else:
            print("You hit a wall! Move towards other Directions")  # Feedback message to player

    losse_point(new_command,score)
# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
