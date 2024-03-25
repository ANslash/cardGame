class Game:
    def __init__(self, playerAlpha, playerBeta):
        self.players: list = [playerAlpha, playerBeta]
        self.turnNumber: int = 0
        self.activePlayer = self.players[0]
        self.inactivePlayer = self.players[1]

    def getPlayers(self):
        print(self.players)
        return self.players

    def getTurnNumber(self):
        print(self.turnNumber)
        return self.turnNumber

    def getActivePlayer(self):
        print(self.activePlayer)
        return self.activePlayer

    def getInactivePlayer(self):
        print(self.inactivePlayer)
        return self.inactivePlayer

    def setActivePlayer(self, player):
        print("New Active Player")
        self.activePlayer = player

    def setInactivePlayer(self, player):
        print("New Active Player")
        self.inactivePlayer = player

    def passTurn(self):
        print("Passing the turn to: ")
        # Checking if player ineeds to discard to handsize
        while len(self.activePlayer.getCardsInHand()) > 3:
            print(self.activePlayer.getCardsInHand())
            choise = int(input("Please discard a card (index): "))
            self.getActivePlayer().discard(choise)

        # Increase turn number
        self.turnNumber += 1

        # Set new active/inactive player
        self.setActivePlayer(self.players[self.turnNumber%len(self.players)])
        self.setInactivePlayer(self.players[(self.turnNumber + 1)% len(self.players)])

        # Run starting phase
        self.activePlayer.increaseMaxMana()
        self.activePlayer.setMana(self.activePlayer.getMaxMana())
        self.activePlayer.drawCards(1)

        # Prepare all creatures on the active player's board to act/attack
        board_size = len(self.activePlayer.getBoard())
        if board_size > 0:
            for i in range(board_size):
                self.getActivePlayer().getBoard()[i].makeReadyToAct()
                self.getActivePlayer().getBoard()[i].untap()

    # Return game to first state
    def newGame(self):
        print("Starting a new game!!")

        self.turnNumber = 0

        self.setActivePlayer(self.players[self.turnNumber % len(self.players)])
        self.setInactivePlayer(self.players[(self.turnNumber + 1) % len(self.players)])

        for player in self.players:
            # shuffle hand, deck and graveyard together
            board_size = len(player.getBoard())
            hand_size = len(player.getCardsInHand())
            if board_size > 0:
                for i in range(board_size):
                    player.board.pop(0)
            if hand_size > 0:
                for i in range (hand_size):
                    player.hand.pop(0)
            player.deck.shuffle(player.deck.deckList)

            # Set life to starting life total
            player.setLifeTo(player.getStartingLife())

            # Set mana and maxMana to starting total
            player.setMaxMana(1)
            player.setMana(player.getMaxMana())

            # Draw two cards at the beginning of play
            player.drawCards(2)