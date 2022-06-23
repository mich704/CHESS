from graphics import *
from math import log
from time import sleep
from move import Move


class Piece():
    """
        Description:
            abstract class, whre from every piece class inherits

        Args:
            promotion_bg_color (str): color specifier string for backgroud of poromition window

            color (str): color of the piece 'black' or 'white'
            img_url (str): path to piece png file
            y (int): vertical coordinate of piece
            x (int): horizontal coordinate of piece
            win (GraphWin): window in which game is displayed

    """

    promotion_bg_color = color_rgb(244, 181, 252)

    def __init__(self, color, y, x, win):
        self.color = color
        self.img_url = ""
        self.y = y
        self.x = x
        self.img = None
        self.win = win

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        """
        Description:
            sets value of color
        """
        if color == 'white':
            self._color = 'white'
        elif color == 'black':
            self._color = 'black'
        else:
            raise ValueError("Color must be black or white")

    def draw_piece(self, y = None, x = None):
        """
        Description:
            undraws piece using draw() method from graphics.py

        Parameters:
            y (int): vertical coordinate of piece
            x (int): horizontal coordinate of piece
        Raises:
            ValueError when image is already drawn

        
        """
        if y is None and x is None:
            y = self.y
            x = self.x

        if self.img == None:
            self.img = Image(Point(x * 100 + 52, y * 100 + 50), self.img_url)
            self.img.draw(self.win)
        else:
            raise ValueError("Image is already drawn, try move_piece")
        
    def undraw_piece(self):
        """
        Description:
            undraws piece using undraw() method from graphics.py 

        Raises:
            ValueError when there is no image to undraw

        
        """
        if self.img != None:
            self.img.undraw()
            self.img = None
        else:
            raise ValueError("There is no image to undraw")

    def move_piece(self, y, x):
        """
        Description:
            moves piece img using move() method, changes actual coordinates 

        Parameters:
            y (int): vertical coordinate of where piece should be moved
            x (int): horizontal coordinate of piece should be moved

        """

        self.img.move((x * 100 + 50) - (self.x * 100 + 50),(y * 100 + 50) - (self.y * 100 + 50))
        
        self.x = x
        self.y = y
        

    def check_moves_king_safety(self, moves, board):
        """
        Description:
           returns all moves after which king is safe

        Parameters:
            moves (list): consisting of coordinates of piece possible moves
            board (list): stores all pieces in appropiate fields

        """
        return [move for move in moves if (move.type == "castle" or self.king_safe(move.y, move.x, board))]
        
    def king_safe(self, m_y, m_x, board):
        """
        Description:
            checks if after given move the king cannot be taken 

        Parameters:
            m_y (int): vertical coordinate after move is done
            m_x (int): horizontal coordinate after move is done
            board (list): stores all pieces in appropiate fields

        Returns:
            True if after given move the king cannot be taken
            False if after given move the king can be taken

        """

        #make hypotetical move
        field_value = board[m_y][m_x]
        board[self.y][self.x] = None
        board[m_y][m_x] = self

        def undo(): # undo hypotetical move
            board[m_y][m_x] = field_value
            board[self.y][self.x] = self


        for y in range(8):
            for x in range(8):
                if board[y][x] != None and board[y][x].color != self.color:

                    if isinstance(board[y][x], Pawn):
                        for move in board[y][x].take_diagonal(board):
                            if isinstance(board[move.y][move.x], King):
                                undo()
                                return False

                    elif isinstance(board[y][x], King):
                        for move in board[y][x].king_moves(board):
                            if isinstance(board[move.y][move.x], King):
                                undo()
                                return False

                    elif board[y][x] != None:
                        for move in board[y][x].all_moves(board, False):
                            if isinstance(board[move.y][move.x], King):
                                undo()
                                return False

        undo()
        return True


    





