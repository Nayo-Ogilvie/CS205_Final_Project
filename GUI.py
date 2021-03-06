import pygame
from Button import Button
from board import Board
from AI import opponent
import time

# global variables
game = Board(1)
defaultX = 1200
defaultY = 700
defaultScreenSize = [defaultX, defaultY]
fullScreenSize = [0, 0]  # set on openning of program
screenSize = defaultScreenSize
whatSize = 0  # 0 is default, 1 is fullscreen
alreadyFullScreen = False
ai = opponent(True)
tiles = []
otherButtons = []
bgOptions = []
endButtons = []
running = True
run = True
start = True
flagEnd = False
gameArray = []
green = (34, 139, 34)
blue = (34, 34, 139)
red = (139, 34, 34)
purple = (128, 0, 128)
background = green
widthLine = 0
flag = False
row = 0
column = 0
difficulty = True
players = 1
turnOrder = 1
player1 = 1  # Assumes human is player 1 to start
player2 = 2  # Assumes AI is player 2 to start


#############################################################
# function to get the difficulty chosen. Returns 0 for easy #
# and 1 for difficult                                       #
#############################################################
def getDifficulty():
    return difficulty


#############################################################
# function to get number of players. Returns 1 and 2        #
#############################################################
def getNumberOfPlayers():
    return players


#############################################################
# function to get the turn order when playing against AI.   #
# Returns 1 for user playing first and 2 for user playing   #
# second                                                    #
#############################################################
def getTurnOrder():
    return turnOrder


#############################################################
# function to get the array from the backend                #
#############################################################
def updateGameArray():
    global gameArray
    gameArray = game.get_current_layout()
    # print(" Getting the array from the backend ")


#############################################################
# function to send the array to the backend                 #
#############################################################
def getGameArray():
    # print(" sending the gameArray ")
    return gameArray


#############################################################
# function to draw the 8x8 board and the pieces             #
#############################################################
def drawBoard(screen):
    global tiles
    updateGameArray()
    tiles = []
    # To draw the grid squares
    x = 20
    y = 50
    square = 80
    for i in range(0, 8):
        for j in range(0, 8):
            if gameArray[i][j] == 3:
                color = background
                if flag:
                    color = (0, 0, 0)

                tiles.append(Button(screen, color, x, y, square, square, widthLine=widthLine))
            else:
                tiles.append(Button(screen, background, x, y, square, square))
            x = x + square + 1
        x = 20
        y = y + square + 1

    # drawing the playing pieces
    radius = 30
    xCir = 60
    yCir = 90
    for i in range(len(gameArray)):
        for j in range(len(gameArray[i])):
            if gameArray[i][j] == 1:
                pygame.draw.circle(screen, (255, 255, 255), (xCir, yCir), radius)
            if gameArray[i][j] == 2:
                pygame.draw.circle(screen, (0, 0, 0), (xCir, yCir), radius)

            xCir = xCir + square + 1
        xCir = 60
        yCir = yCir + square + 1


#############################################################
# buttons for changing the background color there are 4     #
# choices for the background color: red, blue purple, green #
#############################################################
def changeBackground(screen):
    global bgOptions
    bgOptions = []
    Button(screen, (255, 255, 255), 870, 400, 100, 50, "Background color")
    bgOptions.append(Button(screen, red, 840, 470, 30, 30))
    bgOptions.append(Button(screen, blue, 880, 470, 30, 30))
    bgOptions.append(Button(screen, purple, 920, 470, 30, 30))
    bgOptions.append(Button(screen, green, 960, 470, 30, 30))


