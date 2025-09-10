
#Text Adventure Game
import os
import math
import string
import random

# Rooms with stats: Doors that lead to other rooms, items to pick up, locked doors, text of anything else so say about the room
rooms = []
all_doors = []
all_items = []

# Player's items
items = []
to_get = []

# Player configuration
max_items = 4

# Text to use in names
adjectives = ["brown", "red", "gray", "blue", "teal", "orange", "yellow", "pastel", "green", "pink", "small", "large", "old", "new", "glass", "wood", "steel", "copper", "brass", "iron", "plastic", "wire"]
descriptions = ["There is a stain on the wall.", "There is a potted plant in the corner.", "There is a bricked in window on the left wall.", "The room is cold.", "The room is warm.", "There is a puddle on the ground.", "There is a table in the corner.", "There is a chair in the room."]
objects = ["shoe", "cup", "bucket", "frog", "elephant", "bottle", "cube", "ball", "pyramid"]
furniture = ["Closet", "Dresser", "Wardrobe", "Bookshelf", "Sink", "Trashcan", "Flowerpot", "Vase"]
furniture_descriptions = [" rests along the wall.", " rests in the corner of the room.", " sits across the room.", " sits in the center of the room."]

# Room configurations
num_rooms = 20
items_to_find = 3
lock_prob = 0.4 #<- Probability of adding a key or a locked door to a room
new_door_prob = 0.2 #<- Probability of adding a new door to a room
new_item_prob = 0.4
closet_prob = 0.25
doors_lead_back = False

# Show room numbers (debugging)
show_room_numbers = False

# Special Room stuff
classroom_code_len = 5
code_len = 3
notebook_page_len = 6

# Generation lists
to_lock = []
key_adj_left = adjectives

# Messages
help_message = "Commands:\n - pickup <adj> <item>\n - drop <adj> <item>\n - use <adj> <item>\n - enter <adj> <door>\n - inspect <object> \n - back\n - items\n - help\n - goals\n - endgame"
valve1 = "   /---\   \n  | \ / |  \n  | / \ |  \n   \---/   "
valve2 = "   /---\   \n  | _|_ |  \n  |  |  |  \n   \---/   "
line_max_length = 30 # <- Determines where and if a string should have newline characters added 
doSplitLines = False # (Turned off right now--terminal does this automatically)

# Stored room data
previous_rooms_numbers = [0]

# -------------------------------------------------- Class setup

# Item class (Things you can pick up and use, including target items)
class item:
  def __init__(self, name, adj, description):
    self.name = name
    self.description = description
    self.adj = adj
    all_items.append(self)

  # Notebook subclass
  def make_notebook(self, pages):
    self.pages = pages
    self.current_page = 0
    return self

  def set_page(self, page_num):
      if page_num >= 0 and page_num < len(self.pages):
          self.current_page = page_num

  def open_page(self):
    page_text = self.pages[self.current_page]
    page_lines = get_num_lines(page_text)
        
    clear()
    print("=============================")
    print(page_text)
    # Fill in any missing lines in the page so it is always the same length
    for i in range(notebook_page_len - page_lines):
        print("")
    print("=============================")
    command = input("'next', 'previous' or 'close'  -->    ").rstrip()

    if command == "next":
        self.set_page(self.current_page + 1)
        self.open_page()
    elif command == "previous":
        self.set_page(self.current_page - 1)
        self.open_page()
  
  # Lockbox subclass (Lockboxes can be used without being picked up.)
  def make_lockbox(self, passcode, contents):
    self.locked = True
    self.passcode = (passcode)
    self.contents = contents
    return self
    
  def try_unlock(self):
    clear()
    entry = input("Enter Passcode:  -->    ")
      
    if entry == self.passcode:
        print("The lockbox was unlocked.")
        self.locked = False
        return True
    else:
        print("The lockbox will not unlock.")
        print(entry, self.passcode)
        return False

  def on_use(self):
    global items

    if self.locked:
        self.try_unlock()
    
    if not self.locked:
        clear()
        # Print a list of contents
        print("Lockbox contents: ")
        for item in self.contents:
            print(" - " + item.adj + " " + item.name)
            
        # Enter commands
        commands = input("'pickup <adj> <item>' or 'close'  -->    ").rstrip().split(" ")
            
        if commands[0] == "pickup" and len(items) < max_items:
            for item in self.contents:
                if item.adj == commands[1] and item.name == commands[2]:
                    self.contents.remove(item)
                    items.append(item)
                    print("Picked up " + item.adj + " " + item.name)
                    break  
        else:
          clear()
          print("You cannot carry more than " + str(max_items) + " items at a time.")
          input("Type any key to continue -->    ")

  # Valve subclass
  def make_valve(self, target, turn_amount, action_text):
    self.target = target
    self.action_text = action_text
    self.turn_amount = turn_amount
    return self

  def use_valve(self):
    clear()
    print("You place the valve in the " + self.target.name.lower() + ".")
    print(valve1)
    
    turn = input("Type 'turn' to turn the valve  -->    ")
    if turn == "turn":
      clear()
      print("")
      print(valve2)
      self.target.locked = False
      input(self.action_text)
      items.remove(self)

