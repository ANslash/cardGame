# Import PySimpleGUI
import PySimpleGUI as sg

# Import object modules
import game
from player import Player
from deck import Deck
from card import *

# Initialize each instance of unique card object

card1 = Troll_card() #Creature("Troll", 3, 3, 3, 'img\Troll_card.png', True)
card2 = Shock_card() #Spell("Shock", 1, 'img\shock_card.png')
card3 = Lion_card() #Creature("Lion", 1, 2, 1, 'img\lion_card.png', False)
card4 = Bridge_card()  # Creature(name= "Bridge", cost= 1, power= 1, toughness= 7, image= ['img\Bridge_card_tapped.png', 'img\Bridge_card.png'], readeyToAct= False)
card5 = Divination_card() #Spell("Divination", 3, 'img\divination_card.png')
card6 = Wall_card() #Creature("Wall", 1, 4, 2, ['img\wall_card.png', 'img\wall_card_tapped.png'], True)

card7 = Lion_card()
card8 = Lion_card()
card9 = Lion_card()
card10 = Divination_card()
card11 = Divination_card()
card12 = Wall_card()
card13 = Wall_card()
card14 = Wall_card()

# Initialize each instance of unique deck objcect
deck1 = Deck([card1, card2, card3, card4, card5, card6])
deck2 = Deck([card7, card8, card9, card10, card11, card12, card13, card14])

# Create the two players
p1_name = ""
p2_name = ""
while p1_name == p2_name:
    p1_name = sg.popup_get_text('Enter name of Player 1')
    p2_name = sg.popup_get_text('Enter name of Player 2')
    if p1_name == p2_name:
        sg.popup("Both player names are the same.\n"
                 "Please choose unique names.")

playerAlpha = Player(p1_name, deck1)
playerBeta = Player(p2_name, deck2)

# Initialize the game
thisGame = game.Game(playerAlpha, playerBeta)

for player in thisGame.getPlayers():
    player.setGame(thisGame)

thisGame.newGame()


def show_image(cards):
    images = []
    for i in range(len(cards)):
        images.append(sg.Image(cards[i].getImage(), key=f'hand_{i}'))
    return images


""" --- WIP --- """
def pickTarget():
    layout = [[],   # Enemy player
              [],   # Enemy board
              [],   # Own board
              []]   # Player themselves

    layout[0].append(sg.Button(button_text= thisGame.getInactivePlayer().getName(), key= 'other'))
    for i in range(len(thisGame.getInactivePlayer().getBoard())):
        layout[1].append(sg.Button(image_filename= thisGame.getInactivePlayer().getBoard()[i].getImage(), key= f'other_{i}'))
    for i in range(len(thisGame.getActivePlayer().getBoard())):
        layout[2].append(sg.Button(image_filename= thisGame.getActivePlayer().getBoard()[i].getImage(), key= f'this_{i}'))
    layout[3].append(sg.Button(button_text= thisGame.getActivePlayer().getName(), key= 'this'))

def makePlayerBoard(key):
    board_line = []
    for i in range(4):
        board_line.append(sg.Image(filename= 'img\Blank_card.png', key= f'{key}_{i}'))
    board_line.append(sg.Button(button_text= 'Graveyard', key= f'{key}_graveyard', font=('Helvetica', 10)))

    return board_line

# Define the game board
layout = [
    [sg.Text(thisGame.players[0].getName(), key='P1', font=('Helvetica', 10)),
     sg.Text(f'{thisGame.players[0].getLifeTotal()}', key='P1_life', font=('Helvetica', 10)),
     sg.Text(f'Turn: {thisGame.getTurnNumber()}', key='turn', font=('Helvetica', 10)),
     sg.Text(thisGame.players[1].getName(), key='P2', font=('Helvetica', 10)),
     sg.Text(f'{thisGame.players[1].getLifeTotal()}', key='P2_life', font=('Helvetica', 10))], # End of game info display line
    makePlayerBoard("other"),                                                                       # End of inactive player board display line
    [sg.Button('Action', key='act', font=('Helvetica', 10))] + makePlayerBoard('this'),     # End of active player board display line
    [sg.Text(f"{thisGame.getActivePlayer().getCardsInHand()}", key='hand', font=('Helvetica', 10))],    # End of active player hand display line
    [sg.Text(f'Active Player: {thisGame.activePlayer.getName()}', key='active', font=('Helvetica', 10)),
     sg.Text(f'Mana: {thisGame.activePlayer.getMana()}', key='mana', font=('Helvetica', 10)),
     sg.Button('Play card', key='play', font=('Helvetica', 10)),
     sg.Button('Pass Turn', key='pass', font=('Helvetica', 10)),
     sg.Button('New game', key='new_game', font=('Helvetica', 10))],                                # End of active player info display line
]

