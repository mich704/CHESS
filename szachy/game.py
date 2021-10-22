from pieces import *
import winsound as ws
from threading import Thread
from buttons import *



class Game(object):
    """
        Args:
            dark_sqaures_color (str): color specifier string for dark sqaures color 
            light_sqaures_color (str): color specifier string for light sqaures color 
            buttons_color (str): color specifier string for buttons color 

            move_sound (str): stores path to move sound
            choise_sound (str): stores path to choise sound
            take_sound (str): stores path to take sound
            error_sound (str): stores path to error sound
            restore_sound (str): stores path to restore sound

            win (graphics.GraphWin): window in which game is displayed
            mega_board (list): all previous board states
            board (list): current board state
            chosen_piece (Piece): piece that set_starting_position clicked on
            chosen_piece_highlight (graphics.Rectangle): sqaure that marks chosen piece
            eg_window (graphics.GraphWin): window which pop up when the game ends 
            turn (str): color of player which turn it currently is
            pieces (dict): stores all pieces according to color

            prevButton (Button): button used to rewind moves
            nextButton (Button): button used to forward moves
            RestorePosition (Button): button used to Restore position
            NewGameButton (Button): button used to iniciate new game
            
            c_board_nr (int): index of currently diplayed board
            lp_reps (list): list of numbers indicating on which move last possible repetition could have occured
            moves_no_take (int): number of moves in row whithout taking 
    """
    
    dark_sqaures_color = color_rgb(152, 6, 171)
    light_sqaures_color = color_rgb(216, 162, 223)
    buttons_color = color_rgb(240, 152, 251)

    move_sound = 'sounds/move.wav'
    choise_sound = 'sounds/choise.wav'
    take_sound = 'sounds/take.wav'
    error_sound = 'sounds/error.wav'
    restore_sound = 'sounds/restore.wav'
    end_sound = 'sounds/end.wav'
    
    def __init__(self):
        self.mega_board = []
        self.board = [[None for x in range(8)] for y in range(8)]

        self._chosen_piece = None
        self.chosen_piece_highlight = None

        self.win = GraphWin("Chess", 1000, 800)
        self.win.setBackground(Game.dark_sqaures_color)
        self.eg_window = None

        self.turn = 'white'

        self.pieces = {
            'black': [],
            'white': []
        }

        self.prevButton = prevButton(
            self.win,
            "black",
            Game.buttons_color,
            20,
            5,
            860,
            400)

        self.nextButton = nextButton(
            self.win,
            "black",
            Game.buttons_color,
            20,
            5,
            860,
            400)

        self.RestorePosition = RestorePosition(
            self.win,
            Game.buttons_color,
            "black",
            5,
            850,
            950,
            455,
            505,
            "RESTORE\nTHIS\nPOSITION")

        self.NewGameButton = RestorePosition(
            self.win,
            Game.buttons_color,
            "black",
            5,
            850,
            950,
            50,
            100,
            "NEW GAME")

        self.c_board_nr = 0
        self.lp_reps = [0]


        self.moves_no_take = 0



    @property
    def chosen_piece(self):
        return self._chosen_piece

    @chosen_piece.setter
    def chosen_piece(self, chosen_piece):
        """
            Description:
                Set chosen_piece
                Assigns and unassings highlight to chosen piece

            Parameters:
                chosen_piece (Piece): piece clicked on by player
        """

        self._chosen_piece = chosen_piece

        if self.chosen_piece_highlight != None:
            self.chosen_piece_highlight.undraw()

        if chosen_piece != None:
            self.chosen_piece_highlight = Rectangle(
                Point(chosen_piece.x * 100, chosen_piece.y * 100),
                Point(chosen_piece.x * 100 + 100, chosen_piece.y * 100+ 100))

            self.chosen_piece_highlight.setWidth(3)
            self.chosen_piece_highlight.draw(self.win)

    def play_sound(self, sound):
        """
            Description:
                Creates new thread  
                Plays sounds in the new thread

            Parameters:
                sound (str): path to chosen sounds
        """
        
        soundThread = Thread(target = self.play_sound_thread, args=[sound])
        soundThread.start()

    def play_sound_thread(self, sound):
        """
            Description:
                Target function for thread

            Parameters:
                sound (str): path to chosen sounds
        """

        ws.PlaySound(sound, ws.SND_ASYNC)



    def draw_chosen_board(self, board_nr):
        """
            Description:
                Draws chosen board

            Parameters:
                board_nr (int): number of the board to be drawn
        """

        if board_nr in range(0, len(self.mega_board)):
            self.play_sound(Game.choise_sound)

            borad_to_draw = self.mega_board[board_nr]

            to_draw = []

            for y in range(8):
                for x in range(8):
                    if self.mega_board[self.c_board_nr][y][x] != borad_to_draw[y][x]:
                        if self.mega_board[self.c_board_nr][y][x] != None:
                            self.mega_board[self.c_board_nr][y][x].undraw_piece() #undraw current pieces
                            
                        if borad_to_draw[y][x] != None:
                            to_draw.append((borad_to_draw[y][x], y, x))

            for p in to_draw:
                p[0].draw_piece(p[1], p[2])
                            

            self.c_board_nr = board_nr
        
    
            self.refresh_buttons()

        else:
            self.play_sound(Game.error_sound)

        

    def refresh_buttons(self):
        """
            Description:
                checks if prev and next buttons are available to click
        """


        if self.c_board_nr > 0:
            self.prevButton.activate()
        else:
            self.prevButton.deactivate()

        
        if self.c_board_nr < len(self.mega_board) - 1:
            self.nextButton.activate()
            self.RestorePosition.draw_button()
        else:
            self.nextButton.deactivate()
            self.RestorePosition.undraw_button()





    def set_piece(self, y, x, piece, color, win):
        """
            Description:
                assigns given piece to given place
        """
        
        self.board[y][x] = piece(color, y, x, win)

        if piece == King:
            self.pieces[color].insert(0, self.board[y][x])  #king have to be first in list
        else:
            self.pieces[color].append(self.board[y][x])

        


    def set_starting_position(self):
        """
            Description:
                assings all piece to their starting places
        """

        for x in range(8):
            self.set_piece(6, x, Pawn, 'white', self.win) #set pawns
            self.set_piece(1, x, Pawn, 'black', self.win) #set pawns
        
        self.set_piece(7, 1, Knight, 'white', self.win) #set knights
        self.set_piece(0, 1, Knight, 'black', self.win) #set knights
        
        self.set_piece(7, 6, Knight, 'white', self.win) #set knights
        self.set_piece(0, 6, Knight, 'black', self.win) #set knights 
        
        
        self.set_piece(7, 0, Rook, 'white', self.win) #set rooks
        self.set_piece(0, 0, Rook, 'black', self.win) #set rooks
        
        self.set_piece(7, 7, Rook, 'white', self.win) #set rooks
        self.set_piece(0, 7, Rook, 'black', self.win) #set rooks
        
        
        self.set_piece(7, 2, Bishop, 'white', self.win) #set bisops
        self.set_piece(0, 2, Bishop, 'black', self.win) #set bishops
        
        self.set_piece(7, 5, Bishop, 'white', self.win) #set bisops
        self.set_piece(0, 5, Bishop, 'black', self.win) #set bishops 
        
        
        self.set_piece(7, 3, Queen, 'white', self.win) #set queens
        self.set_piece(0, 3, Queen, 'black', self.win) #set queens
        

        self.set_piece(7, 4, King, 'white', self.win) #set kings
        self.set_piece(0, 4, King, 'black', self.win) #set kings
            

        self.mega_board.append(self.deepcopy(self.board))
                  

    def draw_board(self):
        
        """
            Description:
                Draws board (backround)
                Draws fields legend
        """
        for y in range(8):
            for x in range(8):
                
                square = Rectangle(
                    Point(100 * y, 100 *x ),
                    Point(100 * y + 100, 100 *x +100))

                square.setWidth(0)
                

                if y%2 != x%2:
                    square.setFill(Game.dark_sqaures_color)
                else:
                    square.setFill(Game.light_sqaures_color)

                square.draw(self.win)

        for i in range(8):
            txt = Text(Point(100 * i + 90, 790), chr(65 + i))
            txt.setStyle("bold")
            txt.setFace("courier")

            if i%2 == 1:
                txt.setFill(Game.dark_sqaures_color)
            else:
                txt.setFill(Game.light_sqaures_color)

            txt.draw(self.win)
            
            txt = Text(Point(10, 100 * i + 10), 8 - i)
            txt.setStyle("bold")
            txt.setFace("courier")

            if i%2 == 0:
                txt.setFill(Game.dark_sqaures_color)
            else:
                txt.setFill(Game.light_sqaures_color)

            txt.draw(self.win)

                

    def draw_pieces(self):
        """
            Description:
                Draws all piece that are set on the board
        """
        for p in self.pieces['white'] + self.pieces['black']:
            p.draw_piece()

    def draw_menu(self):
        """
            Description:
                Draws sepparating line
                Draws all buttons in menu
        """

        sepLine = Line(Point(803, 0), Point(803,800))
        sepLine.setFill("black")
        sepLine.setWidth(6)
        sepLine.draw(self.win)

        self.NewGameButton.draw_button()
        self.prevButton.draw_button()
        self.nextButton.draw_button()
        

    def find_all_moves(self):
        """
            Description:
                Finds every move of all pieces on the board assings them to accordingpieces
        """
        
        mate = True
        
        for piece in self.pieces[self.turn]:
            if isinstance(piece, Pawn) and self.c_board_nr > 1:
                piece.moves = piece.all_moves(self.board, self.mega_board[-2])
            else:
                piece.moves = piece.all_moves(self.board)

            if piece.moves != []:
                  mate = False


        king = self.pieces[self.turn][0]

        if mate:

            if king.king_safe(king.y, king.x, self.board):
                self.endgame_window(" stalemate", True)

            else:
                self.endgame_window(" checkmate", False)
                

        if self.insufficient_material():
            self.endgame_window(" insufficient\n material", True)

        if self.threefold_repetition():
            self.endgame_window(" threefold\n repetition", True) 

        if self.fifty_moves_rule():
            self.endgame_window(" 50 moves\n rule", True)
                
        
    def draw_chosen_piece_moves(self):
        """
            Description:
                Draws moves of chosen piece on the board
        """
        for move in self.chosen_piece.moves:
            move.draw_move()
        

    def undraw_chosen_piece_moves(self):
        """
            Description:
                Undraws moves of chosen piece from the board
        """
        for move in self.chosen_piece.moves:
            move.undraw_move()




    def make_move(self, x, y):
        
        """
            Description:
                Checks if square that player clicked on is square on which chosen piece can move,
                if so it execute that move

            Parameters:
                x (int): horizontal coordinate of clicked square
                y (int): vertical coordinate of clicked square

            Returns:
                Bool: True if square that player clicked on is square on which chosen piece can move, False if not

        """
        

        for move in self.chosen_piece.moves:
            if y == move.y and x == move.x:

                if move.type == None:
                    self.play_sound(Game.move_sound)
                    self.moves_no_take += 1

                    self.move_piece(y, x, self.chosen_piece)

                elif move.type == 'takes':
                    self.play_sound(Game.take_sound)
                    self.moves_no_take = 0

                    self.take_piece(y, x) #take piece
                    self.move_piece(y, x, self.chosen_piece)

                elif move.type == 'castle':
                    self.play_sound(Game.move_sound)
                    self.moves_no_take += 1

                    if move.castle_way == 'short':
                        self.castle_short(y, 6)
                        
                    elif move.castle_way == 'long':
                        self.castle_long(y, 2)
                        

                elif move.type == 'en_passant':
                    self.play_sound(Game.take_sound)
                    self.moves_no_take = 0

                    self.take_piece(self.chosen_piece.y, x)
                    self.move_piece(y, x, self.chosen_piece)
                

                return True

        
        return False #return false if clicked somewhere else then possible move

    def change_turn(self):
        
        """
            Description:
                Changes turn to the opposite
        """

        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'

    def move_piece(self, y, x, piece_to_move):
        
        """
            Description:
                Changes places of piece in the board
                Initiate move_piece for the piece (changing coordinates)
                Decects if promotion occurs and iniciate it
                If moved piece is Rook or King assings on which move it was moved (declaining castle rights)


            Parameters:
                piece_to_move (piece): piece that designated to move
                x (int): piece will move to this cooridante
                y (int): piece will move to this cooridante

        """
        
        self.board[y][x], self.board[piece_to_move.y][piece_to_move.x] = piece_to_move, None
        

        if isinstance(piece_to_move, Pawn):
            self.moves_no_take = 0

            if (    #promotion
                    (y == 0 and piece_to_move.color == 'white') or 
                    (y == 7 and piece_to_move.color == 'black')
                ):
                self.board[y][x].move_piece(y, x, self.board)

                for i in range(len(self.pieces[piece_to_move.color])):
                    if self.pieces[piece_to_move.color][i] == piece_to_move:
                        self.pieces[piece_to_move.color][i] = self.board[y][x]

                return

        elif isinstance(piece_to_move, (King, Rook)) and piece_to_move.is_moved_on_move == None:
            piece_to_move.is_moved_on_move = self.c_board_nr

        self.board[y][x].move_piece(y, x)



    def take_piece(self, y, x):
        """
            Description:
                Removes taken piece
                Resets moves without taking counter


            Parameters:
                piece_to_move (piece): piece that designated to move
                x (int): horizontal cooridante of piece that will be removed
                y (int): vertical cooridante of piece that will be removed


        """
        self.pieces[self.board[y][x].color].remove(self.board[y][x])
        self.board[y][x].undraw_piece()
        self.board[y][x] = None

        

    def castle_short(self, y, x):
        """
            Description:
                Move piece of short castling

            Parameters:
                x (int): horizontal cooridante of the king
                y (int): vertical cooridante of the king
        """
        self.move_piece(y, x, self.chosen_piece) #move king
        self.move_piece(y, 5, self.board[y][7]) #move rook

    def castle_long(self, y, x):
        """
            Description:
                Move piece of long castling

            Parameters:
                x (int): horizontal cooridante of the king
                y (int): vertical cooridante of the king
        """
        self.move_piece(y, x, self.chosen_piece) #move king
        self.move_piece(y, 3, self.board[y][0]) #move rook
        

    def wait_for_input(self):
        """
            Description:
                Waits for mouse input
                Acts accordingly to input
        """
       
        self.find_all_moves()
    

        while True:

            try:
                clickPoint = self.win.checkMouse()
            except:
                return #window was closed, program will shout down
                
            if clickPoint != None:

                self.undraw_moves()
                

                if clickPoint.x in range(800) and self.eg_window == None and self.nextButton.is_active == False:

                    y = self.px_to_index(clickPoint.y)
                    x = self.px_to_index(clickPoint.x)   
                                        # jezeli gra sie nie skoczyla to patrzy na plansze ###

                    if self.chosen_piece != None and self.make_move(x, y):
                        # if clicked on possible move square
                        self.c_board_nr += 1
                        self.mega_board.append(self.deepcopy(self.board))
                        

                        self.chosen_piece = None
                        self.change_turn()
                        self.find_all_moves()
                        self.refresh_buttons()

                    elif self.chosen_piece != None and self.chosen_piece.y == y and self.chosen_piece.x == x:
                        # if clicked on chosen piece
                        self.chosen_piece = None

                    elif self.board[y][x] != None and self.board[y][x].color == self.turn:     # jezeli next button nie jest aktywny to rysuje ruchy, jak jest aktywny to nie rysuje ###
                        self.play_sound(Game.choise_sound)
                        
                        # if clicked on right turn color piece
                        self.chosen_piece = self.board[y][x]
                        self.draw_chosen_piece_moves()

                    elif self.board[y][x] != None and self.board[y][x].color != self.turn:
                        self.play_sound(Game.error_sound)
                        # if clicked on wrong turn color piece
                        self.chosen_piece = None
                        
                    else:
                        self.chosen_piece = None

                elif clickPoint.x in range(800,1000):  # patrzy na przyciski niezaleznie od konca gry, nie bierze pod uwage self.endgame I TYLE
                    # if clicked on menu
                    self.chosen_piece=None
                    if ( self.prevButton.clicked(clickPoint.x, clickPoint.y) ):  
                        self.draw_chosen_board(self.c_board_nr - 1)

                    elif (  self.nextButton.clicked(clickPoint.x, clickPoint.y) ):
                        self.draw_chosen_board(self.c_board_nr + 1)
                    
                    elif ( self.RestorePosition.clicked(clickPoint.x, clickPoint.y) ):
                        self.play_sound(Game.restore_sound)
                        self.restore(self.c_board_nr)
                        
                    elif ( self.NewGameButton.clicked(clickPoint.x, clickPoint.y) ):
                        self.play_sound(Game.restore_sound)
                        self.restore(0)
                        

                else:
                    self.chosen_piece = None


                
            sleep(0.1)

    def restore(self, board_nr):
        """
            Description:
                Restores board of given number

            Parameters:
                board_nr (int): number of the board to be restored
        """
        
        if self.eg_window != None:
            self.eg_window.close()
            self.eg_window = None
        

        interval = 1.4 / (len(self.pieces['white']) + len(self.pieces['black']))

        for y in range(8): # undraw pieces
            for x in range(8):
                if self.mega_board[self.c_board_nr][y][x] != None:
                    self.mega_board[self.c_board_nr][y][x].undraw_piece()
                    sleep(interval)
                    
        self.board = self.deepcopy(self.mega_board[board_nr])

        if board_nr % 2:
            self.turn = 'black'
        else:
            self.turn = 'white'

        self.lp_reps = [nr for nr in self.lp_reps if nr <= board_nr]

        for i in range(len(self.mega_board) - 1, board_nr, -1):
            del self.mega_board[i]

        
        self.pieces['white'] = [self.pieces['white'][0]]
        self.pieces['black'] = [self.pieces['black'][0]]



        for y in range(8): # refresh pieces coordinates
            for x in range(8):
                if self.board[y][x] != None:

                    if not isinstance(self.board[y][x], King):
                        self.pieces[self.board[y][x].color].append(self.board[y][x])

                    self.board[y][x].y = y
                    self.board[y][x].x = x

                    if (
                            isinstance(self.board[y][x], (King, Rook)) and
                            self.board[y][x].is_moved_on_move != None and
                            self.board[y][x].is_moved_on_move >= board_nr
                        ):
                        self.board[y][x].is_moved_on_move = None    #restore castle rights
        
        for y in range(8):
            for x in range(8):
                if self.board[y][x] != None:
                    self.board[y][x].draw_piece()
                    sleep(interval)

        self.c_board_nr = board_nr


        self.refresh_buttons()
        self.find_all_moves()
        
        
    def px_to_index(self, value):
        """
            Parameters:
                value (int, float): value in pixels

            Returns:
                int: value of index containing given pixel value
        """

        return int(value // 100)

    def undraw_moves(self):
        if self.chosen_piece != None:
            for move in self.chosen_piece.moves:
                move.undraw_move()

    def insufficient_material(self):
        """
            Returns:
                Bool: True if there is insufficient material on the board to win, False if not
        """
        for color in ['white','black']:

            c = 0
            for piece in self.pieces[color]:

                if isinstance(piece, Pawn):
                    return False

                elif isinstance(piece, (Bishop, Knight)):
                    c += 1

                if c == 2:
                    return False
        

        return True


    def fifty_moves_rule(self):
        """
            Returns:
                Bool: True if there was 50 moves without taking or moving pawn in row, False if not
        """
        if self.moves_no_take == 100:
            return True
        else:
            return False

    def endgame_window(self, text, draw):

        """
            Description:
                Pops up the endgame window

            Parameters:
                text (str): text that will be displayed in endgame window
                draw (bool): True if game ended in a draw
        """
        
        self.play_sound(Game.end_sound)

        if draw:
            text += "\n draw"

            img1_url = King.white_img_url
            img2_url = King.black_img_url

        else:
            if self.turn == 'black':
                text += "\n white wins!"

                img1_url = King.white_img_url
                img2_url = Queen.white_img_url

            else:
                text += "\n black wins!"

                img1_url = King.black_img_url
                img2_url = Queen.black_img_url

        x = 300
        y = 150

        self.eg_window = GraphWin("END OF GAME!", x, y)
        self.eg_window.setBackground(Game.buttons_color)

        img1 = Image(Point(x-50, y/2), img1_url)
        img1.draw(self.eg_window)

        img2 = Image(Point(x-240, y/2), img2_url)
        img2.draw(self.eg_window)

        txt = Text(Point(x/2, y/2), text)
        txt.setFace("courier")        
        txt.draw(self.eg_window)



    def threefold_repetition(self):
        """
            Returns:
                Bool: True if there is the position was repeted 3 times, False if not
        """

        def compare_boards(i):
            """
                Parameters:
                    i (int): number of board that will be compared to current
                Returns:
                    Bool: True if the compared boards were the same, False if not
                    Kill (str): if spotted a board state that cannot be repeated
            """
            
            for y in range(8):
                for x in range(8):
                    if self.board[y][x] != self.mega_board[i][y][x]:
                        if (
                                (self.board[y][x] == None and isinstance(self.mega_board[i][y][x], Pawn)) or 
                                (isinstance(self.board[y][x], Pawn) and self.mega_board[i][y][x] == None) or 
                                (self.board[y][x] != None and self.mega_board[i][y][x] != None)
                            ):  
                            return "KILL"
                        else:
                            return False
            return True

        i = len(self.mega_board) - 2
        r = 1

        while i >= self.lp_reps[-1]:
            var = compare_boards(i)

            if var == True:
                r += 1

            elif var == "KILL":
                if self.lp_reps[-1] != i:
                    self.lp_reps.append(i)
                return False

            if r == 3: 
                return True

            i -= 1

        return False


    def deepcopy(self, board):
        """
            Parameters:
                board (list): board that will be deepcopied
            Returns:
                list: deepcopied board
        """

        return [[board[y][x] for x in range(8)] for y in range (8)]

    def mege_print(self, board): 
        
        string = ""
        for y in range(8):
            for x in range(8):
                string += str(board[y][x].__str__()) + "\t"
            
            string+="\n"
        return string


    def __str__(self):
        string = ""
        for y in range(8):
            for x in range(8):
                string += str(self.board[y][x].__str__()) + "\t"
            
            string+="\n"
        return string