# Door class
class door:
  def __init__(self, dest, adj, locked=False, link=None):
    self.dest = dest
    self.locked = locked
    self.adj = adj
    self.link = None
    all_doors.append(self)

  # Unlocks the door if the player has a key that matches
  def unlock(self, key):
    if self.locked == True:
      # Go through the player's items and see if they have a key with a matching adjective.
      if key.name == "key" and key.adj == self.adj:
        self.locked = False
        if self.link is not None:
          self.link.locked = False
        items.remove(key)
      
      # Determine the return message
      if self.locked == True:
        return "You do not have the correct key."
      else:
        return "The " + self.adj + " door was unlocked."
    else:
      return "This door is already unlocked."
    
# Fixture class
class fixture:
  def __init__(self, name, description):
    self.description = description
    self.name = name
    self.category = None
    
  # Closet subclass
  def make_closet(self, contents, locked=False, locked_message=""):
    self.contents = contents
    self.category = "closet"
    self.locked = locked
    self.locked_message = locked_message
    return self
   
  # Poster subclass
  def make_poster(self, text, width=20):
    self.category = "poster"
    self.text = text
    self.width = width
    return self
    
  # Determines what happens when you 'inspect' a fixture
  def on_use(self):
    if self.category == "closet":
      clear()
      if not self.locked:
        # Print a list of contents
        if len(self.contents) > 0:
          print(self.name + " contents: ")
          for item in self.contents:
              print(" - " + item.adj + " " + item.name)
              
          # Enter commands
          commands = input("'pickup <adj> <item>' or 'close'  -->    ").rstrip().split(" ")
              
          if commands[0] == "pickup" and len(items) < max_items:
              for item in self.contents:
                  if item.adj == commands[1] and item.name == commands[2]:
                      self.contents.remove(item)
                      items.append(item)
                      print("Picked up " + item.adj + " " + item.name)
                      break   
          else:
            clear()
            print("You cannot carry more than " + str(max_items) + " items at a time.")
            input("Type any key to continue -->    ")
        else:
          input("The " + self.name.lower() + " is empty. -->    ")
      else:
        input(self.locked_message)
        
    # Action if self is a poster: Display message
    elif self.category == "poster":
      lines = self.text
      bar = "-" * self.width
      clear()
      print(bar)
      
      # Fill out the lines, adding padding so the poster remains rectangular
      for line in lines:
        message = "| " + line
        while len(message) < len(bar) - 2:
          message += " "
        print(message + " |")

      print(bar)
        
      # Prompt continue
      input("-->    ")
    
    else:
      input("There is nothing there.  -->    ")

# Room class
class room:
  def __init__(self, description, doors=[], items=[], fixtures=[]):
    self.description = description
    self.doors = doors
    self.items = items
    self.fixtures = fixtures

  # DOOR FUNCTIONS
  def add_door(self, door):
    self.doors.append(door)

  def get_door(self, adj):
    chosen_door = None
    for door in self.doors:
      if door.adj == adj:
        chosen_door = door
    return chosen_door
  
  def get_locked_doors(self):
    locked_doors = []
    for door in self.doors:
      if door.locked == True:
        locked_doors.append(door)
    return locked_doors
    
  def shuffle_doors(self):
    random.shuffle(self.doors)

  # ITEM FUNCTIONS
  def add_item(self, item):
    self.items.append(item)

  def remove_item(self, item):
    self.items.remove(item)

  def get_item(self, name, adj):
    chosen_item = None
    for item in self.items:
      if item.name == name and item.adj == adj:
        chosen_item = item
    return chosen_item
    
  def shuffle_items(self):
    random.shuffle(self.items)
    
  # FIXTURE FUNCTIONS
  def get_fixture(self, name):
    chosen_fixture = None
    for fixture in self.fixtures:
      if fixture.name.lower() == name:
        chosen_fixture = fixture
    return chosen_fixture

