# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import random


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, n, b, s, blocs, d1, d2, t, recommend=True):
        self.n = n
        self.b = b
        self.s = s
        self.blocs = blocs
        self.d1 = d1
        self.d2 = d2
        self.nb_of_evaluation_by_depth = [0]*(d1+1) if d1 > d2 else [0]*(d2+1)
        self.t = t
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):
        self.current_state = [["." for c in range(self.n)]
                              for r in range(self.n)]

        if(len(self.blocs) == 0):
            for _ in range(self.b):
                x = random.randint(0, self.n-1)
                y = random.randint(0, self.n-1)
                while self.current_state[x][y] != ".":
                    x = random.randint(0, self.n-1)
                    y = random.randint(0, self.n-1)

                self.current_state[x][y] = "*"
        else:
            for bloc in self.blocs:
                self.current_state[bloc[0]][bloc[1]] = "*"

        # Player X always plays first
        self.player_turn = "X"

    def draw_board(self):
        f = open(
            "gameTrace-" + str(self.n)+""+str(self.b)+""+str(self.s) + "" + str(self.t)+".txt", "a")
        print()
        f.write("\n")
        print("  ", end="")
        f.write("  ")
        for col in range(0, self.n):
            print(chr(col+65), end="")
            f.write(chr(col+65))
        print()
        f.write("\n")

        print(" +", end="")
        f.write(" +")
        for col in range(0, self.n):
            print("-", end="")
            f.write("-")
        print()
        f.write("\n")

        for y in range(0, self.n):
            print(str(y)+"|", end="")
            f.write(str(y)+"|")
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
                f.write(F'{self.current_state[x][y]}')
            print()
            f.write("\n")
        print()
        f.write("\n")

    def is_valid(self, px, py):
        if px < 0 or px >= self.n or py < 0 or py >= self.n:
            return False
        elif self.current_state[px][py] != ".":
            return False
        else:
            return True

    def is_end(self):
        # Horizontal win
        for i in range(self.n-self.s+1):
            for j in range(self.n):
                if(self.current_state[i][j] != '.' and self.current_state[i][j] != '*'):
                    win = True
                    for s in range(self.s):
                        if(self.current_state[i][j] != self.current_state[i+s][j]):
                            win = False
                    if win:
                        return self.current_state[i][j]
        # Vertical win
        for i in range(self.n):
            for j in range(self.n-self.s+1):
                if(self.current_state[i][j] != '.' and self.current_state[i][j] != '*'):
                    win = True
                    for s in range(self.s):
                        if(self.current_state[i][j] != self.current_state[i][j+s]):
                            win = False
                    if win:
                        return self.current_state[i][j]
        # Diagonal win
        for i in range(self.n-self.s+1):
            for j in range(self.n-self.s+1):
                if(self.current_state[i][j] != '.' and self.current_state[i][j] != '*'):
                    win = True
                    for s in range(self.s):
                        if(self.current_state[i][j] != self.current_state[i+s][j+s]):
                            win = False
                    if win:
                        return self.current_state[i][j]
                if(self.current_state[i][j+self.s-1] != '.' and self.current_state[i][j+self.s-1] != '*'):
                    win = True
                    for s in range(self.s):
                        if(self.current_state[i][j+self.s-1] != self.current_state[i+s][j+self.s-1-s]):
                            win = False
                    if win:
                        return self.current_state[i][j+self.s-1]

        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == "."):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        final_data = []
        f = open(
            "gameTrace-" + str(self.n)+""+str(self.b)+""+str(self.s) + "" + str(self.t)+".txt", "a")
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
                f.write('The winner is X!\n')
            elif self.result == 'O':
                print('The winner is O!')
                f.write('The winner is O!\n')
            elif self.result == '.':
                print("It's a tie!")
                f.write("It's a tie!\n")
            self.initialize_game()
            print()
            f.write("\n")

            evaluation_time = 0
            nb_of_e_evaluation = 0
            nb_of_evaluation_by_depth = [
                0]*(self.d1+1) if self.d1 > self.d2 else [0]*(self.d2+1)
            average_evaluation_depth = 0
            average_recursion_depth = 0
            for data in self.data:
                evaluation_time += data[0]
                nb_of_e_evaluation += data[1]
                for i in range(len(data[2])):
                    nb_of_evaluation_by_depth[i] += data[2][i]
                average_evaluation_depth += data[3]
                average_recursion_depth += data[4]

            print(
                F'i\tEvaluation time: {round(evaluation_time/len(self.data), 7)}s')
            print(
                F'ii\tHeuristic evaluations: {nb_of_e_evaluation}')
            print(
                F'iii\tEvaluations by depth: {{', end="")
            for i in range(len(nb_of_evaluation_by_depth)):
                if nb_of_evaluation_by_depth[i] != 0:
                    print(
                        "-"+str(i)+": "+str(nb_of_evaluation_by_depth[i])+"-", end="")
            print("}")
            print(
                F'iv\tAverage evaluation depth: {average_evaluation_depth/len(self.data)}')
            print(
                F'v\tAverage recursion depth: {average_recursion_depth/len(self.data)}')
            print(
                F'vi\tTotal moves: {len(self.data)}')

            f.write(
                F'i\tEvaluation time: {round(evaluation_time/len(self.data), 7)}s\n')
            f.write(
                F'ii\tHeuristic evaluations: {nb_of_e_evaluation}\n')
            f.write(
                F'iii\tEvaluations by depth: {{')
            for i in range(len(nb_of_evaluation_by_depth)):
                if nb_of_evaluation_by_depth[i] != 0:
                    f.write(
                        "-"+str(i)+": "+str(nb_of_evaluation_by_depth[i])+"-")
            f.write("}\n")
            f.write(
                F'iv\tAverage evaluation depth: {average_evaluation_depth/len(self.data)}\n')
            f.write(
                F'v\tAverage recursion depth: {average_recursion_depth/len(self.data)}\n')
            f.write(
                F'vi\tTotal moves: {len(self.data)}\n\n')

            final_data = [round(evaluation_time/len(self.data), 7), nb_of_e_evaluation, nb_of_evaluation_by_depth,
                          average_evaluation_depth/len(self.data), average_recursion_depth/len(self.data), len(self.data), self.result, self.switch_sides]

        f.close()

        return (self.result, final_data)

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            try:
                px = ord(input('enter the column letter: ').upper())-65
                py = int(input('enter the row index: '))
                if self.is_valid(px, py):
                    return (px, py)
                else:
                    print('The move is not valid! Try again.')
            except:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def e1(self):
        self.nb_of_e_evaluation += 1
        v = 0
        for i in range(self.n):
            nb_of_x = 0
            nb_of_o = 0
            for j in range(self.n):
                if self.current_state[i][j] == "X":
                    nb_of_x += 1
                if self.current_state[j][i] == "X":
                    nb_of_x += 1
                if self.current_state[i][j] == "O":
                    nb_of_o += 1
                if self.current_state[j][i] == "O":
                    nb_of_o += 1

                v -= pow(2, nb_of_x)
                v += pow(2, nb_of_o)

        return v

    def e2(self, max):
        self.nb_of_e_evaluation += 1
        nb_of_adj_x = 0
        nb_of_adj_o = 0
        nb_of_open_x = 0
        nb_of_open_o = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == "X":
                    if i != 0:
                        if self.current_state[i-1][j] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i-1][j] == "X":
                            nb_of_adj_x += 1

                        if j != self.n-1:
                            if self.current_state[i-1][j+1] == ".":
                                nb_of_open_x += 1
                            elif self.current_state[i-1][j+1] == "X":
                                nb_of_adj_x += 1

                    if i != self.n-1:
                        if self.current_state[i+1][j] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i+1][j] == "X":
                            nb_of_adj_x += 1

                        if j != 0:
                            if self.current_state[i+1][j-1] == ".":
                                nb_of_open_x += 1
                            elif self.current_state[i+1][j-1] == "X":
                                nb_of_adj_x += 1

                    if j != 0:
                        if self.current_state[i][j-1] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i][j-1] == "X":
                            nb_of_adj_x += 1
                    if j != self.n-1:
                        if self.current_state[i][j+1] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i][j+1] == "X":
                            nb_of_adj_x += 1

                    if i != 0 and j != 0:
                        if self.current_state[i-1][j-1] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i-1][j-1] == "X":
                            nb_of_adj_x += 1
                    if i != self.n-1 and j != self.n-1:
                        if self.current_state[i+1][j+1] == ".":
                            nb_of_open_x += 1
                        elif self.current_state[i+1][j+1] == "X":
                            nb_of_adj_x += 1

                if self.current_state[i][j] == "O":
                    if i != 0:
                        if self.current_state[i-1][j] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i-1][j] == "O":
                            nb_of_adj_o += 1

                        if j != self.n-1:
                            if self.current_state[i-1][j+1] == ".":
                                nb_of_open_o += 1
                            elif self.current_state[i-1][j+1] == "O":
                                nb_of_adj_o += 1

                    if i != self.n-1:
                        if self.current_state[i+1][j] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i+1][j] == "O":
                            nb_of_adj_o += 1

                        if j != 0:
                            if self.current_state[i+1][j-1] == ".":
                                nb_of_open_o += 1
                            elif self.current_state[i+1][j-1] == "O":
                                nb_of_adj_o += 1

                    if j != 0:
                        if self.current_state[i][j-1] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i][j-1] == "O":
                            nb_of_adj_o += 1
                    if j != self.n-1:
                        if self.current_state[i][j+1] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i][j+1] == "O":
                            nb_of_adj_o += 1

                    if i != 0 and j != 0:
                        if self.current_state[i-1][j-1] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i-1][j-1] == "O":
                            nb_of_adj_o += 1
                    if i != self.n-1 and j != self.n-1:
                        if self.current_state[i+1][j+1] == ".":
                            nb_of_open_o += 1
                        elif self.current_state[i+1][j+1] == "O":
                            nb_of_adj_o += 1

        if max:
            nb_of_adj_o *= 3
            nb_of_adj_x *= 2
        else:
            nb_of_adj_x *= 3
            nb_of_adj_o *= 2

        return 15 * (nb_of_adj_o - nb_of_adj_x) + 10 * (nb_of_open_o - nb_of_open_x)

    def minimax(self, depth=0, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -infinity - win for 'X'
        # 0  - a tie
        # infinity  - loss for 'X'
        # We're initially setting it to infinity or -infinity as worse than the worst case:
        ard = 0
        value = 10000000000000000
        if max:
            value = -10000000000000000

        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-10000000000000000, x, y, ard)
        elif result == 'O':
            return (10000000000000000, x, y, ard)
        elif result == '.':
            return (0, x, y, ard)

        if round(time.time() - self.start, 7) >= self.t:
            return (value, x, y, ard)

        nb_of_nodes = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    nb_of_nodes += 1
                    if max:
                        self.current_state[i][j] = 'O'
                        if(depth == self.d2):
                            self.nb_of_evaluation_by_depth[depth] += 1
                            v = self.e2(max)
                            ard += depth
                        else:
                            (v, _, _, a) = self.minimax(
                                depth=depth+1, max=False)
                            ard += a
                        if v >= value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        if(depth == self.d1):
                            self.nb_of_evaluation_by_depth[depth] += 1
                            v = self.e1()
                            ard += depth
                        else:
                            (v, _, _, a) = self.minimax(
                                depth=depth+1, max=True)
                            ard += a
                        if v <= value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y, ard/nb_of_nodes)

    def alphabeta(self, alpha=-10000000000000000, beta=10000000000000000, depth=0, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -infinity - win for 'X'
        # 0  - a tie
        # infinity  - loss for 'X'
        # We're initially setting it to infinity or -infinity as worse than the worst case:
        ard = 0
        value = 10000000000000000
        if max:
            value = -10000000000000000

        x = None
        y = None

        result = self.is_end()
        if result == 'X':
            return (-10000000000000000, x, y, ard)
        elif result == 'O':
            return (10000000000000000, x, y, ard)
        elif result == '.':
            return (0, x, y, ard)

        if round(time.time() - self.start, 7) >= self.t:
            self.nb_of_evaluation_by_depth[depth] += 1
            if max:
                if self.switch_sides:
                    value = self.e1()
                else:
                    value = self.e2(max)
            else:
                if self.switch_sides:
                    value = self.e2(max)
                else:
                    value = self.e1()
            ard += depth
            return (value, x, y, ard)

        nb_of_nodes = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    nb_of_nodes += 1
                    if max:
                        self.current_state[i][j] = 'O'
                        if(depth == self.d2):
                            self.nb_of_evaluation_by_depth[depth] += 1
                            if self.switch_sides:
                                v = self.e1()
                            else:
                                v = self.e2(max)
                            ard += depth
                        else:
                            (v, _, _, a) = self.alphabeta(
                                alpha, beta, depth=depth+1, max=False)
                            ard += a
                        if v >= value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        if(depth == self.d1):
                            self.nb_of_evaluation_by_depth[depth] += 1
                            if self.switch_sides:
                                v = self.e2(max)
                            else:
                                v = self.e1()
                            ard += depth
                        else:
                            (v, _, _, a) = self.alphabeta(
                                alpha, beta, depth=depth+1, max=True)
                            ard += a
                        if v <= value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y, ard/nb_of_nodes)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y, ard/nb_of_nodes)
                        if value < beta:
                            beta = value
        return (value, x, y, ard/nb_of_nodes)

    def play(self, algo=None, player_x=None, player_o=None, switch_sides=False):
        self.data = []
        self.switch_sides = switch_sides

        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            (result, final_data) = self.check_end()
            if result:
                return final_data
            self.nb_of_e_evaluation = 0
            for i in range(len(self.nb_of_evaluation_by_depth)):
                self.nb_of_evaluation_by_depth[i] = 0
            self.start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y, ard) = self.minimax(max=False)
                else:
                    (_, x, y, ard) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y, ard) = self.alphabeta(max=False)
                else:
                    (m, x, y, ard) = self.alphabeta(max=True)
            end = time.time()
            f = open(
                "gameTrace-" + str(self.n)+""+str(self.b)+""+str(self.s) + "" + str(self.t)+".txt", "a")
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Recommended move: {chr(x+65)}{y}')
                    f.write(F'Recommended move: {chr(x+65)}{y}\n')
                    print()
                    f.write("\n")
                    print(F'i\tEvaluation time: {round(end - self.start, 7)}s')
                    f.write(
                        F'i\tEvaluation time: {round(end - self.start, 7)}s\n')
                    print(
                        F'ii\tHeuristic evaluations: {self.nb_of_e_evaluation}')
                    f.write(
                        F'ii\tHeuristic evaluations: {self.nb_of_e_evaluation}\n')
                    print(
                        F'iii\tEvaluations by depth: {{', end="")
                    f.write(
                        F'iii\tEvaluations by depth: {{')
                    total_evaluation_depth = 0
                    for i in range(len(self.nb_of_evaluation_by_depth)):
                        total_evaluation_depth += i * \
                            self.nb_of_evaluation_by_depth[i]
                        if self.nb_of_evaluation_by_depth[i] != 0:
                            print(
                                "-{i}: {self.nb_of_evaluation_by_depth[i]}-", end="")
                            f.write(
                                "-{i}: {self.nb_of_evaluation_by_depth[i]}-")
                    print("}")
                    f.write("}\n")
                    print(
                        F'iv\tAverage evaluation depth: {total_evaluation_depth/self.nb_of_e_evaluation}')
                    f.write(
                        F'iv\tAverage evaluation depth: {total_evaluation_depth/self.nb_of_e_evaluation}\n')
                    print(
                        F'v\tAverage recursion depth: {ard}')
                    f.write(
                        F'v\tAverage recursion depth: {ard}\n')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(
                    F'Player {self.player_turn} under AI control plays: {chr(x+65)}{y}')
                f.write(
                    F'Player {self.player_turn} under AI control plays: {chr(x+65)}{y}\n')
                print()
                f.write("\n")
                print(F'i\tEvaluation time: {round(end - self.start, 7)}s')
                f.write(F'i\tEvaluation time: {round(end - self.start, 7)}s\n')
                print(
                    F'ii\tHeuristic evaluations: {self.nb_of_e_evaluation}')
                f.write(
                    F'ii\tHeuristic evaluations: {self.nb_of_e_evaluation}\n')
                print(
                    F'iii\tEvaluations by depth: {{', end="")
                f.write(
                    F'iii\tEvaluations by depth: {{')
                total_evaluation_depth = 0
                for i in range(len(self.nb_of_evaluation_by_depth)):
                    total_evaluation_depth += (i *
                                               self.nb_of_evaluation_by_depth[i])
                    if self.nb_of_evaluation_by_depth[i] != 0:
                        print(
                            "-"+str(i)+": "+str(self.nb_of_evaluation_by_depth[i])+"-", end="")
                        f.write(
                            "-"+str(i)+": "+str(self.nb_of_evaluation_by_depth[i])+"-")
                print("}")
                f.write("}\n")
                average_evaluation_depth = total_evaluation_depth / \
                    (self.nb_of_e_evaluation if self.nb_of_e_evaluation != 0 else 1)
                print(
                    F'iv\tAverage evaluation depth: {average_evaluation_depth}')
                f.write(
                    F'iv\tAverage evaluation depth: {average_evaluation_depth}\n')
                print(
                    F'v\tAverage recursion depth: {ard}')
                f.write(
                    F'v\tAverage recursion depth: {ard}\n')
            f.close()
            self.data.append([round(end - self.start, 7), self.nb_of_e_evaluation,
                             self.nb_of_evaluation_by_depth.copy(), average_evaluation_depth, ard])
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def inputManager():
    n = int(input("Enter the size of the board – n – an integer in [3..10]: "))

    b = int(input("Enter the number of blocs – b – an integer in [0..2n]: "))
    blocs = []
    if b > 0:
        randomBlocs = input(
            "Generate random positions for the blocs?(Y|N) ").upper() == "Y"

        if not randomBlocs:
            for blocIndex in range(b):
                x = int(
                    input("Enter x coordinate of bloc #{}: ".format(blocIndex+1)))
                y = int(
                    input("Enter y coordinate of bloc #{}: ".format(blocIndex+1)))
                blocs.append([x, y])

    s = int(
        input("Enter the winning line-up size – s – an integer in [3..n]: "))

    d1 = int(input(
        "Enter the maximum depth of the adversarial search for player 1 – d1 – an integer: "))
    d2 = int(input(
        "Enter the maximum depth of the adversarial search for player 2 – d2 – an integer: "))
    t = float(
        input("Enter the maximum allowed time (in seconds) to return a move – t: "))

    a = Game.ALPHABETA if input(
        "Enter a Boolean to force the use of either minimax (FALSE) or alphabeta (TRUE) – a: ").upper() == "TRUE" else Game.MINIMAX

    playMode = input(
        "Enter the play mode (H-H | H-AI | AI-H | AI-AI): ").upper()
    if playMode == "H-H" or playMode == "H-AI":
        player_x = Game.HUMAN
    else:
        player_x = Game.AI

    if playMode == "H-H" or playMode == "AI-H":
        player_o = Game.HUMAN
    else:
        player_o = Game.AI

    return (n, b, s, blocs, d1, d2, t, a, player_x, player_o)