#############################################################
# Display the end game screen questions whether the user    #
# would like to play again and indicates winner of the game #
#############################################################
def displayEndButtons(screen):
    global endButtons
    endButtons = []
    endButtons.append(Button(screen, (255, 255, 255), 600, 300, 100, 100, "Play again?"))
    endButtons.append(Button(screen, (210, 210, 210), 800, 500, 100, 100, "Yes"))
    endButtons.append(Button(screen, (210, 210, 210), 400, 500, 100, 100, "No"))

    if game.determineWinner() == 1:
        endButtons.append(Button(screen, (255, 255, 255), 500, 100, 100, 100, "Player 1 Wins!"))
    elif game.determineWinner() == 2:
        endButtons.append(Button(screen, (255, 255, 255), 600, 100, 100, 100, "Player 2 Wins"))
    elif game.determineWinner() == 3:
        endButtons.append(Button(screen, (255, 255, 255), 600, 100, 100, 100, "It's a tie!"))


#############################################################
# Display the buttons located to the right of the game board#
# during actual game play                                   #
#############################################################
def displayOtherButtons(screen):
    global otherButtons
    otherButtons = []
    otherButtons.append(Button(screen, (210, 210, 210), 950, 100, 130, 80, "Show moves"))
    otherButtons.append(Button(screen, (210, 210, 210), 950, 200, 130, 80, "Help"))
    otherButtons.append(Button(screen, (210, 210, 210), 750, 100, 150, 80, "Fullscreen"))
    otherButtons.append(Button(screen, (210, 210, 210), 750, 200, 150, 80, "Default Screen"))
    if (game.get_current_turn() == 1):
        otherButtons.append(Button(screen, (255, 255, 255), 850, 1, 100, 100, "Player 1's Turn"))
    else:
        otherButtons.append(Button(screen, (255, 255, 255), 850, 1, 100, 100, "Player 2's Turn"))
    player1Tiles = "Player 1 tiles = " + str(game.numberOfTiles(1))
    player2Tiles = "Player 2 tiles = " + str(game.numberOfTiles(2))
    otherButtons.append(Button(screen, (255, 255, 255), 870, 550, 100, 50, player1Tiles))
    otherButtons.append(Button(screen, (255, 255, 255), 870, 600, 100, 100, player2Tiles))
    otherButtons.append(Button(screen, (210, 210, 210), 870, 300, 120, 80, "undo"))


#############################################################
# Returns the players moves                                 #
#############################################################
def getNextMove():
    return row, column


#############################################################
# Function listens for button press for the game board      #
# all of the buttons to the right of the game board,        #
# including fullscreen, show moves, default screen, help,   #
# undo, and the background color buttons                    #
# The listenor also listens for the end game page buttons   #
# yes and no indiciating whether the user would like to     #
# play again                                                #
#############################################################
def eventListener(position):
    global running, flagEnd, gameArray, background, widthLine, flag, row, column, run, screenSize, whatSize, alreadyFullScreen, start
    for event in pygame.event.get():
        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # Did the user click?
        if event.type == pygame.MOUSEBUTTONDOWN:
            for t in range(len(tiles)):
                if tiles[t].isOver(position):
                    row = t // 8
                    column = t % 8
                    # updateGameArray()
            for c in range(len(bgOptions)):
                if bgOptions[c].isOver(position):
                    background = bgOptions[c].color

            if otherButtons[0].isOver(position):
                if flag:
                    widthLine = 0
                    flag = False
                else:
                    widthLine = 3
                    flag = True
            if otherButtons[1].isOver(position):
                helpScreen()
            if otherButtons[2].isOver(position):
                screenSize = fullScreenSize
                whatSize = 1
            if otherButtons[3].isOver(position):
                screenSize = defaultScreenSize
                whatSize = 0
                alreadyFullScreen = False
            if otherButtons[7].isOver(position):
                game.undo()
                row = 0
                column = 0
                updateGameArray()

            try:
                if endButtons[1].isOver(position):
                    game.reset()
                    start = True
                    flagEnd = False
                if endButtons[2].isOver(position):
                    running = False
                    run = False
            except:
                pass


