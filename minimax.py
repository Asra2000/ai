X = "X"
O = "O"
empty = None

win_position = [[(0, 0), (1, 1), (2,2)],
                [(0, 0), (0, 1), (0,2)],
                [(1, 0), (1, 1), (1,2)],
                [(2, 0), (2, 1), (2,2)],
                [(0, 0), (1, 0), (2,0)],
                [(0, 1), (1, 1), (2,1)],
                [(0, 2), (1, 2), (2,2)],
                [(0, 2), (1, 1), (0,2)]]

class Board:
    def __init__(self):
        self.board = [[empty, empty, empty],
                      [empty, empty, empty],
                      [empty, empty, empty]]
        
    
    def check(self):
        # Returns X if playerX wins or O for other player
        # else returns None
        for pos in win_position:
            countX = 0
            countO = 0
            for i, j in pos:
                if self.board[i][j] == X:
                    countX += 1
                elif self.board[i][j] == O:
                    countO += 1
                
                if countX == 3:
                    return X
                elif countO == 3:
                    return O

        return empty

    def game_over(self):
        if self.check() != empty:
            return True

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == empty:
                    return False

        return True


    def place(self, i, j, move):
        self.board[i][j] = move

    def remove(self, i, j):
        self.board[i][j] = empty

    def is_available(self, i, j):
        return not (i >= len(self.board) or 
            j >= len(self.board[i]) or
            i < 0 or j < 0 or
            self.board[i][j] != empty)

    def play(self):
        
        if self.game_over():
            return

        move = self.turn()
        points = float("-inf") if move == X else float("inf")
        action = ()
    
        for i in range(3):
            for j in range(3):
                if self.is_available(i, j):
                    self.place(i, j, move)
                    cost = self.play_value(points)
                    self.remove(i, j)

                    if move == X:
                        cost = max(cost, points)
                    else :
                        cost = min(cost, points)

                    if cost != points:
                        points = cost
                        action = (i, j)

        return action
                
    def play_value(self, best_value):
        '''
            Added Alpha-Beta prunning
        '''
        if self.game_over():
            winner = self.check()
            return self.utility(winner)

        move = self.turn()
        current_point = float("-inf") if move == X else float("inf")

        for i in range(3):
            for j in range(3):
                if self.is_available(i, j):
                    self.place(i, j, move)
                    new_point = self.play_value(current_point)
                    self.remove(i, j)

                    if move == X:
                        if new_point > best_value:
                            return new_point
                        current_point = max(new_point, current_point)

                    else:
                        if new_point < best_value:
                            return new_point
                        current_point = min(new_point, current_point)

        return current_point


    def turn(self):

        countX = 0
        countO = 0

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == X:
                    countX += 1
                elif self.board[i][j] == O:
                    countO += 1
        
        if countX <= countO:
            return X
        return O

    def utility(self, winner):
        if winner == X:
            return 1
        elif winner == O:
            return -1
        return 0   

    def display(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j]:
                    print(self.board[i][j], end=" ")
                else:
                    print("-", end=" ")
            print("")

        print("")



def main():
    game = Board()

    while not game.game_over():
        turn = game.turn()
        print("Player", turn, "playing...")
        i, j = game.play()
        game.place(i, j, turn)
        game.display()

main()