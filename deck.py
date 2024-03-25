from random import randrange

class Deck:
    def __init__(self, deckList):
        self.deckList: list = deckList
        self.deck: list = deckList

    def __str__(self):
        return f"{self.deckList}"

    def getDeckList(self):
        return self.deckList

    def getDeck(self):
        return self.deck

    def shuffle(self, cards):

        print("Shuffle")

        self.deck = []
        buffer = list(cards)

        while len(buffer) > 0:
            index = randrange(0, len(buffer))
            card = buffer[index]
            buffer.pop(index)
            self.deck.append(card)

    def putInDeck(self, index, card):
        print("Placed card in deck")

        self.deck.insert(index, card)

    def removeFromDeck(self, index):
            print(f"Removed card number: {index + 1}")

            card = self.deck[index]

            self.deck.pop(index)

            return card