def main():
    (n, b, s, blocs, d1, d2, t, a, player_x, player_o) = inputManager()

    #n = 8
    #b = 7
    #s = 6
    #t = 5
    #d1 = 6
    #d2 = 6
    #blocs = []
    #player_x = Game.AI
    #player_o = Game.AI
    #a = Game.ALPHABETA

    g = Game(n, b, s, blocs, d1, d2, t, recommend=True)

    with open("gameTrace-" + str(n)+""+str(b)+""+str(s) + "" + str(t)+".txt", "a") as f:
        f.write("n="+str(n)+" b="+str(b)+" s="+str(s)+" t="+str(t)+"\n")
        f.write("blocs = "+str(blocs)+"\n")

        player1 = "AI" if player_x == Game.AI else "HUMAN"
        player2 = "AI" if player_o == Game.AI else "HUMAN"
        f.write("Player 1: "+str(player1)+" d = " +
                str(d1)+" a = "+str(a)+" e1\n")
        f.write("Player 2: "+str(player2)+" d = " +
                str(d2)+" a = "+str(a)+" e2\n")

    data = []
    r = 10
    for _ in range(int(r/2)):
        data.append(g.play(algo=a, player_x=player_x,
                    player_o=player_o, switch_sides=False))
    for _ in range(int(r/2)):
        data.append(g.play(algo=a, player_x=player_x,
                    player_o=player_o, switch_sides=True))

    with open("scoreboard.txt", "a") as f:
        evaluation_time = 0
        nb_of_e_evaluation = 0
        nb_of_evaluation_by_depth = [
            0]*(d1+1) if d1 > d2 else [0]*(d2+1)
        average_evaluation_depth = 0
        average_recursion_depth = 0
        moves = 0
        total_wins_e1 = 0
        total_wins_e2 = 0
        for d in data:
            evaluation_time += d[0]
            nb_of_e_evaluation += d[1]
            for i in range(len(d[2])):
                nb_of_evaluation_by_depth[i] += d[2][i]
            average_evaluation_depth += d[3]
            average_recursion_depth += d[4]
            moves += d[5]
            if d[6] != ".":
                if d[7]:
                    if d[6] == "X":
                        total_wins_e2 += 1
                    else:
                        total_wins_e1 += 1
                else:
                    if d[6] == "X":
                        total_wins_e1 += 1
                    else:
                        total_wins_e2 += 1

        f.write("n="+str(n)+" b="+str(b)+" s="+str(s)+" t="+str(t)+"\n")

        f.write("Player 1: d="+str(d1)+" a="+str(a)+"\n")
        f.write("Player 2: d="+str(d2)+" a="+str(a)+"\n")

        f.write(str(len(data))+" games\n")

        f.write(
            "Total wins for heuristic e1: "+str(total_wins_e1)+" ("+str(round(total_wins_e1/len(data)*100, 1))+" %)\n")
        f.write(
            "Total wins for heuristic e2: "+str(total_wins_e2)+" ("+str(round(total_wins_e2/len(data)*100, 1))+" %)\n")
        f.write(
            "Total ties: "+str(len(data)-total_wins_e1-total_wins_e2)+" ("+str(round((len(data)-total_wins_e1-total_wins_e2)/len(data)*100, 1))+" %)\n")

        f.write(
            F'i\tAverage evaluation time: {round(evaluation_time/len(data), 7)}s\n')
        f.write(
            F'ii\tTotal heuristic evaluations: {nb_of_e_evaluation}\n')
        f.write(
            F'iii\tEvaluations by depth: {{')
        for i in range(len(nb_of_evaluation_by_depth)):
            if nb_of_evaluation_by_depth[i] != 0:
                f.write(
                    "-"+str(i)+": "+str(nb_of_evaluation_by_depth[i])+"-")
        f.write("}\n")
        f.write(
            F'iv\tAverage evaluation depth: {average_evaluation_depth/len(data)}\n')
        f.write(
            F'v\tAverage recursion depth: {average_recursion_depth/len(data)}\n')
        f.write(
            F'vi\tAverage moves per game: {moves/len(data)}\n\n')


if __name__ == "__main__":
    main()
