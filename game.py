import os
from player import player
from game_data import rooms
import commands

# Display starting menu
def prompt():
    print("			Welcome to The Forgotten Manor\n\n\ Find the three rings of the fallen knights to unlock the secrets of the manor and find your escape.\n\n        Moves:\t\"go {direction}\" (travel north, south, east, or west)\n\n        \t\"get {item}\" (add nearby item to inventory)\n\n        \t\"drop {item}\" (drop an item from your inventory)\n\n        \t\"open {object}\" (open a chest or other container)\n\n        \t\"look\" (examine the room)\n\n        \t\"inspect {item}\" (examine an item in your inventory)\n\n")

    input("Press any key to continue...")

# clear screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Enhanced display function
def display_room_info():
    current_room = player["location"]
    print(f" {current_room}")
    print(f" Inventory: {', '.join(player['inventory']) if player['inventory'] else 'Empty'}")
    
    # Show obvious exits clearly
    exits = [direction for direction in ["North", "South", "East", "West"]
             if direction in rooms[current_room]]
    print(f" Exits: {', '.join(exits)}")
    print("-" * 27)

def start_game():
    clear()
    prompt()

    #Gameplay Loop
    while True:
        clear()
        current_room = player["location"] # Get current room name

        #Display info to player
        display_room_info()
        
        #Display message (moved before description)
        if commands.msg:
            print(commands.msg + "\n")
            commands.msg = "" # Clear message after displaying

        # Progressive revelation
        if not rooms[current_room].get("visited", True):
            print("First time here...\n".title())
            rooms[current_room]["visited"] = True

        #Display room description
        print(rooms[current_room]["Description"] + "\n")

        # Win Condition
        if "Win" in rooms[current_room]:
            print("Congratulations, you have won the game!")
            break

        #Item indicator
        if "Item" in rooms[current_room].keys():
            nearby_item = rooms[current_room]["Item"]
            if nearby_item not in player["inventory"]:
                # Plural
                if nearby_item[-1] == "s":
                    print(f"You see {nearby_item}")
                # Singular starts with a vowel
                elif nearby_item[0].lower() in commands.vowels:
                    print(f"You see an {nearby_item}")
                # Singular starts with consonant
                else:
                    print(f"You see a {nearby_item}")

        #Boss Encounter - REMOVED

        # Accept players move as input
        user_input = input("Enter your move:\n")
        if not user_input:
            continue

        # Split move into words
        next_move = user_input.split(" ")

        # First word is action
        action = next_move[0].title()

        # Ensure there's a second word for item/direction
        target = ""
        if len(next_move) > 1:
            target_parts = next_move[1:]
            target = " ".join(target_parts).title()


        #Moving between rooms
        if action == "Go":
            commands.do_go(target)
        # Picking up items
        elif action == "Get":
            commands.do_get(target)
        # Opening chests
        elif action == "Open":
            commands.do_open(target)
        # Look around
        elif action == "Look":
            commands.do_look(target)
        # Inspect item
        elif action == "Inspect":
            commands.do_inspect(target)
        # Drop item
        elif action == "Drop":
            commands.do_drop(target)
        # Exit game
        elif action == "Exit":
            break
        else:
            commands.msg = commands.handle_command_error(action, target) # Ensure msg is always set for invalid commands
