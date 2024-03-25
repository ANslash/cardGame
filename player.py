from graveyard import Graveyard
class Player:
    def __init__(self, name, deck):
        self.name: str = name
        self.deck = deck
        self.graveyard: Graveyard = Graveyard()
        self.hand: list = []
        self.board: list = []
        self.startLife: int = 100
        self.lifeTotal: int = self.startLife
        self.mana: int = 0
        self.maxMana: int = 0
        self.playingGame = None

    def __str__(self):
        return f"{self.name}: {self.deck}"

    def getName(self):
        print(f"Player name: {self.name}")
        return self.name

    def getGraveyard(self):
        return self.graveyard

    def getMana(self):
        print(self.mana)
        return self.mana

    def useMana(self, cost):
        self.mana -= cost

    def setMana(self, amount):
        print(f"Setting mana to: {amount}")
        self.mana = amount

    def getMaxMana(self):
        print(self.maxMana)
        return self.maxMana

    def setMaxMana(self, amount):
        print(f"Setting max mana to: {amount}")
        self.maxMana = amount

    def increaseMaxMana(self):
        print("Increasing max mana!")
        self.maxMana += 1

    def getPlayerDeck(self):
        print(self.deck)
        return self.deck

    def getPlayerGraveyard(self):
        return self.graveyard

    def getCardsInHand(self):
        print(self.hand)
        return self.hand

    def drawCards(self, amount):
        for i in range(amount):
            if len(self.deck.deck) > 0:
                card = self.deck.removeFromDeck(0)
                print(f"--Card drawn--\n{card}")
                self.hand.append(card)

    def getBoard(self):
        print(self.board)
        return self.board

    def removeFromBoard(self, index):
        self.board.pop(index)

    def playCardFromHand(self, index):
        if self.getMana() >= self.hand[index].getCost() and len(self.board) < 4:
            self.useMana(self.hand[index].getCost())
            print(f"--Casting--\n{self.hand[index]}")
            if self.hand[index].getCardType() == "Permanent":
                self.hand[index].setController(self)
                self.board.append(self.hand[index])
                self.hand.pop(index)
                if hasattr(self.board[-1], 'enterTrig'):
                    self.board[-1].triggerETB(self.getGame())
                print("Goes to the board!")
            else:
                """self.drawCards(self.hand[index].getSpellPower())"""
                self.hand[index].castingSpell(self.getGame())
                self.graveyard.addToGraveyard(self.hand[index])
                self.hand.pop(index)
                print("Goes to the graveyard!")

        else:
            print("Not enough mana to play this spell...")

    def changeLifeTotal(self, amount):
        self.lifeTotal += amount
        print(f"Lifetotal is now: {self.lifeTotal}")


    def setLifeTo(self, amount):
        print(f"Setting life to: {amount}")
        self.lifeTotal = amount

    def getStartingLife(self):
        print(f"Starting life: {self.startLife}")
        return self.startLife

    def getLifeTotal(self):
        print(self.lifeTotal)
        return self.lifeTotal

    def discard(self, index):
        print("Card discarded")
        self.graveyard.addToGraveyard(self.hand[index])
        self.hand.pop(index)

    def getGame(self):
        return self.playingGame

    def setGame(self, game):
        self.playingGame = game