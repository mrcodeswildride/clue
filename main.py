import os
import random

def cls():
  os.system("cls" if os.name == "nt" else "clear")

def print_game_state():
  cls()

  number = rooms[current_room]["number"]
  print(layout.replace(number, "X", 1))

  print(f"Current room: {current_room}\n")

def get_command():
  while True:
    command = input("Enter a command [look/move/get/drop/guess]: ").lower()

    if command == "":
      print("Invalid command.\n")
    else:
      parts = command.split()

      if parts[0] == "look":
        return "look", None
      elif parts[0] == "move":
        if len(parts) < 2:
          example = random.choice(rooms["hall"]["accessible"])
          print(f"Say what room to move to. Example: move {example}\n")
        elif parts[1] == current_room:
          print("You are already in that room.\n")
        elif parts[1] not in rooms[current_room]["accessible"]:
          print("That room is not accessible from here.\n")
        else:
          return "move", parts[1]
      elif parts[0] == "get":
        if len(parts) < 2:
          example = items[0]
          print(f"Say what item to get. Example: get {example}\n")
        elif parts[1] == current_item:
          print("You already have that item.\n")
        elif parts[1] not in rooms[current_room]["items"]:
          print("That item is not here.\n")
        elif current_item is not None:
          print(f"Your hands are full with the {current_item}.\n")
        else:
          return "get", parts[1]
      elif parts[0] == "drop":
        if current_item is None:
          print("You are not holding anything.\n")
        else:
          return "drop", None
      elif parts[0] == "guess":
        if current_item is None:
          print("You must be holding an item in order to guess.\n")
        elif [current_room, current_item] in guesses:
          print("You already made that guess.\n")
        else:
          return "guess", None
      else:
        print("Invalid command.\n")

def look():
  accessible = rooms[current_room]["accessible"]
  accessible_display = ", ".join(accessible)
  print(f"\nAccessible rooms: {accessible_display}")

  items = rooms[current_room]["items"]
  items_display = ", ".join(items) if len(items) > 0 else "none"
  print(f"Items in room: {items_display}")

  item_display = current_item if current_item is not None else "none"
  print(f"Item you are holding: {item_display}\n")

def guess():
  print("\nYour guess for the murder location and weapon:")
  print(f"Location: {current_room}")
  print(f"Weapon: {current_item}\n")

  if current_room != correct_room and current_item != correct_item:
    print("That guess is wrong. Here is a clue:")

    if random.random() < 0.5:
      print(f"The murder did not take place in the {current_room}.\n")
    else:
      print(f"The murder did not take place with the {current_item}.\n")

    return False
  elif current_room != correct_room:
    print("That guess is wrong. Here is a clue:")
    print(f"The murder did not take place in the {current_room}.\n")
    return False
  elif current_item != correct_item:
    print("That guess is wrong. Here is a clue:")
    print(f"The murder did not take place with the {current_item}.\n")
    return False
  else:
    return True

layout = """
 ___________________________
|           |   |           |
|   2    ___|   |___    3   |
|       |           |       |
|_______|     1     |_______|
|       |           |       |
|       |___     ___|       |
|   4       |   |       5   |
|___________|___|___________|

1-hall, 2-kitchen, 3-bedroom, 4-dining, 5-parlor
"""

items = ["wrench", "knife", "pipe", "gun", "rope"]
random.shuffle(items)

rooms = {
  "hall": {
    "number": "1",
    "accessible": ["kitchen", "bedroom", "dining", "parlor"],
    "items": [items[0]]
  },
  "kitchen": {
    "number": "2",
    "accessible": ["hall", "dining"],
    "items": [items[1]]
  },
  "bedroom": {
    "number": "3",
    "accessible": ["hall", "parlor"],
    "items": [items[2]]
  },
  "dining": {
    "number": "4",
    "accessible": ["hall", "kitchen"],
    "items": [items[3]]
  },
  "parlor": {
    "number": "5",
    "accessible": ["hall", "bedroom"],
    "items": [items[4]]
  }
}

correct_room = random.choice(list(rooms))
correct_item = random.choice(items)
current_room = "hall"
current_item = None
guesses = []
game_over = False

cls()
print()

print("Welcome to Clue! Your goal is to figure out the location and weapon of a recent murder. Use commands to explore the house, find clues, and solve the mystery.\n")
input("Press enter to start. ")

print_game_state()

while not game_over:
  verb, noun = get_command()

  if verb == "look":
    look()
  elif verb == "move":
    current_room = noun
    print_game_state()
  elif verb == "get":
    rooms[current_room]["items"].remove(noun)
    current_item = noun
    print(f"You picked up the {current_item}.\n")
  elif verb == "drop":
    rooms[current_room]["items"].append(current_item)
    print(f"You dropped the {current_item}.\n")
    current_item = None
  elif verb == "guess":
    correct = guess()
    guesses.append([current_room, current_item])

    if correct:
      game_over = True

      if len(guesses) == 1:
        print("You solved the mystery with no clues!")
      else:
        print(f"You solved the mystery with {len(guesses)} guesses!")
