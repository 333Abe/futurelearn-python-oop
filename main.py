from room import Room
from item import Item
from item import Weapon
from item import Furniture
from item import Key
from character import Enemy
import time
from tkinter import *


mainDisplayList=["You're a lowly kitchen servant in the great house.", "Do what you're told or else."]

def typewriter(typewriterText): #accepts a list of strings
    displayText=""
    #this function will make the text flow out like it's being typed into the screen like you see in classic rpgs
    #the label used to display this will need to display over multiple lines by using the newline \n thingy
    for i in range(len(typewriterText)):
        global guiMainDisplay
        displayVariable = StringVar()
        for letter in typewriterText[i]:
            guiMainDisplay.grid_forget()
            displayText+=letter
            displayVariable.set(displayText)
            guiMainDisplay=Label(gui, textvariable=displayVariable, font=("FreeSerif", 18), bd=3, relief=SUNKEN, bg="#EBEBD3")
            guiMainDisplay.grid(row=10, column=0, columnspan=6, padx=5, pady=10, sticky=W+E)
            gui.update()
            time.sleep(0.01)
        displayText+="\n"
    return

def move(command):
    global current_room
    global mainDisplayList
    if current_room == current_room.move(command):
        mainDisplayList = ["You can't go that way"]
        typewriter(mainDisplayList)
    else:
        current_room = current_room.move(command)
        look()

def look():
    #send room details, inhabitant details, and item details to typewriter
    global inhabitant
    global current_room
    global mainDisplayList
    mainDisplayList=[]
    mainDisplayList.append(current_room.get_details())
    inhabitant = current_room.get_character()
    if inhabitant is not None:
        mainDisplayList.append("[Character]: " + inhabitant.get_name())
    items = current_room.get_item()
    if len(items)>0:
        roomItems="[Items]: "
        for item in items:
            roomItems += item.get_name() + ", "
        roomItems = roomItems[:-2]
        mainDisplayList.append(roomItems)
        for item in items:
            if isinstance(item, Furniture) and item.get_isOpen() == True:
                contents = item.get_contents()
                furnitureItems = "\n[{} items]: ".format(item.get_name())
                if len(contents)>0:
                    for fitem in contents:
                        furnitureItems += fitem.get_name() + ", "
                    furnitureItems = furnitureItems[:-2]
                else:
                    furnitureItems += "the {} is empty".format(item.get_name())
                mainDisplayList.append(furnitureItems)
    typewriter(mainDisplayList)

def get():
    thing = guiEntrybox.get()
    items = current_room.get_item()
    itemExists = False
    fitemExists = False
    mainDisplayList=[]
    if len(items)>0:
        for item in items:
            if item.get_name() == thing:
                itemExists = True
                break
    if itemExists == True:
        if isinstance(item, Furniture):
            mainDisplayList.append("you can't take that")
        else:
            holding.append(item)
            current_room.set_item(item)
            mainDisplayList.append("You collect: " + item.get_name())
    if len(items)>0:
        for item in items:
            if isinstance(item, Furniture):
                contents = item.get_contents()
                for fitem in contents:
                    if fitem.get_name() == thing:
                        fitemExists = True
                        break
                if fitemExists == True:
                    holding.append(fitem)
                    item.set_contents(fitem)
                    mainDisplayList.append("You collect: " + fitem.get_name() + " from the {}".format(item.get_name()))
    elif itemExists == False and fitemExists == False:
        mainDisplayList.append("You can't see that here...")
    typewriter(mainDisplayList)

def drop():
    thing = guiEntrybox.get()
    itemExists = False
    mainDisplayList=[]
    if len(holding)>0:
        for item in holding:
            if item.get_name() == thing:
                itemExists = True
                break
    if itemExists == True:
        holding.remove(item)
        current_room.set_item(item)
        mainDisplayList.append("You drop: " + item.get_name())
    else:
        mainDisplayList.append("You're not holding that...")
    typewriter(mainDisplayList)

