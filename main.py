# Import PySimpleGUI
import PySimpleGUI as sg

# Import object modules
from game import Game
from player import Player
from deck import Deck
from card import *

# Initialize each instance of unique card object

card7 = Creature("Troll", 3, 3, 3, 'img\Troll_card.png', True)
card8 = Spell("Shock", 1, 'img\shock_card.png', 2)
card9 = Creature("Lion", 2, 2, 1, 'img\lion_card.png', False)
card10 = Creature("Bridge", 5, 1, 7, 'img\Bridge_card.png', False)
card11 = Spell("Divination", 3, 'img\divination_card.png', 3)
card12 = Creature("Wall", 1, 4, 2, 'img\wall_card.png', False)

# Initialize each instance of unique deck objcect
deck1 = Deck([card7, card8, card9, card10, card11, card12])

# Create the two players
p1_name = sg.popup_get_text('Enter name of Player 1')
p2_name = sg.popup_get_text('Enter name of Player 2')

playerAlpha = Player(p1_name, deck1)
playerBeta = Player(p2_name, deck1)

# Initialize the game
thisGame = Game(playerAlpha, playerBeta)

thisGame.newGame()


def show_image(cards):
    images = []
    for i in range(len(cards)):
        images.append(sg.Image(cards[i].getImage(), key=f'hand_{i}'))
    return images

def chooseCard(cards, title):
    layout = [[]]
    for i in range(len(cards)):
        layout[0].append(sg.Button(image_filename= cards[i].getImage(), key= i))
    window = sg.Window(title= title, layout= layout, size= (1600, 800))
    event = window.read(close= True)
    return event[0]

# Define the game board
layout = [
    [sg.Text(thisGame.players[0].getName(), key='P1', font=('Helvetica', 10)),
     sg.Text(f'{thisGame.players[0].getLifeTotal()}', key='P1_life', font=('Helvetica', 10)),
     sg.Text(f'Turn: {thisGame.getTurnNumber()}', key='turn', font=('Helvetica', 10)),
     sg.Text(thisGame.players[1].getName(), key='P2', font=('Helvetica', 10)),
     sg.Text(f'{thisGame.players[1].getLifeTotal()}', key='P2_life', font=('Helvetica', 10))],
    [sg.Text('Enemey Board', key='other_board', font=('Helvetica', 10)),
     sg.Button('Graveyard', key='other_graveyard', font=('Helvetica', 10))],
    [sg.Button('Action', key='act', font=('Helvetica', 10)),
     sg.Text('Player Board', key='this_board', font=('Helvetica', 10)),
     sg.Button('Graveyard', key='this_graveyard', font=('Helvetica', 10))],
    [sg.Text(f"{thisGame.getActivePlayer().getCardsInHand()}", key='hand', font=('Helvetica', 10))],
    # show_image(thisGame.getActivePlayer().getCardsInHand())
    [sg.Text(f'Active Player: {thisGame.activePlayer.getName()}', key='active', font=('Helvetica', 10)),
     sg.Text(f'Mana: {thisGame.activePlayer.getMana()}', key='mana', font=('Helvetica', 10)),
     sg.Button('Play card', key='play', font=('Helvetica', 10)),
     sg.Button('Pass Turn', key='pass', font=('Helvetica', 10)),
     sg.Button('New game', key='new_game', font=('Helvetica', 10))],
]

window = sg.Window('Card game', layout, size=(1600, 800))