#############################################################
# Function where all setup game functions occur including   #
# drawing the board, displaying other buttons, changing     #
# the background colors also is container for performing    #
# moves for the AI and player                               #
#############################################################
def mainGameLoop():
    global screenSize, fullScreenSize, whatSize, alreadyFullScreen, running, flagEnd, player1, player2, endButtons
    pygame.init()

    infoObject = pygame.display.Info()
    fullScreenSize = [infoObject.current_w, infoObject.current_h]
    # Set up the drawing window
    if whatSize == 0:
        screen = pygame.display.set_mode(screenSize)
    else:
        screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    # Run until the user asks to quit

    while running:
        if whatSize == 0:
            screen = pygame.display.set_mode(screenSize)
        else:
            if alreadyFullScreen == False:
                alreadyFullScreen = True
                screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)

        # Fill the background with white
        screen.fill((255, 255, 255))

        if start:
            startScreen(screen)
            endButtons = []
        else:
            if not flagEnd:
                # Draw the screen elements
                drawBoard(screen)
                displayOtherButtons(screen)
                changeBackground(screen)
                pygame.display.update()

                # get the mouse position and check whether there was a click
                position = pygame.mouse.get_pos()
                eventListener(position)

                # Game operations
                game.generate_legal_moves()

                # Player 1's turn and legal moves exist
                if (game.get_current_turn() == 1 and game.isPossibleMove()):
                    if (player1 == 1):
                        do_human_move(1)
                    elif (player1 == 2):
                        do_ai_move(1)

                # Player 2's turn and legal moves exist
                elif (game.get_current_turn() == 2 and game.isPossibleMove()):
                    if (player2 == 1):
                        do_human_move(2)
                    elif (player2 == 2):
                        do_ai_move(2)

                else:
                    game.clear_history()
                    flagEnd = True

            # Neither player has legal moves, game is over
            else:
                endScreen(screen)
        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


#############################################################
# Check if a valid move can be made, if it can be made then #
# place the piece and flip all the appropriate pieces that  #
# the player as captured                                    #
#############################################################
def do_human_move(player_number):
    if (game.place_piece((row, column), player_number)):
        game.flip_pieces((row, column))
        game.switchTurn()
        game.save_to_history()


#############################################################
# Perform the move of the AI player, then wait a second to  #
# make the game feel more realistic instead of instantanious#
#############################################################
def do_ai_move(player_number):
    time.sleep(1)  # Sleep for 1 second so user can see what the AI does
    move = ai.pick_next_move(game.get_current_layout())
    if (game.place_piece(move, player_number)):  # Returns True if place_piece succeeds
        game.flip_pieces(move)
        game.switchTurn()
        game.save_to_history()


#############################################################
# Function displays all buttons and text located on the     #
# the start screen. Including buttons for Easy, Difficult,  #
# 1 player, 2 player, going 1st, going 2nd, and the game    #
# start button. It Also displays the banner on the start    #
# page                                                      #
#############################################################
def startScreen(screen):
    global difficulty, players, start, running, turnOrder, player1, player2
    banner = pygame.image.load("gameBanner.jpg")
    screen.blit(banner, (400, 10))
    diff = []
    people = []
    turn = []
    if difficulty:
        diffBanner = "Diffculty: Easy"
    else:
        diffBanner = "Difficulty: Hard"
    Button(screen, (255, 255, 255), 200, 200, 100, 100, diffBanner)
    diff.append(Button(screen, (210, 210, 210), 100, 300, 100, 100, "Easy"))
    diff.append(Button(screen, (210, 210, 210), 300, 300, 100, 100, "Hard"))
    if players == 1:
        playerBanner = "Players : 1"
    else:
        playerBanner = "Players : 2"
    Button(screen, (255, 255, 255), 900, 200, 100, 100, playerBanner)
    people.append(Button(screen, (210, 210, 210), 800, 300, 100, 100, "1"))
    people.append(Button(screen, (210, 210, 210), 1000, 300, 100, 100, "2"))
    close = Button(screen, (34, 139, 34), 500, 570, 150, 100, "Play!")
    if turnOrder == 1:
        turnOrderBanner = "Turn Order: 1st"
    else:
        turnOrderBanner = "Turn Order: 2nd"
    Button(screen, (255, 255, 255), 900, 400, 100, 100, turnOrderBanner)
    turn.append(Button(screen, (210, 210, 210), 800, 500, 100, 100, "1st"))
    turn.append(Button(screen, (210, 210, 210), 1000, 500, 100, 100, "2nd"))

    position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # Did the user click?
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if diff[0].isOver(position):
                difficulty = True
                ai.setDifficulty(difficulty)

            if diff[1].isOver(position):
                difficulty = False
                ai.setDifficulty(difficulty)
            if people[0].isOver(position):
                players = 1
                player1 = 1
                player2 = 2
            if people[1].isOver(position):
                players = 2
                player1 = 1
                player2 = 1
            if turn[0].isOver(position):
                turnOrder = 1
                if (players == 1):  # If only one human player, set them to player 1, AI to player 2
                    player1 = 1
                    player2 = 2
                else:  # Else, two human players
                    player1 = 1
                    player2 = 1
            if turn[1].isOver(position):
                turnOrder = 2
                if (players == 1):  # If only one human, set them to player 2, AI to player 1
                    player1 = 2
                    player2 = 1
                else:  # Else, two human players
                    player1 = 1
                    player2 = 1
            if close.isOver(position):
                start = False

    pygame.display.update()

