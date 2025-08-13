import os


# Display starting menu
def prompt():
    print("\t\t\tWelcome to my game\n\n\
        You must collect all six items before fighting the boss.\n\n\
        Moves:\t'go {direction}' (travel north, south, east, or west)\n\
        \t'get {item}' (add nearby item to inventory)\n\n")

    input("Press any key to continue...")

# clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


#Map - CREATE MAP
rooms = {
    'Liminal Space': {'North': 'Mirror Maze', 'South': 'Bat Cavern', 'East': 'Bazaar'},
    'Mirror Maze': {'South': 'Liminal Space', 'Item': 'Crystal'},
    'Bat Cavern': {'North': 'Liminal Space', 'East': 'Volcano', 'Item': 'Staff'},
    'Bazaar' : {'West': 'Liminal Space', 'North': 'Meat Locker', 'East': 'Dojo', 'Item': 'Altoids'},
    'Meat Locker' : {'South': 'Bazaar', 'East': 'Quicksand Pit', 'Item': 'Fig'},
    'Quicksand Pit': {'West': 'Meat Locker', 'Item': 'Robe'},
    'Volcano': {'West': 'Bat Cavern', 'Item': 'Elderberry'},
    'Dojo': {'West': 'Bazaar', 'Boss': 'Shadow Man'}
    }

# List of vowels

vowels = ["a", "e", "i", "o", "u"]

# List to track inventory
inventory = []

# Tracks current room
current_room = "Liminal Space"



# Result of the last message

msg = ""

clear()
prompt()


#Gameplay Loop
while True:
    clear()

    #Display info to player
    print(f"You are in {current_room}\nInventory: {inventory}\n{'-' * 27}")

    #Display message
    print(msg)

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

    #Boss Encounter
    if "Boss" in rooms[current_room].keys():
        # Lose - Player has not collect all items
        if len(inventory) < 6:
            print(f"You lost a fight with {rooms[current_room]['Boss']}")
            break
        # Win
        else:
            print(f"You beat {rooms[current_room]['Boss']}!")
            break
    # Accept players move as input
    user_input = input("Enter your move:\n")

    # Split move into words
    next_move = user_input.split(' ')

    # First word is action
    action = next_move[0].title()

    if len(next_move) > 1:
        item = next_move[1:]
        direction = next_move[1].title()

        item = ' '.join(item).title()

    #Moving between rooms
    if action == "Go":

        try:
            current_room = rooms[current_room][direction]
            msg = f"You travel {direction}."

        except:
            msg = f"You can't go that way."
    # Picking up items
    elif action == "Get":
        if item == rooms[current_room]["Item"]:
            if item not in inventory:
                inventory.append(rooms[current_room]["Item"])
                msg = f"{item} retrieved"
                