while True:
    # Show GUI
    event, values = window.read()

    # Look for event
    match event:
        # 'Close' button have been pressed
        case sg.WINDOW_CLOSED:
            break

        # 'New game' button pressed
        case 'new_game':
            # Reset game
            thisGame.newGame()

        # 'Pass Turn' button pressed
        case 'pass':
            # Passing the turn to the next player
            thisGame.passTurn()

        # 'Play card' button pressed
        case 'play':
            # Ask player for card to play
            cardToPlay = chooseCard(thisGame.getActivePlayer().getCardsInHand(), 'Play card')
            if cardToPlay != None:
                # Display and double check
                decide = sg.popup_yes_no('Do you want to cast this card?', image= thisGame.getActivePlayer().getCardsInHand()[cardToPlay].getImage())
                if decide == "Yes":
                    thisGame.getActivePlayer().playCardFromHand(cardToPlay)

        # 'Graveyard' button pressed for active player
        case 'this_graveyard':
            grave = ""
            grave_size = len(thisGame.getActivePlayer().getPlayerGraveyard().getGraveyard())
            for i in range(grave_size):
                grave += f"{thisGame.getActivePlayer().getPlayerGraveyard().getGraveyard()[i]}\n---\n"
            sg.popup(grave)

        # 'Graveyard' button pressed for inactive player
        case 'other_graveyard':
            grave = ""
            grave_size = len(thisGame.getInactivePlayer().getPlayerGraveyard().getGraveyard())
            for i in range(grave_size):
                grave += f"{thisGame.getInactivePlayer().getPlayerGraveyard().getGraveyard()[i]}\n---\n"
            sg.popup(grave)

        # 'Action' button pressed
        case 'act':
            # Ask for the card to act
            attacker_event = chooseCard(thisGame.getActivePlayer().getBoard(), 'Attack with Creature')
            if attacker_event != None:
                attacker = thisGame.getActivePlayer().getBoard()[attacker_event]
                # Display card to avoid unwanted moves
                attacker.act()
                block_with_card = None
                if len(thisGame.getInactivePlayer().getBoard()) > 0:
                    block_with_card = chooseCard(thisGame.getInactivePlayer().getBoard(), 'Defend with Creature')
                    if block_with_card != None:  # and thisGame.getInactivePlayer().getBoard()[int(block_with_card)].isReadyToAct() == True
                        defender = thisGame.getInactivePlayer().getBoard()[block_with_card]
                        attacker.takeDamage(defender.getPower())
                        defender.takeDamage(attacker.getPower())
                        if attacker.getToughness() <= 0:
                            thisGame.getActivePlayer().getGraveyard().addToGraveyard(attacker)
                            thisGame.getActivePlayer().removeFromBoard(attacker_event)
                        if defender.getToughness() <= 0:
                            thisGame.getInactivePlayer().getGraveyard().addToGraveyard(defender)
                            thisGame.getInactivePlayer().removeFromBoard(block_with_card)
                    else:
                        thisGame.getInactivePlayer().changeLifeTotal(-(attacker.getPower()))
                        window['P1_life'].update(f"{thisGame.getPlayers()[0].getLifeTotal()}")
                        window['P2_life'].update(f"{thisGame.getPlayers()[1].getLifeTotal()}")

                        # Check for knock-out
                        if thisGame.getInactivePlayer().getLifeTotal() <= 0:
                            # Ask for new game
                            choise = sg.popup_yes_no(
                                f"{thisGame.getInactivePlayer().getName()}'s life total has hit {thisGame.getInactivePlayer().getLifeTotal()} and lost the game!\n"
                                f"New game?")
                            if choise == "Yes":
                                thisGame.newGame()
                            else:
                                break

    # Update display information
    window['hand'].update(f"{thisGame.activePlayer.getCardsInHand()}")
    window['other_board'].update(f"{thisGame.inactivePlayer.getBoard()}")
    window['this_board'].update(f"{thisGame.activePlayer.getBoard()}")
    window['mana'].update(f"Mana: {thisGame.activePlayer.getMana()}")
    window['turn'].update(f"Turn: {thisGame.getTurnNumber()}")
    window['active'].update(f"Active Player: {thisGame.activePlayer.getName()}")
    window['P1_life'].update(f"{thisGame.activePlayer.getLifeTotal()}")
    window['P2_life'].update(f"{thisGame.inactivePlayer.getLifeTotal()}")