# ----------------------------------------------------- Functions
# Clears the terminal
def clear():
  os.system("cls")

# Has a probability of returning true; a way to make floats into probabilities
def if_prob(probability):
  number = random.random()
  if probability > number:
    return True
  else:
    return False

# Should a word be preceded by a or an?
def a_or_an(string):
  vowels = ["a", "e", "i", "o", "u"]
  if string[0] in vowels:
    return "an"
  else:
    return "a"
  
# Find a specific item the player has
def get_item(name, adj):
  chosen_item = None
  for item in items:
    if item.name == name:
      if item.adj == adj:
        chosen_item = item
  return chosen_item
  
# Turn a list into a string
def as_string(list1):
  string = ""
  for item in list1:
    string += str(item)
  return string

# Determines whether a player has an item (this one uses the item class and returns bool)
def does_player_have(item):
  adj = item.adj
  name = item.name

  matches = False

  for item in items:
    if item.name == name:
      if item.adj == adj:
        matches = True
        break
  
  return matches

# Splitting up text lines function
def split_lines(text):
  if len(text) > line_max_length and doSplitLines: #< - Turns this off; wasn't neccessary as the terminals do this themselves better
    times_to_split = math.floor(len(text) / line_max_length)
    words = text.split(" ")
    result_text = ""
    characters_indexed = 0
    
    for word in words:
      characters_indexed += len(word)
      
      # Insert newline whenever we get through enough characters
      if characters_indexed > line_max_length:
        index = words.index(word)
        words.insert(index, "\n")
        characters_indexed = 0
      
    for word in words:
      if word[len(word) - 1] == "\n":
        result_text = result_text + word
      else:
        result_text = result_text + word + " "
      
    return result_text
    
  else:
    return text

# Gets the number of lines in a text
def get_num_lines(text):
    num_lines = 1
    for char in text:
        if char == "\n":
            num_lines += 1
    return num_lines
    
# Randomly selects characters out of a list to create a passcode
def generate_passcode(length, chars=string.ascii_lowercase):
  passcode = ""
  while len(passcode) < length:
    new_char = random.choice(chars)
    if not new_char in passcode: 
      passcode += new_char
  return passcode

# ----------------------------------------------------------------------------------------------Special Items

# Key use protocol
def use_key(room, key):

  clear()
  # If there are any doors to unlock, have the player select which door to unlock.
  if len(room.get_locked_doors()) > 0:

    # Try to get the door that matches the adjective of the key
    selected_door = room.get_door(key.adj)

    if selected_door is not None:
      message = selected_door.unlock(key)
      print(message)
    else:
      print("The key does not fit in any of the doors.")
  else:
    print("There are no doors to unlock in this room.")

#-------------------------------------------------------------------------------RANDOM GENERATION
    
# Generates a destination for a door
def nxt_room_num(dont_pick_list, rand=False):
  global rooms
  global all_doors
  
  found = None
  
  for list_room in rooms:
    is_empty = True
    #1. Check if there is anything in the room
    if list_room.description == "":
      #2. Check if there are any doors that enter on this room (has it already been claimed?)
      for list_door in all_doors:
        if list_door.dest == rooms.index(list_room):
          is_empty = False
    else:
      is_empty = False
      
    if is_empty:
      found = rooms.index(list_room)
      break
  
  # Create a door to a random room if there are no empty rooms left (if on)
  if found == None and (doors_lead_back or rand):
    found = random.randint(0, num_rooms - 1)
    while found in dont_pick_list:
      found = random.randint(0, num_rooms - 1)
  return found
  