#############################################################
# Displays end sreen which will as user if they want to play#
# again as well as declare the winner                       # 
#############################################################
def endScreen(screen):
    screen.fill((255, 255, 255))
    displayEndButtons(screen)
    pygame.display.update()
    position = pygame.mouse.get_pos()
    eventListener(position)

#############################################################
# Function creates the new window to display help screen pic#
# and text information                                      #
#############################################################
def helpScreen():
    global alreadyFullScreen, running
    pygame.init()

    # Set up the drawing window
    if whatSize == 0:
        help = pygame.display.set_mode(screenSize)
        alreadyFullScreen = False
    else:
        help = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        alreadyFullScreen = True
    # Run until the user asks to quit
    run = True
    while run:
        if whatSize == 0:
            help = pygame.display.set_mode(screenSize)
            alreadyFullScreen = False
        else:
            if alreadyFullScreen == False:
                help = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Fill the background with white
        help.fill((255, 255, 255))

        # Write out the text
        font = pygame.font.SysFont('comicsans', 30)
        rules = "Othello Rules\nGame setup:\nThe game is played on an 8x8 grid. There are two color pieces (black or " \
                "white) to designate either player 1 or player 2. The two players that are trying to claim as much of " \
                "the board as possible with their designated pieces.\nGame Start:\nTo start the game place 4 pieces " \
                "in a diagonal pattern as seen in the photo below\n"
        picture = pygame.image.load("startBoard.gif")
        help.blit(picture, (30, 190))
        rules2 = "Game Capture:\nIn " \
                 "order to capture the opponents pieces it must be between your most recent placed piece and a " \
                 "previously placed piece of the same color. The capture can occur horizontally, vertically, " \
                 "and diagonally. If you are confused as to what a legal move is turn on the feature that shows all " \
                 "legal moves on the game board.\nGame Finish:\nThe Game is finished when neither player has a legal " \
                 "move, or one of the players resigns. The winner of the game is the player with the most pieces on " \
                 "the board, unless a player resigned. The player that resigns loses the game "

        myRect = pygame.Rect((20, 20, 1000, 160))
        myRect2 = pygame.Rect((20, 20, 1000, 400))

        text = renderText(rules, font, myRect, (0, 0, 0), (255, 255, 255), 0)
        text2 = renderText(rules2, font, myRect2, (0, 0, 0), (255, 255, 255), 0)

        if text:
            help.blit(text, myRect.topleft)
            help.blit(text2, myRect2.bottomleft)

        pygame.display.update()

#############################################################
# Code in the following function authored by                #
# http://www.pygame.org/pcr/text_rect/index.php             #
#############################################################
def renderText(string, font, rect, text_color, background_color, justification=0):
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

            # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
        accumulated_height += font.size(line)[1]

    return surface


mainGameLoop()
