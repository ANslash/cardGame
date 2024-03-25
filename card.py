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
        self.controller = None

    def __str__(self):
        return (f"Type: {self.subTypes}\n"
                f"Cost: {self.cost}\n"
                f"Text: {self.name}\n"
                f"Controller: {self.controller}")

    def getController(self):
        return self.controller

    def setController(self, controller):
        self.controller = controller

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

    def __init__(self, name, cost, image):
        super().__init__(cardType= "Spell", cost= cost, name= name)
        self.image = image

    def __str__(self):
        return (f"Type: {self.name}\n"
                f"Cost: {self.cost}\n"
                f"Text: {self.cardType}")

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
        #self.defender = False

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
    def triggerDeathRattle(self, game):
        kittyToken = Creature(name= "Kitten", cost= 0, power= 1, toughness= 1, readyToAct= False, image= ['img\kitten_token_tapped.png', 'img\kitten_token.png'])
        for player in game.getPlayers():
            if player == self.controller:
                player.getBoard().append(kittyToken)


class Shock_card(Spell):
    def __init__(self):
        super().__init__(name= "Shock", cost= 1, image= 'img\shock_card.png')
        self.spellDamage = 2

    """
    Cast this spell:
    Deals 2 (base)damage to any target
    """
    def castingSpell(self, game):
        legal_targets = []
        for player in game.getPlayers():
            legal_targets.append(player)
            legal_targets += player.getBoard()
        target = legal_targets[game.chooseCard(legal_targets, f'Deal {self.spellDamage} to any target')]
        if hasattr(target, 'toughness'):            # Check if tartet is a Creature
            target.takeDamage(self.spellDamage)
            if target.getToughness() <= 0:          # Check if target is destroyed
                dead_creature = target
                target.setController(None)
                for combatant in range(len(target.getController().getBoard())):
                    if target.getController().getBoard()[combatant] == target:
                        dead_creature.getController().getGraveyard().addToGraveyard(target)
                        dead_creature.getController().getBoard().pop(combatant)
                if hasattr(target, 'deathRattle'):  # Check if target has triggered ability on death
                    dead_creature.triggerDeathRattle(game)
            elif hasattr(target, 'frenzied') and not target.isFrenzied():   # Check if target has a taking damage
                target.frenzyTrigger()

        elif hasattr(target, 'lifeTotal'):          # Check if target is a player
            game.damagePlayer(self.spellDamage, target)

class Divination_card(Spell):
    def __init__(self):
        super().__init__(name= "Divination", cost= 1, image= 'img\divination_card.png')

    """
    Draws the caster 2 cards when played
    """
    def castingSpell(self, game):
        game.getActivePlayer().drawCards(2)