class Pawn(Piece):
    """
        Description:
            stores properities of Pawn, inherits form Piece class

        Args:
            white_img_url (str): path to white Pawn png
            black_img_url (str): path to black Pawn png

    """

    white_img_url = 'pieces/w_pawn_png_shadow_128px.png'
    black_img_url = 'pieces/b_pawn_png_shadow_128px.png'

    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)
        
        if self.color == 'white':
            self.img_url = Pawn.white_img_url
        elif self.color == 'black':
            self.img_url = Pawn.black_img_url
                

    def move_piece(self, y, x, board = None):
        """
        Description:
            moves piece img using move() method, changes actual coordinates
            and checks if current move is leading to promotion

        Parameters:
            y (int): vertical coordinate of where piece should be moved
            x (int): horizontal coordinate of piece should be moved

        """

        self.img.move((x * 100 + 50) - (self.x * 100 + 50),(y * 100 + 50) - (self.y * 100 + 50))

        self.x = x
        self.y = y

        if board != None:
            self.promotion(board)



    def all_moves(self, board, prev_board = None, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that Pawn object can make

        Parameters:
            board (list): stores all pieces in appropiate fields
            prev_board (list): previous state of board (list)
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []
        moves += self.move_forward(board) + self.take_diagonal(board)

        if prev_board != None:
            moves += self.en_passant(board, prev_board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)

        return moves
        

    def move_forward(self, board):
        """
        Description:
            Returns list of all possible moves that Pawn object can make in vertical direction

        Parameters:
            board (list): stores all pieces in appropiate fields

        Returns 
            (list): all possible moves that Pawn object can make in vertical direction
        
            
        """

        if self.color == 'white':

            if board[self.y - 1][self.x] == None:
                if self.y == 6 and board[self.y - 2][self.x] == None:
                    return [Move(self.y - 1, self.x, self.win), Move(self.y - 2, self.x, self.win)]

                else:
                    return [Move(self.y - 1,self.x, self.win)]
                
            else:
                return []
                

        elif self.color == 'black':

            if board[self.y + 1][self.x] == None:
                if self.y == 1 and board[self.y + 2][self.x] == None:
                    return [Move(self.y + 1, self.x, self.win), Move(self.y + 2, self.x, self.win)]
                else:
                    return [Move(self.y + 1,self.x, self.win)]
                
            else:
                return []



    def take_diagonal(self, board):
        """
        Description:
            Returns list of all possible take moves of Pawn 

        Parameters:
            board (list): stores all pieces in appropiate fields

        Returns 
            moves (list): all possible moves that Pawn object can make in diagonal direction
        
            
        """
        if self.color == 'white':
            moves = []


            if (
                    self.x < 7 and board[self.y - 1][self.x + 1] != None and
                    board[self.y - 1][self.x + 1].color == 'black'
                ):  
                    moves.append(Move(self.y - 1, self.x + 1, self.win, 'takes')) 
            if (
                    self.x > 0 and board[self.y - 1][self.x - 1] != None and
                    board[self.y - 1][self.x - 1].color == 'black'
                ):
                    moves.append(Move(self.y - 1, self.x - 1, self.win, 'takes'))
                

        elif self.color == 'black':
            moves = []
            
            if (
                    self.x < 7 and board[self.y + 1][self.x + 1] != None and
                    board[self.y + 1][self.x + 1].color == 'white'
                ):
                moves.append(Move(self.y + 1, self.x + 1, self.win, 'takes'))
            
            if (
                    self.x > 0 and board[self.y + 1][self.x - 1] != None and
                    board[self.y + 1][self.x - 1].color == 'white'
                ):
                moves.append(Move(self.y + 1, self.x - 1, self.win, 'takes'))
                
        return moves
    
    def en_passant(self, board, prev_board):
        """

        Parameters:
            board (list): stores all pieces in appropiate fields
            prev_board (list): previous state of board (list)

        Returns 
            moves (list): field where Pawn object can be after en passant move
        
            
        """

        moves=[]

        if self.color == 'white' and self.y == 3:
            for i in range(-1, 2):
                if i == 0: continue

                if(
                    self.x + i in range(0, 8) and
                    isinstance(board[self.y][self.x + i], Pawn) and
                    board[self.y][self.x + i].color != self.color and 
                    isinstance(prev_board[1][self.x + i], Pawn) and
                    prev_board[1][self.x +i].color != self.color 
                ):
                    moves.append(Move(self.y-1, self.x+i, self.win, 'en_passant'))
                    break

        elif self.color == 'black' and self.y == 4:
            for i in range(-1, 2):
                if i==0: continue

                if(
                    self.x + i in range(0,8) and
                    isinstance(board[self.y][self.x + i], Pawn) and
                    board[self.y][self.x + i].color != self.color and 
                    isinstance(prev_board[6][self.x + i], Pawn) and
                    prev_board[6][self.x + i].color != self.color
                ): 
                    moves.append(Move(self.y + 1, self.x + i, self.win, 'en_passant'))
                    break
                
            

        return moves


    def promotion(self, board):
        """
        Parameters:
            board (list): stores all pieces in appropiate fields

        Returns 
            moves (list): field where Pawn object can be after promotion move
        
            
        """

        y = self.y
        x = self.x
        color = self.color
        win = self.win

        x_mid_px = (round(log(x + 2, 1.5), 1) + 0.5) * 100

        if self.color == 'white':
            y_mid_px = 75

        elif self.color == 'black':
            y_mid_px = 725

        size_x = 400
        size_y = 100

        start_x = x_mid_px - (size_x/2)

        #draw pop up window
        bg_rectangle = Rectangle(
            Point(x_mid_px - size_x/2, y_mid_px - size_y/2),
            Point(x_mid_px + size_x/2, y_mid_px + size_y/2))
        bg_rectangle.setFill(Piece.promotion_bg_color)
        bg_rectangle.setWidth(3)
        bg_rectangle.draw(win)
        
        prom_pieces = [Knight, Bishop, Rook, Queen]

        #draw and add pieces to prom_pieces_img
        for i in range(4):
            prom_pieces[i] = prom_pieces[i](color, (y_mid_px - 50) / 100, (start_x + (i * 100)) / 100, win)
            prom_pieces[i].draw_piece()

        
        def chosen_piece():
            """
            Description:
                Waits for input (which piece user chose)

            Returns:
                (class): chosen piece type 
            """
            
            while True: #wait for input
                clickPoint = self.win.checkMouse()
                if (
                        clickPoint != None and
                        int(clickPoint.y) in range(int(y_mid_px - size_y/2), int(y_mid_px + size_y/2))
                    ):  
                    for i in range(4):
                        if int(clickPoint.x) in range(int(start_x) + (i * 100), int(start_x) + (i * 100) + 100):
                            return type(prom_pieces[i])

                sleep(0.1)

        self.undraw_piece()
        board[y][x] = chosen_piece()(color, y, x, win)

        #undraw pop up window and pieces
        for i in range(4):
            prom_pieces[i].undraw_piece()
        bg_rectangle.undraw()
        
        board[y][x].draw_piece()





    def __str__(self):
        return self.color[0] + "P"








class Knight(Piece):
    """
        Description:
            stores properities of Knight, inherits form Piece class

        Args:
            white_img_url (str): path to white Knight png
            black_img_url (str): path to black Knight png

    """


    white_img_url = 'pieces/w_knight_png_shadow_128px.png'
    black_img_url = 'pieces/b_knight_png_shadow_128px.png'

    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)
        
        if self.color == 'white':
            self.img_url = Knight.white_img_url
        elif self.color == 'black':
            self.img_url = Knight.black_img_url
    

    def all_moves(self, board, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that Knight object can make 
            and changes list if king is not safe

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []
        moves+=self.knight_moves(board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)

        return moves


    def knight_moves(self,board):
        """
        Description:
            Creates list of all possible moves that Knight object can make 

        Parameters:
            board (list): stores all pieces in appropiate fields

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves=[]

        for y in range(-2,3):
            for x in range(-2,3):
                if(
                    y and x and abs(y) != abs(x) and
                    self.y + y in range(8) and self.x + x in range(8)
                ):
                    if board[self.y + y][self.x + x] == None:
                        moves.append(Move(self.y +y ,self.x +x, self.win))

                    elif board[self.y + y][self.x + x].color != self.color:
                        moves.append(Move(self.y +y ,self.x +x, self.win, 'takes'))

        return moves
    


    def __str__(self):
        return self.color[0] + "N"









class Rook(Piece):
    """
        Description:
            stores properities of Rook, inherits form Piece class

        Args:
            white_img_url (str): path to white Rook png
            black_img_url (str): path to black Rook png

    """


    white_img_url = 'pieces/w_rook_png_shadow_128px.png'
    black_img_url = 'pieces/b_rook_png_shadow_128px.png'

    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)

        self.is_moved_on_move = None
        
        if self.color == 'white':
            self.img_url = Rook.white_img_url
        elif self.color == 'black':
            self.img_url = Rook.black_img_url

      

    def all_moves(self, board, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that Rook object can make 
            and changes list if king is not safe

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []
        moves+=self.rook_moves(board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)

       
        return moves

    def rook_moves(self,board):
        """
        Description:
            Creates list of all possible moves that Rook object can make 

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """

        moves = []

        for d in range(2):
            for sense in range(-1,2):
                if sense == 0: continue

                i = 1
                while True:
                    if d == 0:
                        x = self.x
                        y = self.y + (i * sense)
                    elif d == 1:
                        x = self.x + (i * sense)
                        y = self.y 
                    
                    if x not in range(8) or y not in range(8):
                        break

                    if board[y][x] == None:
                        moves.append(Move(y, x, self.win))

                    elif board[y][x].color != self.color:
                        moves.append(Move(y, x, self.win, 'takes'))
                        break

                    else:
                        break

                    i += 1
        return moves

    def __str__(self):
        return self.color[0] + "R"









class Bishop(Piece):
    """
        Description:
            stores properities of Bishop, inherits form Piece class

        Args:
            white_img_url (str): path to white Bishop png
            black_img_url (str): path to black Bishop png

    """

    

    white_img_url = 'pieces/w_bishop_png_shadow_128px.png'
    black_img_url = 'pieces/b_bishop_png_shadow_128px.png'

    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)
        
        if self.color == 'white':
            self.img_url = Bishop.white_img_url
        elif self.color == 'black':
            self.img_url = Bishop.black_img_url

      

    def all_moves(self, board, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that Bishop object can make 
            and changes list if king is not safe

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []
        moves+=self.bishop_moves(board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)
            
        return moves

       

    def bishop_moves(self,board):
        """
        Description:
            Creates list of all possible moves that Bishop object can make 

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """

        moves = []

        for d in range(4):

            i = 1
            while True:
                if d == 0: 
                    x = self.x + i
                    y = self.y - i
                elif d == 1:
                    x = self.x - i
                    y = self.y + i
                elif d == 2:
                    x = self.x + i
                    y = self.y + i
                elif d == 3:
                    x = self.x - i
                    y = self.y - i
                

                if x not in range(8) or y not in range(8):
                    break


                if board[y][x] == None:
                    moves.append(Move(y, x, self.win))

                elif board[y][x].color != self.color:
                    moves.append(Move(y, x, self.win, 'takes'))
                    break

                else:
                    break

                i += 1
        return moves

    def __str__(self):
        return self.color[0] + "B"







class Queen(Bishop, Rook):
    """
        Description:
            stores properities of Queen, inherits form Bishop and Rook class

        Args:
            white_img_url (str): path to white Queen png
            black_img_url (str): path to black Queen png

    """


    white_img_url = 'pieces/w_queen_png_shadow_128px.png'
    black_img_url = 'pieces/b_queen_png_shadow_128px.png'

    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)
        
        if self.color == 'white':
            self.img_url = Queen.white_img_url
        elif self.color == 'black':
            self.img_url = Queen.black_img_url


    def all_moves(self, board, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that Queen object can make 
            and changes list if king is not safe

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
            all Bishop moves + all Rook moves
        
            
        """
        moves = []
        moves += Bishop.bishop_moves(self,board) + Rook.rook_moves(self,board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)
       
        return moves

    def __str__(self):
        return self.color[0] + "Q"






class King(Piece):
    """
        Description:
            stores properities of King, inherits form Piece class

        Args:
            white_img_url (str): path to white King png
            black_img_url (str): path to black King png

    """

    white_img_url = 'pieces/w_king_png_shadow_128px.png'
    black_img_url = 'pieces/b_king_png_shadow_128px.png'
    
    def __init__(self, color, y, x, win):
        super().__init__(color, y, x, win)

        self.is_moved_on_move = None  # when king was moved, variabe used in castle methods
        
        if self.color == 'white':
            self.img_url = King.white_img_url
        elif self.color == 'black':
            self.img_url = King.black_img_url


    def all_moves(self, board, check_king_safety = True):
        """
        Description:
            Creates list of all possible moves that King object can make 
            and changes list if king is not safe

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []
        moves += self.king_moves(board) + self.castle_short(board) + self.castle_long(board)

        if check_king_safety:
            moves = self.check_moves_king_safety(moves, board)

        return moves


    def king_moves(self,board):
        """
        Description:
            Creates list of all possible moves that King object can make 

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move
        
            
        """
        moves = []

        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if (
                        not(y == self.y and x == self.x) and
                        y in range(8) and x in range(8)
                    ):
                    if board[y][x] == None:
                        moves.append(Move(y, x, self.win))
                        

                    elif board[y][x].color != self.color:
                        moves.append(Move(y, x, self.win, 'takes'))


        return moves



    def castle_long(self, board):
        """

        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move after castle_long move
        
            
        """
        if (
                self.is_moved_on_move == None and
                isinstance(board[self.y][0], Rook) and
                board[self.y][0].is_moved_on_move == None
            ):
            for x in range(1,4):
                if (
                        board[self.y][x] != None or
                        not self.king_safe(self.y, x, board)
                    ):
                    return []

            if not self.king_safe(self.y, self.x, board):
                return []

            return [Move(self.y, 2, self.win, 'castle', 'long'), Move(self.y, 0, self.win, 'castle', 'long')]

        else:
            return []

    def castle_short(self, board):
        """
        
        Parameters:
            board (list): stores all pieces in appropiate fields
            check_king_safety (bool): information about king safety

        Returns 
            moves (list): stores coordinates of all possible fields where object can move after castle_short move
        
            
        """
        if (
                self.is_moved_on_move == None and
                isinstance(board[self.y][7], Rook) and
                board[self.y][7].is_moved_on_move == None
            ):
            for x in range(5,7):
                if (
                        board[self.y][x] != None or 
                        not self.king_safe(self.y, x, board)
                    ):
                    return []

            if not self.king_safe(self.y, self.x, board):
                return []

            return [Move(self.y, 6, self.win, 'castle', 'short'), Move(self.y, 7, self.win, 'castle', 'short')]
            
        else:
            return []


    def __str__(self):
        return self.color[0] + "K"
    