def use(item):#opens and closes doors or furniture, or uses an item if that's possible
    global holding
    thing = guiEntrybox.get()
    items = current_room.get_item()
    itemExists = False
    mainDisplayList=[]
    if len(items)>0:# are there items in the room?
        for item in items:
            if item.get_name() == thing: # does an item in the room match what was typed?
                itemExists = True
                if isinstance(item, Weapon):
                    mainDisplayList.append("You need to being holding the {} to use it.".format(item.get_name()))
                elif isinstance(item, Furniture): # furniture can't be held and can only be opened where it is
                    if item.get_locked() == True:
                        mainDisplayList.append("The {} is locked.".format(item.get_name()))
                    elif item.get_locked() == False:
                        if item.get_isOpen() == True:
                            mainDisplayList.append("The {} is already open.".format(item.get_name()))
                        elif item.get_isOpen() == False:
                            item.set_isOpen("open")
                            mainDisplayList.append("You open the {} and ".format(item.get_name()) + item.get_useText())
                elif isinstance(item, Item):
                    mainDisplayList.append("You need to being holding the {} to use it.".format(item.get_name()))
    for item in holding: # are you holding the item?
        if item.get_name() == thing:
            itemExists = True
            if isinstance(item, Weapon):
                inhabitant = current_room.get_character()
                if inhabitant is not None:
                    mainDisplayList.append(inhabitant.fight(item))
                else:
                    mainDisplayList.append("There's noone here to use the {} on".format(item))
            elif isinstance(item, Key):
                if item.get_lockForKey() in items:
                    item.get_lockForKey().set_locked("unlocked")
                    mainDisplayList.append("The key fits the {}. {}".format(item.get_lockForKey().get_name(), item.get_useText()))
            else:#isinstance(item, Item):
                mainDisplayList.append("i still haven't coded how to use normal items")
    if itemExists == False:
        mainDisplayList.append("You can't see that here...")
    typewriter(mainDisplayList)

def examine():
    # used to examine an item you're holding or a piece of furniture
    global mainDisplayList
    thing = guiEntrybox.get()
    for item in current_room.get_item():
        if item.get_name() == thing:
            if isinstance(item, Furniture):
                if item.get_isOpen() == True:
                    open_closed = "open"
                elif item.get_isOpen() == False:
                    open_closed = "closed"
                if item.get_locked() == True:
                    locked = "locked"
                elif item.get_locked() == False:
                    locked = "unlocked"
                mainDisplayList = [item.get_description()]
                mainDisplayList.append("The {} is {} and {}".format(item.get_name(), open_closed, locked))
                if open_closed == "open":
                    contents = item.get_contents()
                    furnitureItems = "\n[{} items]: ".format(item.get_name())
                    if len(contents)>0:
                        for fitem in contents:
                            furnitureItems += fitem.get_name() + ", "
                        furnitureItems = furnitureItems[:-2]
                    else:
                        furnitureItems += "the {} is empty".format(item.get_name())
                    mainDisplayList.append(furnitureItems)
                typewriter(mainDisplayList)
                return
            if isinstance(item, Item):
                mainDisplayList=["You'll need to hold that to examine it"]
                typewriter(mainDisplayList)
                return
    for item in holding:
        if item.get_name() == thing:
            mainDisplayList=["You examine the " + item.get_name()]
            mainDisplayList.append(item.get_description())
            typewriter(mainDisplayList)
            return
    mainDisplayList=["You can't examine " + thing]
    typewriter(mainDisplayList)

def inventory():
    # used to list the items you're holding
    global mainDisplayList
    mainDisplayList = ["You are holding:"]
    if len(holding)>0:
        for item in holding:
            mainDisplayList.append(item.get_name() + " ")
    else:
        mainDisplayList.append(" Nothing")
    typewriter(mainDisplayList)

def talk():
    global inhabitant
    inhabitant = current_room.get_character()
    inhabitantDetails=[]
    if inhabitant is None:
        inhabitantDetails.append("There's nobody to talk to...")
        typewriter(inhabitantDetails)
    else:
        typewriter(inhabitant.talk())


########################################################################################################################################################
#      set initial state of the game
########################################################################################################################################################

kitchen = Room("Kitchen")
ballroom = Room("Ballroom")
dining_hall = Room("Dining Hall")

kitchen.set_description("You can see this place is kept in good order")
ballroom.set_description("Time for a dance")
dining_hall.set_description("Let's eat!")

kitchen.link_room(dining_hall, "south")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")
ballroom.link_room(dining_hall, "east")

dave = Enemy("Zombie Dave", "Dave was once your friend, but he's now just a smelly zombie")
dave.set_conversation("...brrrraaaiinnssss")
dave.set_weakness("poisoned brains")
dave.set_killsPlayerText("braaiinnsss...nom...nom...nom")
dave.set_npcDeathText("You give the poisoned brains to Dave.\nHe begins to foam from his mouth, then bleed from his eyes.\nAfter some time Dave is just a smelly pile of ooze and bones on the floor...")
dining_hall.set_character(dave)

#create some items
cup = Item("cup", "a plain drinking vessel used by the servants", "use text")
sword = Weapon("sword", "an ornate infantry saber, but with a keen edge", "use text")
rat_poison = Item("rat poison", "white powder used to kill vermin", "use text")
bottle_of_wine = Item("bottle of red wine", "a fine vintage with a fruity nose", "use text")

