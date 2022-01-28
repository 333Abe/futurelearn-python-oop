class Room():
    def __init__(self, room_name):
        self.name = room_name
        self.description = None
        self.linked_rooms = {}
        self.character = None
        self.items = []

    def set_description(self, room_description):
        self.description = room_description

    def get_description(self):
        return self.description

    def set_character(self, character):
        self.character = character

    def get_character(self):
        return self.character

    def set_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print("item removed")
        else:
            self.items.append(item)
            print("item added")

    def get_item(self):
        return self.items

    def describe(self):
        print(self.description)

    def set_name(self, room_name):
        self.name = room_name

    def get_name(self):
        return self.name

    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link
        #print( self.name + " linked rooms :" + repr(self.linked_rooms) )

    def get_details(self):
        #print("You are in the " + self.get_name())
        roomDetails = "You are in the " + self.get_name() + "\n" #-------------------------------------------------------------------------
        #print(self.description)
        roomDetails = roomDetails + self.description + "\n" + "[Exits]: "#-------------------------------------------------------------------------------------
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            #print("The " + room.get_name() + " is to the " + direction)
            roomDetails = roomDetails + direction + ", " #--------------------------------------
        roomDetails = roomDetails[:-2]
        return roomDetails #---------------------------------------------------------------------------------------------------------------

    def move(self, direction):
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self