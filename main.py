import os


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


#Map - CREATE MAP
rooms = {
    "Awakening Chamber": {
        "North": "Passage of King's",
        "South": "The Grand Hall",
        "Description": "You wake sprawled upon cold stone, the absolute darkness broken only by moonlight creeping through ancient diamond-paned window.\nTo the north, a door of blackened steel looms like a giant's shield, its serpent-wrought handle cold as winter's heart and utterly immovable."
        },
    "The Grand Hall": {
        "North": "Awakening Chamber",
        "South": "The Bone Garden",
        "West" : "Moonlight Gallery",
        "East": "Scullery",
        "Description": "Moonbeams slant through high windows, illuminating dust that dance around the great table of black oak, surrounded by chairs toppled in chaos.\nThree stone sentinels preside over this Grand hall. Their bronze, silver, and gold placards tell of rings gifted to a king who reigns eternal."
        },
    "Moonlight Gallery": {
        "North": "The King's Rest",
        "South": "The Royal Armory",
        "West" : "Scriptorium",
        "East": "The Grand Hall",
        "Description": "Silver moonlight light pours through windows that frame the banners that flow through the gallery, portraits whose painted eyes follow your passage.\nMemories of lords and ladies who once walked these halls laid bare."
        },

    "The King's Rest" : {
        "South": "Moonlight Gallery",
        "Item": "Golden Ring",
        "Description": "Power emanates from this great chamber where shadows pool like black blood around the throne of the forgotten king.\nRed satin drapes down over the kings headrest. A Golden Ring rests upon its velvet cushion, radiating light so powerful, you cannot look away."
        },
    "Scriptorium" : {
        "East": "Moonlight Gallery",
        "West": "Scriptorium",
        "Description" : "Bound leather and parchment of ancient histories lie here: chronicles of the three knights, records of the rings, accounts of a realm's glory.\nQuills rest like the bones of their maester, crumbling with the throne of which they served."
        },
    "The Royal Armory": {
        "North": "Moonlight Gallery",
        "Item": "Silver Ring",
        "Description": "Steel in ordered rows where the king's knights once drew their blades, worn shields bearing the heraldry of the forgotten realm.\nA Silver Ring of Sharp Decision gleams. These instruments of royal justice wait perfectly sharp, eternally loyal to masters made of shadow and stone."
        },
    "Scullery": {
        "North": "Provision's Vault",
        "South": "Drowner's Winery",
        "West" : "The Grand Hall",
        "East": "Thrall's Quaters",
        "Description": "Copper vessels hang like the organs of gutted beasts, broken stone basins and dusty cutlery inhabit the uneven cobblestone floor.\nRemnants of the once great feasts that honored their liege now rotting for eternity."
        },
    "Provision's Vault": {
        "South": "Scullery",
        "Description": "Shelves cradle jars whose contents dissolved into dust, torn sacks and empty crates.\nThe air carries scents of spices that once overflowed, preserving nothing but the echo of abundance.\nHere lie the remnants of prosperity that died with the king, rotten by time and forgotten."
        },
    "Thrall's Quaters" : {
        "West": "Scullery",
        "Item": "Brass Ring",
        "Description": "Cots bear the impressions of bodies that once served.\nPersonal effects and torn clothes scattered throughout the dimly lit quarters.\nA brass ring sits beside the dresser, hidden in plain sight."
        },
    "Drowner's Winery": {
        "North": "Scullery",
        "Chest": "Locked Chest",
        "Description": "Stained wine weeps from shattered caskets. The air hangs thick with the phantom sweetness of alcohol lingering in wood.\nUpon the far wall stands an iron chest bearing three sullen sockets.nHere, where sovereignty dissolved into spirits, the final key still waits.",
        "Chest_Contents": "king's Key", # Item given when chest is opened
        "Chest_Open": False # State of the chest
    },
    "Passage of King's": {
        "South": "Awakening Chamber",
        "Description": "You use the Ancient Key and the great steel door swings open. A blast of fresh air hits your face, carrying the scent of damp earth and freedom. You have escaped the Forgotten Manor.",
        "Locked": True, # This room is locked
        "Key": "Ancient Key", # Key required to enter
        "Win": True # Player wins upon entering
        },
    "Bone Garden": {
        "North": "The Grand Hall",
        "Item": "Ancient Key",
        "Description": "Hidden beyond the three great statues lies the catacomb that cradles the final resting place of the forgotten king.\nBone and regalia are fused together, his golden circlet grown into his skull. Clutched in his skeletal hand is a large, ornate key.",
        "Locked": True, # This room is locked
        "Key": "king's Key" # Key required to enter
        }

    }

