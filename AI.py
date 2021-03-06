import random

#############################################################
# Class used to define the opponent, this creates automated #
# Moves for a human to play against if they are the only one#
# playing the game                                          #
#############################################################
class opponent():
    def __init__(self, isEasy):
        self.easyDiff = isEasy
        self.possibleMove = True
    
    #############################################################
    # Generate a move based on a random selection of possible   #
    # moves                                                     #
    #############################################################
    def pick_next_move_easy(self, gameBoard):
        currentLayout = gameBoard
        possibleMoveList = []
        possible_move = 3
        for row in range(len(currentLayout)):
            for piece in range(len(currentLayout)):
                #print(currentLayout[row][piece])
                if (currentLayout[row][piece] == possible_move):
                    columnIndex = piece
                    rowIndex = row
                    #print("Row: " + str(rowIndex) + " Column: " + str(columnIndex))
                    possibleMoveList.append((rowIndex, columnIndex))
        if (len(possibleMoveList) > 0):
            move = random.choice(possibleMoveList)
            #print(move)
            return move
    #############################################################
    # Select a legal move from a list of possible moves.        #
    # This function picks some moves over others as it will lead#
    # to a more likely victory see ideal moves below            #
    #############################################################
    def pick_next_move_difficult(self, gameBoard):
        #Ideal moves for the gameBoard
        #If one of these moves is available take it
        ###################
        # 1 0 2 0 0 2 0 1 #
        # 0 0 0 0 0 0 0 0 #
        # 2 0 3 0 0 3 0 2 #
        # 0 0 0 0 0 0 0 0 #
        # 0 0 0 0 0 0 0 0 #
        # 2 0 3 0 0 3 0 2 #
        # 0 0 0 0 0 0 0 0 #
        # 1 0 2 0 0 2 0 1 #
        ###################
        currentLayout = gameBoard
        tier_one = []
        tier_two = []
        tier_three = []
        possibleMoveList = []
        possible_move = 3
        
        #Add Tier One Moves
        if (currentLayout[0][0] == possible_move):
            tier_one.append((0, 0))
        if (currentLayout[0][7] == possible_move):
            tier_one.append((0, 7))
        if (currentLayout[7][0] == possible_move):
            tier_one.append((7, 0))
        if (currentLayout[7][7] == possible_move):
            tier_one.append((7, 7))
            
        #Add Tier Two Moves
        if (currentLayout[0][2] == possible_move):
            tier_two.append((0, 2))
        if (currentLayout[0][5] == possible_move):
            tier_two.append((0, 5))
        if (currentLayout[2][0] == possible_move):
            tier_two.append((2, 0))
        if (currentLayout[2][7] == possible_move):
            tier_two.append((2, 7))
        if (currentLayout[5][0] == possible_move):
            tier_two.append((5, 0))
        if (currentLayout[5][7] == possible_move):
            tier_two.append((5, 7))
        if (currentLayout[7][2] == possible_move):
            tier_two.append((7, 2))
        if (currentLayout[7][5] == possible_move):
            tier_two.append((7, 5))
        #Add Tier Three Moves
        if (currentLayout[2][2] == possible_move):
            tier_three.append((2, 2))
        if (currentLayout[5][2] == possible_move):
            tier_three.append((5, 2))
        if (currentLayout[5][2] == possible_move):
            tier_three.append((5, 2))
        if (currentLayout[5][5] == possible_move):
            tier_three.append((5, 5))
        
        for row in range(len(currentLayout)):
            for piece in range(len(currentLayout)):
                #print(currentLayout[row][piece])
                if (currentLayout[row][piece] == possible_move):
                    columnIndex = piece
                    rowIndex = row
                    #print("Row: " + str(rowIndex) + " Column: " + str(columnIndex))
                    possibleMoveList.append((rowIndex, columnIndex))
        
        #
        #Check for tier moves in order
        if (len(tier_one) > 0):
            move = random.choice(tier_one)
            return move     
        elif (len(tier_two) > 0):
            move = random.choice(tier_two)
            return move
        elif (len(tier_three) > 0):
            move = random.choice(tier_three)
            return move
        elif (len(possibleMoveList) > 0):
            move = random.choice(possibleMoveList)
            return move
            
    #############################################################
    # Pick the next move based on whether easy or difficult game#
    # play has been selected                                    #
    #############################################################
    def pick_next_move(self, gameBoard):
        if (self.easyDiff):
            return self.pick_next_move_easy(gameBoard)
        else:
            return self.pick_next_move_difficult(gameBoard)
            
    #############################################################
    # Set whether this AI has a possible move                   #
    #############################################################    
    def setPossibleMove(self, possible):
        self.possibleMove = possible
    #############################################################
    # Get whether this AI has a possible move                   #
    #############################################################  
    def getPossibleMove(self):
        return self.possibleMove
        
    #############################################################
    # Set difficulty of the AI player for the game              #
    #############################################################
    def setDifficulty(self, isEasy):
        self.easyDiff = isEasy