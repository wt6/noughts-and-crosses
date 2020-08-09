from tkinter import *
import tkinter.messagebox as tk_msgbox
import tkinter.font as tkfont

from lib.game import Game


class NoughtsAndCrossesApp(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold')

        self.starting_player = None
        self.mode = None

        #container of frames
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuScreen, GameScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.configure(background = 'white')
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[page_name] = frame

        self.show_frame('MenuScreen')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == 'GameScreen':
            self.frames['GameScreen'].new_game()

    def game_over(self, winner):
        if winner == 1:
            tk_msgbox.showinfo("Congratulations!", "Well done. You won!")
        elif winner == 2:
            tk_msgbox.showinfo("Sorry!", "Sorry. You lost!")
        else:
            tk_msgbox.showinfo("Draw", "It's a draw")

        self.play_again = tk_msgbox.askquestion('Play Again?', 'would you like to play again?')

        if self.play_again == 'yes':
            self.show_frame('MenuScreen')
            self.frames['GameScreen'].frame1.destroy()
        else:
            self.destroy()


class MenuScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Noughts and Crosses - Menu")

        self.mode = StringVar()
        self.mode.set('easy')
        self.starting_player = IntVar()
        self.starting_player.set(0)

        frame1 = Frame(bg='white')
        frame1.place(in_=self, anchor='c', relx=.5, rely=.5)

        label_welcome = Label(frame1, text="Welcome to Noughts and Crosses", bg='white', font=self.controller.title_font)
        label_welcome.grid(columnspan=3, row=0, sticky='n')
        
        label_choose_mode = Label(frame1, text="\n\n\nSelect difficulty mode:", bg='white')
        mode_option1 = Radiobutton(frame1, text="Easy", variable=self.mode, value='easy', bg='white')
        mode_option2 = Radiobutton(frame1, text="Impossible", variable=self.mode, value='impossible', bg='white')
        label_choose_mode.grid(column=0, row=2, sticky='w')
        mode_option1.grid(column=0, row=3, sticky='w')
        mode_option2.grid(column=0, row=4, sticky='w')


        label_starting_player = Label(frame1, text="\n\n\nSelect who you would you like to go first:", bg='white')
        start_option1 = Radiobutton(frame1, text="Human", variable=self.starting_player, value=0, bg='white')
        start_option2 = Radiobutton(frame1, text="Computer", variable=self.starting_player, value=1, bg='white')
        label_starting_player.grid(columnspan=2, column=0, row=5, sticky='w')
        start_option1.grid(column=0, row=6, sticky='w')
        start_option2.grid(column=0, row=7, sticky='w')

        button_ok = Button(frame1, text="OK", width=5, command=self.ok_button, bg='white')
        button_quit = Button(frame1, text="EXIT", width=5, command=self.exit_button, bg='white')
        button_ok.grid(column=0, row=8, sticky='e', pady=40)
        button_quit.grid(column=1, row=8, sticky='w', padx=10)

    def ok_button(self):
        self.controller.mode = self.mode.get()
        self.controller.starting_player = self.starting_player.get()
        self.controller.show_frame('GameScreen')

    def exit_button(self):
        self.controller.exit_game = True
        self.controller.destroy()


class GameScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=500, bg='white')

        self.blank_image = PhotoImage(file='data/blank.png')
        self.nought_image = PhotoImage(file='data/nought.png')
        self.cross_image = PhotoImage(file='data/cross.png')

        self.depth = 9

    def new_game(self):
        self.starting_player = self.controller.starting_player
        self.game = Game(self.controller.mode)
        
        self.controller.title("Noughts and Crosses - Mode: " + self.controller.mode.capitalize())
       
        self.frame1 = Frame(width=300, height=300, bg='white')
        self.frame1.place(in_=self, anchor='c', relx=.5, rely=.5)

        if self.controller.mode == 'impossible':
            self.frame2 = Frame(self.frame1, width=300, height=100, bg='white')
            self.frame2.grid(columnspan=4, row=0)
            
            self.depth_label = Label(self.frame2, text="Calculation Depth: %d" %self.depth, bg='white')
            button_dec = Button(self.frame2, text="<", bg='white', width=1, height=1, command=self.dec_button)
            button_inc = Button(self.frame2, text=">", bg='white', width=1, height=1, command=self.inc_button)
            self.depth_label.grid(column=0, row=0)
            button_dec.grid(column=1, row=0)
            button_inc.grid(column=2, row=0)
            
            self.moves_until_win = Label(self.frame2, fg='red', bg='white', padx=5, font=("Courier", 13))
            self.moves_until_win.grid(column=3, row=0)

        self.buttons = [Button(self.frame1, image=self.blank_image, width=150,
                                  height=150, command=lambda button=i:
                                  self.button_click(button), bg='white') for i in range(9)]

        if self.starting_player == 0:
            self.player_image = self.cross_image
            self.opponent_image = self.nought_image
        else:
            self.player_image = self.nought_image
            self.opponent_image = self.cross_image

        but = 0
        for row in range(1,4):
            for col in range(3):
                self.buttons[but].grid(column=col, row=row)
                but += 1

        if self.controller.starting_player == 1:
            self.game.update(None)
            self.update()

    def inc_button(self):
        if self.depth < 9:
            self.depth += 1
            self.depth_label.config(text="Calculation Depth: %d" %self.depth)

    def dec_button(self):
        if self.depth > 1:
            self.depth -= 1
            self.depth_label.config(text="Calculation Depth: %d" %self.depth)
                
    def button_click(self, button):      
        self.buttons[button].config(image=self.player_image, state='disabled')
        self.move = button
        if self.controller.mode == 'impossible':
            self.game.players[1].minimax.set_depth(self.depth)
        self.game.update(self.move)
        self.update()
        
    def update(self):
        if self.controller.mode == 'impossible':
            moves = self.game.players[1].moves_until_win
            if moves:
                if moves == 1:
                    self.moves_until_win.config(text="You will lose in 1 move!")
                elif moves >= 2:
                    self.moves_until_win.config(text="You will lose within %d moves!" %moves)

        if self.game.move_no > 1:
            button = self.game.players[1].moves[-1]
            self.buttons[button].config(image=self.opponent_image, state='disabled')

        if not self.game.winner == None:
            self.controller.game_over(self.game.winner)