window = sg.Window('Card game', layout, size=(1000, 600))

def updatePlayerBoard(player):
    activePlayer = (player == thisGame.getActivePlayer())
    for i in range(4):
        if activePlayer:
            if len(player.getBoard()) > i:
                window[f"this_{i}"].update(player.getBoard()[i].getImage())
            else:
                window[f"this_{i}"].update('img\Blank_card.png')
        else:
            if len(player.getBoard()) > i:
                window[f"other_{i}"].update(player.getBoard()[i].getImage())
            else:
                window[f"other_{i}"].update('img\Blank_card.png')



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
            cardToPlay = thisGame.chooseCard(thisGame.getActivePlayer().getCardsInHand(), 'Play card') # Call function from game.py module
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
            # Display cards on board and choose attacker
            attacker_event = thisGame.chooseCard(thisGame.getActivePlayer().getBoard(), 'Attack with Creature')                         # Display possible attackers on GUI and use button choise (chooseCard funtion from game.py module)
            if attacker_event != None:
                attacker = thisGame.getActivePlayer().getBoard()[attacker_event]
                if attacker.isReadyToAct() and attacker.getIsUntapped():                                                          # Check if tapped or summoning sick
                    attacker.tap()                                                                                                  # Tap cards as part of action
                    block_with_card = None                                                                                          # init block index
                    if len(thisGame.getInactivePlayer().getBoard()) > 0:                                                            # Check if there is any possible blockers
                        block_with_card = thisGame.chooseCard(thisGame.getInactivePlayer().getBoard(), 'Defend with Creature')          # Display blockers on GUI and use button choise (chooseCard funtion from game.py module)
                        if block_with_card != None and thisGame.getInactivePlayer().getBoard()[block_with_card].getIsUntapped():  # Check if valid defender (untapped)
                            defender = thisGame.getInactivePlayer().getBoard()[block_with_card]

                            # Creatures deals damage to each other
                            atk_dmg = attacker.getPower()
                            def_dmg = defender.getPower()
                            attacker.takeDamage(def_dmg)
                            defender.takeDamage(atk_dmg)

                            # Check for combat related triggers
                            if attacker.getToughness() <= 0:                                                                        # Is attacker destroyed?
                                thisGame.getActivePlayer().getGraveyard().addToGraveyard(attacker)
                                if hasattr(attacker, "deathRattle"):                                                                # Does attacker have a triggered ability on death?
                                    attacker.triggerDeathRattle(thisGame.getActivePlayer())
                                thisGame.getActivePlayer().removeFromBoard(attacker_event)
                            elif hasattr(attacker, "frenzied") and not attacker.isFrenzied() and def_dmg > 0:                       # Is attacker now frenzied?
                                attacker.frenzyTrigger()
                            if defender.getToughness() <= 0:                                                                        # Is defender destroyed?
                                thisGame.getInactivePlayer().getGraveyard().addToGraveyard(defender)
                                if hasattr(defender, "deathRattle"):                                                                # Does defender have a triggeder ability on death?
                                    defender.triggerDeathRattle(thisGame.getInactivePlayer())
                                thisGame.getInactivePlayer().removeFromBoard(block_with_card)
                            elif hasattr(defender, "frenzied") and not defender.isFrenzied() and atk_dmg > 0:                       # Is defender now frenzied?
                                defender.frenzyTrigger()
                        else:
                            # Deal damage to player
                            thisGame.damagePlayer(attacker.getPower(), thisGame.getInactivePlayer())
                    else:
                        # Deal damage to player
                        thisGame.damagePlayer(attacker.getPower(), thisGame.getInactivePlayer())

    # Update display information
    window['hand'].update(f"{thisGame.activePlayer.getCardsInHand()}")
    updatePlayerBoard(thisGame.getInactivePlayer())
    updatePlayerBoard(thisGame.getActivePlayer())
    window['mana'].update(f"Mana: {thisGame.activePlayer.getMana()}")
    window['turn'].update(f"Turn: {thisGame.getTurnNumber()}")
    window['active'].update(f"Active Player: {thisGame.activePlayer.getName()}")
    window['P1_life'].update(f"{thisGame.activePlayer.getLifeTotal()}")
    window['P2_life'].update(f"{thisGame.inactivePlayer.getLifeTotal()}")