# Fills out a new room with keys and such
def setup_room(new_room):
  global to_lock
  global rooms
  global key_adj_left

  new_description = ""
  room_items = []
  dont_pick_nums = [rooms.index(new_room)] #<- Room numbers that the doors should not go to, starting with this one.
  room_doors = []
  keys_added = 0
  door_availible_adjs = list(adjectives)

  # Determine room description + add it in: Needed so room finder for door function will not choose the same room
  new_description = random.choice(descriptions)
  new_room.description = new_description

  # Add doors, locked doors and keys IF there are still rooms to be added beyond this one.
  if rooms.index(new_room) < num_rooms - 1:
    # Randomize chance for a key; if so, add to the list of doors to lock.
    if if_prob(lock_prob) and len(key_adj_left) > 0:
      # Get an adjective from the remaining
      key_adj = random.choice(key_adj_left)
      key_adj_left.remove(key_adj)
      keys_added += 1

      # Create the key
      new_key = item("key", key_adj, "on the ground")
      room_items.append(new_key)

      # Save it to the list of doors to add locks to.
      to_lock.append(key_adj)

    # Randomize chance for a locked door; go through each key needing a door and probability it to get a door.
    if len(to_lock) + keys_added > 2: #<- Reduce probability that key is in same room as door
      for adj in to_lock:
        if if_prob(lock_prob):
            dest = nxt_room_num(dont_pick_nums)
            new_door = door(dest, adj, True)
            room_doors.append(new_door)
            dont_pick_nums.append(dest)
            to_lock.remove(adj)

    # Will create at least one door, or potentially more
    while len(door_availible_adjs) > 0 and (len(room_doors) == 0 or if_prob(new_door_prob)):
      # Make sure no two doors in a room have the same adjectives
      door_adj = random.choice(door_availible_adjs)
      door_availible_adjs.remove(door_adj)
      # Set the door's destination and create the door
      new_dest = nxt_room_num(dont_pick_nums)
      room_doors.append(door(new_dest, door_adj, False))
      dont_pick_nums.append(new_dest)

  # Probability for a closet
  if if_prob(closet_prob):
    # Probablility for a different item in the closet
    if if_prob(new_item_prob):
      room_items.append(item(random.choice(objects), random.choice(adjectives), "on the ground"))
    closet_type = random.choice(furniture)
    new_closet = fixture(closet_type, "A " + closet_type.lower() + random.choice(furniture_descriptions))
    new_closet.make_closet(room_items) #<- Move room items into the closet
    room_items = [] 
    new_room.fixtures = [new_closet]
    
  # Add in other items
  while if_prob(new_item_prob):
    room_items.append(item(random.choice(objects), random.choice(adjectives), "on the ground"))

  # Add doors and items
  new_room.doors = room_doors
  new_room.items = room_items
  
  # Shuffle doors and items
  new_room.shuffle_doors()
  new_room.shuffle_items()

  return new_room

# Creates the randomly generated rooms. Or not...
def create_rooms():
  global rooms
  global all_doors

  # Setup numbers for special rooms
  fountain_room_num = random.randint(4, num_rooms - 1)
  theater_room_num = random.randint(6, num_rooms - 1)
  closet_room_num = random.randint(4, num_rooms - 1)
  class_room_num = random.randint(8, num_rooms - 5)
  
  # Create the specified number of rooms
  for room_number in range(num_rooms):
    rooms.append(room("", [], []))
    
  # Set up the rooms in order
  for index in range(len(rooms)):
    if index == fountain_room_num:
        fountain_room(rooms[index])
    elif index == theater_room_num:
        little_theater(rooms[index])
    elif index == closet_room_num:
        closet(rooms[index])
    elif index == class_room_num:
        classroom(rooms[index])
    else:
        setup_room(rooms[index])
    
  # Get rid of any doors that do not open on a room
  for list_room in rooms:
    for list_door in list_room.doors:
      if list_door.dest == None:
        all_doors.remove(list_door)
        list_room.doors.remove(list_door)

