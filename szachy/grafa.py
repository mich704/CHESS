from graphics import *
from time import sleep
from game import Game
from pieces import *




def main(): 

    #initiate game
    g1 = Game()
    g1.draw_board()
    g1.draw_menu()
    g1.set_starting_position()
    g1.draw_pieces()
    g1.wait_for_input()

    
if  __name__ == '__main__':
    main()