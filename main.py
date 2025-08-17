import os
from game_data import rooms # Import game data


# Display starting menu
def prompt():
    print("\t\t\tWelcome to The Forgotten Manor\n\n\
        Find the three rings of the fallen knights to unlock the secrets of the manor and find your escape.\n\n\
        Moves:\t\"go {direction}\" (travel north, south, east, or west)\n\
        \t\"get {item}\" (add nearby item to inventory)\n\
        \t\"open {object}\" (open a chest or other container)\n\n") # Added open command

    input("Press any key to continue...")

# clear screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")


#List of vowels
vowels = ["a", "e", "i", "o", "u"]

# Centralize player state
player = {
    "location": "Awakening Chamber",
    "inventory": []
}

# Result of the last message
msg = ""

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

# Smart error handling
def handle_command_error(action, item):
    if action == "Go":
        return "You can't go that way. Try 'go' followed by a valid direction."
    elif action == "Get":
        return f"You can't get '{item}'. Look around to see available items."
    elif action == "Open":
        return "You can't open that. Try 'open chest' if you see one."
    else:
        return "Invalid command. Try: go [direction], get [item], or open [object]."

# --- Command Functions ---

def do_go(direction):
    """Handles player movement."""
    global msg
    current_room_name = player["location"]
    
    if direction in rooms[current_room_name]:
        target_room_name = rooms[current_room_name][direction]
        target_room_data = rooms[target_room_name]

        if target_room_data.get("Locked", False):
            required_key = target_room_data.get("Key")
            if required_key and required_key in player["inventory"]:
                player["location"] = target_room_name
                msg = f"You used the {required_key} and traveled {direction}."
            else:
                msg = "The way is locked. You need the right key."
        else:
            player["location"] = target_room_name
            msg = f"You travel {direction}."
    else:
        msg = handle_command_error("Go", direction)

def do_get(item):
    """Handles picking up items."""
    global msg
    current_room_name = player["location"]
    
    if "Item" in rooms[current_room_name] and item.lower() == rooms[current_room_name]["Item"].lower():
        if item not in player["inventory"]:
            player["inventory"].append(rooms[current_room_name]["Item"])
            msg = f"{item} added to inventory."
        else:
            msg = f"You already have the {item}."
    else:
        msg = handle_command_error("Get", item)

def do_open(item):
    """Handles opening objects like chests."""
    global msg
    current_room_name = player["location"]

    if item.lower() in ["chest", "locked chest"]:
        if "Chest" in rooms[current_room_name] and not rooms[current_room_name].get("Chest_Open", False):
            required_rings = ["Golden Ring", "Silver Ring", "Brass Ring"]
            if all(ring in player["inventory"] for ring in required_rings):
                key_item = rooms[current_room_name].get("Chest_Contents")
                if key_item:
                    player["inventory"].append(key_item)
                    rooms[current_room_name]["Chest_Open"] = True
                    msg = f"You used the rings to open the chest and found a {key_item}!"
                else:
                    msg = "The chest opens, but it's empty."
            else:
                msg = "You need all three rings to open the Locked Chest."
        elif rooms[current_room_name].get("Chest_Open", False):
            msg = "The chest is already open."
        else:
            msg = "There is no chest here to open."
    else:
        msg = handle_command_error("Open", item)


clear()
prompt()


#Gameplay Loop
while True:
    clear()
    current_room = player["location"] # Get current room name

    #Display info to player
    display_room_info()
    
    #Display message (moved before description)
    if msg:
        print(msg + "\n")
        msg = "" # Clear message after displaying

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
            elif nearby_item[0].lower() in vowels:
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
        do_go(target)
    # Picking up items
    elif action == "Get":
        do_get(target)
    # Opening chests
    elif action == "Open":
        do_open(target)
    # Exit game
    elif action == "Exit":
        break
    else:
        msg = handle_command_error(action, target) # Ensure msg is always set for invalid commands