chest = Furniture("chest", "an old wooden chest that looks like it once belonged to a pirate", "the lid creaks loudly")
chest.set_locked("locked")
chest.set_contents(sword)

small_key = Key("small key", "a small cast iron key, it looks pretty old", "The key turns easily...")
small_key.set_lockForKey(chest)

#put items in rooms
kitchen.set_item(cup)
kitchen.set_item(rat_poison)
kitchen.set_item(chest)
ballroom.set_item(small_key)

holding = []

current_room = kitchen


########################################################################################################################################################
#      instantiate the gui
########################################################################################################################################################

gui = Tk()
gui.geometry("800x800")
gui.title("RPG Game")
gui.configure(bg="#EBEBD3")
'''
guiRoomName=Label(gui, text=current_room.get_name(), font=("FreeSerif", 30), bd=3, relief=SUNKEN)
guiRoomName.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky=W+E)
guiRoomDesc=Label(gui,text=current_room.get_description(), font=("FreeSerif", 18))
guiRoomDesc.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
'''
guiNorth=Button(gui, text="N", padx=18, pady=20, command=lambda: move("north"), bg="#EBEBD3", font=("FreeSerif", 18))
guiNorth.grid(row=4, column=4, padx=5, pady=5)
guiSouth=Button(gui, text="S", padx=20, pady=20, command=lambda: move("south"), bg="#EBEBD3",  font=("FreeSerif", 18))
guiSouth.grid(row=6, column=4, padx=5, pady=5)
guiEast=Button(gui, text="E", padx=20, pady=20, command=lambda: move("east"), bg="#EBEBD3",  font=("FreeSerif", 18))
guiEast.grid(row=5, column=5, padx=5, pady=5)
guiWest=Button(gui, text="W", padx=17, pady=20, command=lambda: move("west"), bg="#EBEBD3",  font=("FreeSerif", 18))
guiWest.grid(row=5, column=3, padx=5, pady=5)

#-----------------DISPLAY--------------------
guiMainDisplay=Label(gui, font=("FreeSerif", 18), bd=3, relief=SUNKEN, bg="#EBEBD3")
guiMainDisplay.grid(row=10, column=0, columnspan=6, padx=5, pady=10, sticky=W+E)

guiEntrybox=Entry(gui,width=60)
guiEntrybox.grid(row=3, column=0, columnspan=6, padx=20, pady=20)

#-----------------LOOK--------------------
guiLook=Button(gui, text="Look", padx=14, pady=20, command=look, font=("FreeSerif", 18))
guiLook.grid(row=4 , column=1)

#-----------------Take--------------------
guiGet=Button(gui, text="Take", padx=18, pady=20, command=get, font=("FreeSerif", 18))
guiGet.grid(row=4, column=0)

#-----------------DROP--------------------
guiDrop=Button(gui, text="Drop", padx=12, pady=20, command=drop, font=("FreeSerif", 18))
guiDrop.grid(row=5, column=0)

#-----------------Talk--------------------
guiTalk=Button(gui, text="Talk", padx=19, pady=20, command=talk, font=("FreeSerif", 18))
guiTalk.grid(row=5, column=1)

#-----------------USE--------------------
guiUse=Button(gui, text="Use", padx=18, pady=20, command=lambda: use("item"), font=("FreeSerif", 18))
guiUse.grid(row=6, column=0)

#-----------------INVENTORY--------------------
guiUse=Button(gui, text="Inventory", padx=1, pady=20, command=inventory, font=("FreeSerif", 18))
guiUse.grid(row=6, column=1)

#-----------------EXAMINE--------------------
guiUse=Button(gui, text="Examine", padx=1, pady=20, command=examine, font=("FreeSerif", 18))
guiUse.grid(row=8, column=0)

typewriter(mainDisplayList)



gui.mainloop()


while True:
    print("\n")
    current_room.get_details()
    inhabitant = current_room.get_character()
    if inhabitant is not None:
        inhabitant.describe()
    command = input("> ")
    if command in travel:
        current_room = current_room.move(command)
    elif command == "talk":
        if inhabitant is None:
            print("There's nobody to talk to...")
        else:
            inhabitant.talk()
    elif command == "fight":
        if inhabitant is None:
            print("You slap yourself in the face... GET A GRIP!")
        else:
            combat_item = input("What will you use to fight " + str(inhabitant) + "?")
            if combat_item in backpack:
                if dave.fight(combat_item) == True:
                    print(str(inhabitant) + " lies dead at your feet")
                    current_room.set_character(None)









