import sys
sys.path.append(r'c:\Users\nzach\OneDrive\00_python\01_text_based_dungeon_learning')

from commands import do_go, do_get, do_open, do_drop, do_inspect, do_look
from player import player
from game_data import rooms, items


def setup_function():
    """Reset player state before each test."""
    player["location"] = "Awakening Chamber"
    player["inventory"] = []
    # Reset any modified game data
    if "Item" not in rooms["The King's Rest"]:
        rooms["The King's Rest"]["Item"] = "Golden Ring"
    rooms["Drowner's Winery"]["Chest_Open"] = False

def test_do_go_valid_direction():
    do_go("South")
    assert player["location"] == "The Grand Hall"

def test_do_go_invalid_direction():
    do_go("West")
    assert player["location"] == "Awakening Chamber"

def test_do_get_valid_item():
    player["location"] = "The King's Rest"
    do_get("Golden Ring")
    assert "Golden Ring" in player["inventory"]
    assert "Item" not in rooms["The King's Rest"]

def test_do_get_invalid_item():
    player["location"] = "The King's Rest"
    do_get("Silver Ring")
    assert "Silver Ring" not in player["inventory"]

def test_do_open_locked_chest_with_keys():
    player["location"] = "Drowner's Winery"
    player["inventory"] = ["Golden Ring", "Silver Ring", "Brass Ring"]
    do_open("chest")
    assert "king's Key" in player["inventory"]
    assert rooms["Drowner's Winery"]["Chest_Open"] == True

def test_do_open_locked_chest_without_keys():
    player["location"] = "Drowner's Winery"
    do_open("chest")
    assert "king's Key" not in player["inventory"]
    assert rooms["Drowner's Winery"]["Chest_Open"] == False

def test_do_drop_item():
    player["inventory"] = ["Golden Ring"]
    do_drop("Golden Ring")
    assert "Golden Ring" not in player["inventory"]
    assert rooms["Awakening Chamber"]["Item"] == "Golden Ring"

def test_do_inspect_item_in_inventory():
    player["inventory"] = ["Golden Ring"]
    do_inspect("Golden Ring")
    # This test only checks if the function runs without error
    # A more robust test would check the output message


def test_do_look():
    do_look(None)
    # This test only checks if the function runs without error
    # A more robust test would check the output message