# ---------------------------------------------------------------------- Special Room Setups
def fountain_room(new_room):
  
  passcode = generate_passcode(code_len)
  
  notebook = item("notebook", "frayed", "on the marble rim of the fountain")
  notebook.make_notebook(["The passcode is " + passcode])
  
  lockbox = item("lockbox", "army-green", "that requires a 3-letter code, on the floor")
  lockbox.make_lockbox(passcode, [item("key", "ornate", "in the lockbox.")])

  nxt_room_num([rooms.index(new_room)])
  
  new_room.description = split_lines("The room is rather large. Under its fluorescent lights, a ring of planter beds filled with dandelions surrounds the ornate marble fountain in the center of the room. Your attention is immediately drawn to what lays precariously on the rim of the fountain.")
  
  # Create the door to the room + add a corresponding door into this room
  dest = nxt_room_num([rooms.index(new_room)], True)
  new_door = door(dest, "ornate", True)
  link_door = door(rooms.index(new_room), "ornate", True, link=new_door)
  new_door.link = link_door
  
  new_room.add_door(new_door)
  rooms[dest].add_door(link_door)
  
  new_room.add_item(notebook)
  new_room.add_item(lockbox)
  
def little_theater(new_room):
  pass1 = generate_passcode(code_len)
  pass2 = generate_passcode(code_len)
  
  notebook = item("notebook", "purple", "in a seat").make_notebook(["\n  SCRIPT", 
                                                                    "Choose Wisely\nRED:  " + pass1 + "\nBLUE:  " + pass2, 
                                                                    "Shall I compare thee to a summer's day?\nThou art more lovely and more temperate;\nRough winds do shake the darling buds of May,\nAnd summer's lease hath all too short a date:\nSometime too hot the eye of heaven shines,\nAnd often is his gold complexion dimm'd;", 
                                                                    "And every fair from fair sometime declines,\nBy chance or nature's changing course untrimm'd;\nBut thy eternal summer shall not fade\nNor lose possession of that fair thou owest;\nNor shall Death brag thou wander’st in his shade,\nWhen in eternal lines to time thou growest:",
                                                                    "So long as men can breathe or eyes can see,\nSo long lives this and this gives life to thee.\n\n– William Shakespeare"
                                                                    ])

  blue_box = item("lockbox", "blue", "on the stage").make_lockbox(pass2, [])
  red_box = item("lockbox", "red", "on the stage").make_lockbox(pass1, [])
  
  key = item("key", "black", "in the lockbox")
  
  dest = nxt_room_num([rooms.index(new_room)], True)
  new_door = door(dest, "black", True)
  link_door = door(rooms.index(new_room), "black", True, link=new_door)
  new_door.link = link_door
  
  room_doors = [new_door]
  rooms[dest].add_door(link_door)
  
  room_items = [blue_box, red_box]
  
  random.choice(room_items).contents = [key]

  room_items.append(notebook)
  
  new_room.description = split_lines("The room is rectangular, with a small, curved bank of red velvet seats facing a small wooden stage to the right. The walls are painted black.")
  new_room.doors = room_doors
  new_room.items = room_items
  
def closet(new_room):
  potential_items = [("coat", "mink", "hanging on the bar"),
                    ("coat", "fur", "hanging on the bar"),
                    ("jacket", "ski", "hanging on the bar"),
                    ("jacket", "leather", "hanging on the bar"),
                    ("sweater", "wool", "hanging on the bar"),
                    ("sneakers", "new", "on the ground")]
  room_items = []
  for i in range(random.randint(1, 3)):
    selected_set = random.choice(potential_items)
    new_item = item(selected_set[0], selected_set[1], selected_set[2])
    room_items.append(new_item)
    
  new_room.description = split_lines("The room is more of a closet, and there is a wooden bar extending across its width on which to hang coats of sorts. It is very dusty inside.")
  new_room.items = room_items