# List of vowels

vowels = ["a", "e", "i", "o", "u"]

# List to track inventory
inventory = []

# Tracks current room
current_room = "Awakening Chamber"



# Result of the last message

msg = ""

clear()
prompt()


#Gameplay Loop
while True:
    clear()

    #Display info to player
    print(f"You are in {current_room}\nInventory: {inventory}\n{"-" * 27}")
    
    #Display message (moved before description)
    print(msg + "\n")

    #Display room description
    print(rooms[current_room]["Description"] + "\n")

    # Win Condition
    if "Win" in rooms[current_room]:
        print("Congratulations, you have won the game!")
        break

    #Item indicator
    if "Item" in rooms[current_room].keys():
        nearby_item = rooms[current_room]["Item"]
        if nearby_item not in inventory:
            # Plural
            if nearby_item[-1] == "s":
                print(f"You see {nearby_item}")
            # Singular starts with a vowel
            if nearby_item[0] in vowels:
                print(f"You see an {nearby_item}")
            # Singular starts with consonant
            else:
                print(f"You see a {nearby_item}")

    #Boss Encounter - REMOVED

    # Accept players move as input
    user_input = input("Enter your move:\n")

    # Split move into words
    next_move = user_input.split(" ")

    # First word is action
    action = next_move[0].title()

    # Ensure there's a second word for item/direction
    item = ""
    direction = ""
    if len(next_move) > 1:
        item_parts = next_move[1:]
        direction = next_move[1].title() # Only the first word after action for direction
        item = " ".join(item_parts).title() # All words after action for item


    #Moving between rooms
    if action == "Go":
        try:
            target_room_name = rooms[current_room][direction]
            target_room_data = rooms[target_room_name]

            if target_room_data.get("Locked", False): # Check if the target room is locked
                required_key = target_room_data.get("Key")
                if required_key and required_key in inventory:
                    current_room = target_room_name
                    msg = f"You use the {required_key} and travel {direction}."
                else:
                    msg = f"The {target_room_name} is locked. You need a key."
            else:
                current_room = target_room_name
                msg = f"You travel {direction}."

        except KeyError:
            msg = f"You can't go that way."
        except Exception as e:
            msg = f"An unexpected error occurred: {e}"

    # Picking up items
    elif action == "Get":
        try:
            if "Item" in rooms[current_room] and item.lower() == rooms[current_room]["Item"].lower():
                if item not in inventory:
                    inventory.append(rooms[current_room]["Item"])
                    msg = f"{item} retrieved"
                else:
                    msg = f"You already have the {item}."
            else:
                msg = f"Can't find {item}."
        except:
            msg = f"Can't find {item}."

    # Opening chests
    elif action == "Open":
        if item.lower() == "chest" or item.lower() == "locked chest": # Allow "open chest" or "open locked chest"
            if "Chest" in rooms[current_room] and rooms[current_room]["Chest"] == "Locked Chest":
                if not rooms[current_room].get("Chest_Open", False): # Check if chest is not already open
                    # Check for the 3 rings (Golden Ring, Silver Ring, Brass Ring)
                    required_rings = ["Golden Ring", "Silver Ring", "Brass Ring"]
                    has_all_rings = all(ring in inventory for ring in required_rings)

                    if has_all_rings:
                        key_item = rooms[current_room].get("Chest_Contents")
                        if key_item and key_item not in inventory:
                            inventory.append(key_item)
                            rooms[current_room]["Chest_Open"] = True # Mark chest as open
                            msg = f"You use the rings to open the Locked Chest and find a {key_item}!"
                        elif key_item and key_item in inventory:
                            msg = f"The chest is open, but you already have the {key_item}."
                        else:
                            msg = "The chest opens, but it's empty." # Fallback if Chest_Contents is missing
                    else:
                        msg = f"You need all three rings to open the Locked Chest."
                else:
                    msg = "The chest is already open."
            else:
                msg = "There is no chest here to open."
        else:
            msg = "What do you want to open?"

    # Exit game
    elif action == "Exit":
        break
    else:
        msg = "Invalid command." # Ensure msg is always set for invalid commands