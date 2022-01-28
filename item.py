#item class
'''
Attributes for the name and the description of the item
A constructor method
Getters and setters for the name and the description of the item
Any additional attributes and methods you would like to add
'''
class Item():
    def __init__(self, name, description, use_text):
        self.name = name
        self.description = description
        self.use_text = use_text

    def set_name(self, item_name):
        self.name = item_name

    def get_name(self):
        return self.name

    def set_description(self, item_description):
        self.description = item_description

    def get_description(self):
        return self.description

    def get_useText(self):
        return self.use_text

class Weapon(Item): # items used to destroy enemies
    def __init__(self, name, description, use_text):
        super().__init__(name, description, use_text)
        self.target = None

    def set_target(self, target):
        self.target = target

    def get_target(self):
        return self.target

class Furniture(Item): # items which contain other items, and may need to be unlocked
    def __init__(self, name, description, use_text):
        super().__init__(name, description, use_text)
        self.isOpen = False
        self.locked = None
        self.contents = []

    def set_isOpen(self, command):
        if command == "open":
            self.isOpen = True
        if command == "close":
            self.isOpen = False

    def get_isOpen(self):
        return self.isOpen

    def set_locked(self, state):
        if state == "locked":
            self.locked = True
        if state == "unlocked":
            self.locked = False

    def get_locked(self):
        return self.locked

    def set_contents(self, item):
        if item in self.contents:
            self.contents.remove(item)
        else:
            self.contents.append(item)

    def get_contents(self):
        return self.contents

class Key(Item):
    def __init__(self, name, description, use_text):
        super().__init__(name, description, use_text)
        self.lockForKey = None

    def set_lockForKey(self, lockForKey):
        self.lockForKey = lockForKey

    def get_lockForKey(self):
        return self.lockForKey