def classroom(new_room):
  print(rooms.index(new_room))
  # Create a password for the lockbox
  password = list(generate_passcode(5, string.ascii_letters))
  password.sort()
  # Create a "key" of the remaining letters
  ltrs = string.ascii_uppercase + string.ascii_lowercase
  for index in range(len(ltrs)):
    if ltrs[index] in password:
      ltrs = ltrs.replace(ltrs[index], " ")

  
  dest1 = nxt_room_num([rooms.index(new_room)], True)
  dest2 = nxt_room_num([rooms.index(new_room)], True)
  door1 = door(dest1, "metal", False)
  door2 = door(dest2, "rainbow", True)
  link_door1 = door(rooms.index(new_room), "metal", False, link=door1)
  link_door2 = door(rooms.index(new_room), "purple", True, link=door2)
  door1.link = link_door1
  door2.link = link_door2
  
  key = item("key", "toy", "on the ground")
  crayon = item("crayon", random.choice(["red", "blue", "yellow"]), "on the ground")
  valve = item("valve", "red", "on the ground").make_valve(None, 90, "The water drains out of the sink.  -->    ")
  lockbox = item("lockbox", "wooden", "on the ground").make_lockbox(as_string(password), [valve])
  notebook = item("notebook", "composition", "on a table in the room").make_notebook(["Remember your ABC's!"])
  
  sink = fixture("Sink", "A small sink sits next to the locker.").make_closet([key], True, "The sink is full of water. -->    ")
  locker = fixture("Locker", "To your left is a short, blue locker.").make_closet([lockbox])
  cubbyhole = fixture("Cubbyhole", "On the far end of the room is a wooden cubbyhole.").make_closet([])
  #trashcan = fixture("Trashcan", "A metal trashcan sits under the sink.").make_closet([])

  valve.target = sink

  rem = len(ltrs)
  tab = "      "
  poster = fixture("Poster", "A faded poster is tacked to the wall.").make_poster([
    tab + "THE LETTERS:",
    "",
    tab + ltrs[0:int(rem/4)],
    tab + ltrs[int(rem/4):int(rem/2)],
    tab + ltrs[int(rem/2):int(3*rem/4)],
    tab + ltrs[int(3*rem/4):rem]
  ], width=30)
  
  choice = random.choice([locker, cubbyhole])
  new_items = choice.contents
  new_items.append(crayon)
  choice.contents = new_items
  
  room_items = [notebook]
  room_fixtures = [locker, cubbyhole, sink, poster]
  room_doors = [door1, door2]
  rooms[dest1].add_door(link_door1)
  rooms[dest2].add_door(link_door2)
  
  new_room.description = split_lines("The room gives a semblance of a kindergarden classroom. The walls are coated with multicolored paint, dulled and chipped with age. Small tables dot the room, along with a set of cheap plastic chairs.")
  new_room.items = room_items
  new_room.fixtures = room_fixtures
  new_room.doors = room_doors
  
#------------------------------------------------------------------------ User Interaction/Commands
  
