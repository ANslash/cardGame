class Card:
    def __init__(self, cardType, cost, name):
        self.cardType: str = cardType
        self.cost: int = cost
        self.name: str = name

    def getCardType(self):
        print(self.cardType)
        return self.cardType

    def getCost(self):
        print(self.cost)
        return self.cost

    def getName(self):
        print(self.name)
        return self.name

class Permanent(Card):

    def __init__(self, name, cost, image, subTypes, isTapped):
        super().__init__(cardType= "Permanent", cost= cost, name= name)
        self.subTypes = subTypes
        self.isTapped = isTapped
        self.image = image

    def __str__(self):
        return (f"Type: {self.cardType}\n"
                f"Cost: {self.cost}\n"
                f"Text: {self.name}\n")

    def getSubTypes(self):
        return self.subTypes

    def getIsTapped(self):
        return self.isTapped

    def tap(self):
        self.isTapped = True

    def untap(self):
        self.isTapped = False

    def getImage(self):
        if self.isTapped:
            return self.image[0]
        else:
            return self.image[1]

class Creature(Permanent):
    def __init__(self, name, cost, power, toughness, image, readyToAct):
        super().__init__(name= name, cost= cost, image= image, subTypes= ["Creature"], isTapped= False)
        self.power = power
        self.toughness = toughness
        self.readyToAct = readyToAct

    def getToughness(self):
        return self.toughness

    def takeDamage(self, amount):
        self.toughness -= amount

    def setStats(self, newPower, newToughness):
        self.power = newPower
        self.toughness = newToughness

    def isReadyToAct(self):
        print(self.readyToAct)
        return self.readyToAct

    def makeReadyToAct(self):
        print("Made ready to act")
        self.readyToAct = True

    def act(self):
        print("It acts")
        self.readyToAct = False

    def getPower(self):
        print(f"Card power: {self.power}")
        return self.power

class Spell(Card):

    def __init__(self, name, cost, image, spellPower):
        super().__init__(cardType= "Spell", cost= cost, name= name)
        self.spellPower = spellPower
        self.image = image

    def __str__(self):
        return (f"Type: {self.cardType}\n"
                f"Cost: {self.cost}\n"
                f"Text: {self.name}\n"
                f"SpellPower: {self.spellPower}")

    def getSpellPower(self):
        return self.spellPower

    def getImage(self):
        return self.image

class Troll_card(Creature):
    def __init__(self):
        super().__init__(name= "Troll", cost= 3, power= 3, toughness= 3, readyToAct= True, image= ['img\Troll_card_tapped.png', 'img\Troll_card.png'])

class Bridge_card(Creature):
    def __init__(self):
        super().__init__(name= "Brigde", cost= 1, power= 1, toughness=7, readyToAct= True, image= ['img\Bridge_card_tapped.png','img\Bridge_card.png'])
        #self.defender = True    # Permanents with defender can't attack.
        self.frenzied = False   # Has a trigger when it survives damage for the first time.

    """
    When this card takes damage for the first time without dying, a trigger happens:
    It switches its power and toughness, and can attack as though it didn't have defender.
    """
    def frenzyTrigger(self):
        self.frenzied = True
        super().setStats(newPower= self.toughness, newToughness= self.power)
        self.defender = False

    def isFrenzied(self):
        return self.frenzied

    """def isDefender(self):
        return self.defender"""

class Lion_card(Creature):
    def __init__(self):
        super().__init__(name= "Lion", cost=2, power= 2, toughness= 1, readyToAct= False, image= ['img\lion_card_tapped.png', 'img\lion_card.png'])
        self.deathRattle = True # Has a trigger, when it is destroyed from the battlefield.

    """
    Triggers when this card is put into the graveyard from the battlefield:
    Creates a 1/1 Kitten creature token.
    """
    def triggerDeathRattle(self, player):
        kittyToken = Creature(name= "Kitten", cost= 0, power= 1, toughness= 1, readyToAct= False, image= ['img\kitten_token_tapped.png', 'img\kitten_token.png'])
        player.getBoard().append(kittyToken)


