class Character():

    # Create a character
    def __init__(self, char_name, char_description):
        self.name = char_name
        self.description = char_description
        self.conversation = None

    # Describe this character
    def describe(self):
        print( self.name + " is here!" )
        print( self.description )
        return self.description #--------------------------------------used to update the gui

    def get_name(self):
        return self.name

    # Set what this character will say when talked to
    def set_conversation(self, conversation):
        self.conversation = conversation

    def get_conversation(self):
        return self.conversation

    # Talk to this character
    def talk(self):
        characterConversation=[] #--------------------------------------
        if self.conversation is not None:
            print("[" + self.name + " says]: " + self.conversation)
            characterConversation.append("[" + self.name + " says]: " + self.conversation) #--------------------------------------
        else:
            print(self.name + " doesn't want to talk to you")
            characterConversation.append(self.name + " doesn't want to talk to you") #--------------------------------------
        return characterConversation #--------------------------------------

    # Fight with this character
    def fight(self, combat_item):
        print(self.name + " doesn't want to fight with you")
        return True

class Enemy(Character):
    def __init__(self, char_name, char_description):
        super().__init__(char_name, char_description)
        self.weakness = None
        self.killsPlayerText = ""
        self.npcDeathText = ""

    def set_weakness(self, weakness):
        self.weakness = weakness

    def get_weakness(self):
        return self.weakness

    def set_killsPlayerText(self, killsPlayerText):
        self.killsPlayerText = killsPlayerText

    def get_killsPlayerText(self):
        return self.killsPlayerText

    def set_npcDeathText(self, npcDeathText):
        self.npcDeathText = npcDeathText

    def get_npcDeathText(self):
        return self.npcDeathText

    def fight(self, combat_item):
        if combat_item == self.weakness:
            #print("you smack " + self.name + " with the " + combat_item + " and he dies")
            return True
        else:
            #print(self.name + " kills you without mercy")
            return False
