# Function for opening a room and accepting player inputs 
def open_room(room_number):
  global items
  global previous_rooms_numbers

  clear()
  print("You enter the room.")

  # Get the information on the room
  room = rooms[room_number]
  room_doors = room.doors
  room_items = room.items
  room_fixtures = room.fixtures

  # Print the room's description
  print(room.description + "\n")
  
  # Generate fixture text
  if len(room_fixtures) > 0:
    for fixture in room_fixtures:
      print(fixture.description)
    print("")

  # Generate text for doors
  if len(room_doors) > 0:

    bullet = ""

    # Procedure for more than 1 door: State the number, and introduce each door with a bullet.
    if len(room_doors) > 1:
      print("There are " + str(len(room_doors)) + " doors. ")
      bullet = " - "

    for door in room_doors:
      # Check if the door is locked. If so, add a locked message
      locked_text = ""
      if door.locked == True:
        locked_text = " It is locked."

      # Print the final message.
      print(bullet + "There is a " + str(door.adj) + " door." + locked_text)

  # Generate text for items
  if len(room_items) > 0:
    for item in room_items:
      print("There is " + a_or_an(item.adj) + " " + item.adj + " "+ item.name + " " + item.description + ".")

  # Ask for inputs
  command = input("-->  ").rstrip().lower()
  commands = command.split(" ")

  # Handles single-word commands
  if len(commands) == 1:
    # Help command: Bring up commands menu list
    if command == "help":
      clear()
      print(help_message)
      input("Type any key to continue -->  ")
      open_room(room_number)

    # Back command: open previous room
    elif command == "back":
      if len(previous_rooms_numbers) > 1:
        # Get the last room from the top of the "stack"
        to_enter_number = previous_rooms_numbers[len(previous_rooms_numbers) - 1]

        # Get rid of the number and open the room
        previous_rooms_numbers.remove(to_enter_number)
        open_room(to_enter_number)
      else:
        open_room(0)

    # Items command: Prints a list of the player's items
    elif command == "items":
      clear()
      print("Your items: ")
      for item in items:
        print(" - " + item.adj + " " + item.name)
      input("Type any key to continue -->  ")
      open_room(room_number)

    elif command == "endgame":
      print("The game has been terminated.")
    
    elif command == "goals":
      clear()
      print("Your goals: ")
      num_req_met = 0

      for item in to_get:
        met = does_player_have(item)

        if met:
          print(" - " + item.adj + " " + item.name + " (Has)")
          num_req_met += 1
        else:
          print(" - " + item.adj + " " + item.name)

      # If player has all 3 items: End game
      if num_req_met == items_to_find:
        print("Congratulations! You have found all 3 items.")
      else:
        input("Type any key to continue -->  ")
        open_room(room_number)

    # If command is illegible, reopen the room
    else:
      open_room(room_number)
      
  # Handles 2-word Use commands: Inspect fixtures
  elif len(commands) == 2:
    action = commands[0]
    obj = commands[1]
    
    if action == "inspect" and room.get_fixture(obj):
      room.get_fixture(obj).on_use()
    
    open_room(room_number)
      
  # Handles 3-word commands: Pickup, Drop, Use, Enter
  elif len(commands) == 3:
    action = commands[0]
    adj = commands[1]
    object = commands[2]

    # Picks up an item put of the room if it exists and the player has room.
    if action == "pickup":
      chosen_item = room.get_item(object, adj)

      if chosen_item is not None:
        if len(items) < max_items:
          room.items.remove(chosen_item)
          items.append(chosen_item)
        else:
          clear()
          print("You cannot carry more than " + str(max_items) + " items at a time.")
          input("Type any key to continue -->    ")
          
      open_room(room_number)
  
    # Drops an item in the room
    elif action == "drop":
      chosen_item = get_item(object, adj)
      
      if chosen_item is not None:
        chosen_item.description = "on the ground"
        items.remove(chosen_item)
        room.add_item(chosen_item)

      open_room(room_number)

    # Uses an item
    elif action == "use":
      # Make sure the player actually has the requested item
      if get_item(object, adj): 
        # Key function
        if object == "key":
          use_key(room, get_item(object, adj))
        elif object == "notebook":
           get_item(object, adj).open_page()
        elif object == "lockbox":
          get_item(object, adj).on_use()
        elif object == "valve":
          get_item(object, adj).use_valve()
      elif object == "lockbox" and room.get_item("lockbox", adj):
        room.get_item("lockbox", adj).on_use()
        
      input("Type any key to continue -->    ")
      open_room(room_number)

    # Door-entering protocol
    elif action == "enter" and object == "door":
      # Find the door
      chosen_door = room.get_door(adj)
  
      if chosen_door is not None:
        # Door locked message
        if chosen_door.locked == True:
          clear()
          input("The " + chosen_door.adj + " door is locked. -->    ")
          open_room(room_number)

        # Door is unlocked 
        else:
          # If the room the door is trying to take you to actually exists, open that room.
          if chosen_door.dest >= 0 and chosen_door.dest < len(rooms):
            if previous_rooms_numbers[len(previous_rooms_numbers) - 1] != room_number:
              previous_rooms_numbers.append(room_number)
            open_room(chosen_door.dest)
          else:
            open_room(room_number)
      else:
        open_room(room_number)
    
    # Debugging command to see all the rooms-DEVS ONLY
    elif action == "sudo" and adj == "open":
      open_room(int(object))

    # If command is illegible, reopen the room
    else:
      open_room(room_number)

  # If command is not any useful length, reopen the room.
  else:
    open_room(room_number)

# Determines the 3 items you must find in the Rooms
def get_target_items():
    if len(all_items) >= items_to_find:
      selections = []
      # Choose 3 items THAT ARE NOT IDENTICAL and return them in a list - NO KEYS
      for item_num in range(items_to_find):
        chosen_item = random.choice(all_items)
        while chosen_item in selections or chosen_item.name == "key" or chosen_item.name == "valve":
          chosen_item = random.choice(all_items)
        selections.append(chosen_item)

      return selections
    else:
        return None

# Game startup function
def start_game():
  global to_get

  # Game setup
  create_rooms()
  to_get = get_target_items()

  # Start messages
  print("Welcome to the Rooms. You must find: ")
  for target in to_get:
    print(" - " + target.adj + " " + target.name)
  print(help_message)
  input("Type 'start' to start.  -->   ")

  open_room(0)

start_game()
