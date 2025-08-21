from player import player
from game_data import rooms, items

#List of vowels
vowels = ["a", "e", "i", "o", "u"]

# Result of the last message
msg = ""

# Smart error handling
def handle_command_error(action, item):
    if action == "Go":
        return "You can't go that way. Try 'go' followed by a valid direction."
    elif action == "Get":
        return f"You can't get '{item}'. Look around to see available items."
    elif action == "Open":
        return "You can't open that. Try 'open chest' if you see one."
    elif action == "Drop":
        return f"You can't drop '{item}'. You can only drop items in your inventory."
    elif action == "Inspect":
        return f"You can't inspect '{item}'. You can only inspect items in your inventory."
    else:
        return "Invalid command. Try: go, get, drop, open, look, or inspect."

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
            del rooms[current_room_name]["Item"]
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

def do_look(item):
    """Handles looking around the room."""
    global msg
    current_room_name = player["location"]
    msg = rooms[current_room_name]["Description"]
    if "Item" in rooms[current_room_name].keys():
        nearby_item = rooms[current_room_name]["Item"]
        if nearby_item not in player["inventory"]:
            # Plural
            if nearby_item[-1] == "s":
                msg += f"\nYou see {nearby_item}"
            # Singular starts with a vowel
            elif nearby_item[0].lower() in vowels:
                msg += f"\nYou see an {nearby_item}"
            # Singular starts with consonant
            else:
                msg += f"\nYou see a {nearby_item}"

def do_inspect(item):
    """Handles inspecting an item in the inventory."""
    global msg
    if item in player["inventory"]:
        msg = items[item]["description"]
    else:
        msg = handle_command_error("Inspect", item)

def do_drop(item):
    """Handles dropping an item from the inventory."""
    global msg
    current_room_name = player["location"]
    if item in player["inventory"]:
        player["inventory"].remove(item)
        rooms[current_room_name]["Item"] = item
        msg = f"You dropped the {item}."
    else:
        msg = handle_command_error("Drop", item)
