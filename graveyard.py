class Graveyard:
    def __init__(self):
        self.conains: list = []

    def getGraveyard(self):
        print(self.conains)
        return self.conains

    def removeFromGraveyard(self, index):
        print(f"Removed the card: {self.conains[index]}")
        self.conains.pop(index)

    def addToGraveyard(self, card):
        print(f"Added {card} to the graveyard")
        self.conains.append(card)