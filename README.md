#Noughts and Crosses
By Wesley Thompson


##Description
*With this game of Noughts and Crosses (AKA Tic Tac Toe) you can play against the computer with the option of two different difficulty modes, 'Easy' or 'Impossible'.
*Using the impossible difficulty setting the computer plays a perfect game and can't be beaten, only tied with.
*You can choose from the start menu if you or the computer takes the first turn.

##How to Use
1 Clone the noughts-and-crosses git repository.
2 Run the run_game.pyw file using python interpreter (3.0 or later).
3 At the start menu select the difficulty mode and whether you would like to take the first turn, then click OK.
4 Click on tiles to place a 'X' or 'O'.
5 If Impossible difficulty mode is selected the calculation depth of the algorithm can be adjusted using buttons at the top of the board. Reducing the calculation depth reduces how many moves ahead the computer is able to look.
6 When in Impossible mode, red text will will appear above the board when loosing is inevitable and will inform you of the maximum number of moves remaining before the computer wins.

##Prerequisites
*Python 3.0 or later is required to run Noughts and Crosses

##Implementation
*Python 3 was used to create this game of Noughts and Crosses
*The recursive Minimax algorithm was implemented to enable the computer to play a perfect game.
*The Tkinter toolkit for Python was implemented to provide the graphical user interface.