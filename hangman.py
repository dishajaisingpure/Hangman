import tkinter as tk
import random
import re
import words_dictionary as v

"""Initializing the global variable here.
hint_word = This variable stores the hint of the word to be guessed by the player
word = It stores the word to be guessed by the player
win_score = It holds the number of games won by the player
total_score = This variable holds the total games played 
hangman_canvas = This variable holds the canvas where the hangman is displayed
word_canvas = This variable holds the canvas where the word along with other elements is displayed
word_letters_lbl = This variable holds the label which displays the number of letter in a word 
hint_lbl = It holds the label which displays the hint
score_lbl = This variable holds the label which displays the score of the player to the total games played
next_word_btn = It holds the label which displays the 
coordinate_list = It holds the coordinates list required to print the dash lines on the screen
all_images = It holds the image list which is required to display the hangman
display_hangman_coordinates =  It holds the coordinates list which is required to display the hangman
"""

hint_word = random.choice(list(v.word_dict.keys()))
word = random.choice(v.word_dict[hint_word]).lower()
win_score = total_score = 0
hangman_canvas = word_canvas = ""
word_letters_lbl = hint_lbl = score_lbl = next_word_btn = ""
coordinate_list = all_images = display_hangman_coordinates = []


class MainFrame(tk.Tk):

    """This class acts like the main class.
    This class creates a main frame that holds all the sub components, creates the sub components, and also takes care
    of displaying all the components """

    def __init__(self, *args, **kwargs):

        """This method is called as soon as MainFrame object is created.
        It holds all the necessary parameters, class variables required for the MainFrame class execution."""

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame2 = ThirdFrame(self.container, self)
        self.frames[ThirdFrame] = frame2
        frame2.grid(row=1, column=0, sticky='e')

        frame1 = SecondFrame(self.container, self)
        self.frames[SecondFrame] = frame1
        frame1.grid(row=1, column=0, sticky="w")

        frame = FirstFrame(self.container, self)
        self.frames[FirstFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_propagate(0)

        self.show_frames(FirstFrame)
        # self.show_frames(SecondFrame)
        self.show_frames(ThirdFrame)

    def show_frames(self, cont):

        """This method is used to display the 3 sub frames on the window"""

        frame = self.frames[cont]
        frame.tkraise()


class ThirdFrame(tk.Frame):

    """This class is responsible for holding all the other necessary components in the frame.
    Some of them are generating the word dashes, displaying the letters above the dashes, etc.
    It is is the super class of the SecondFrame."""

    def __init__(self, parent, controller):

        """This method is called as soon as ThirdFrame object is created.
        It holds all the necessary parameters, class variables required for the ThirdFrame class execution."""

        global word_canvas, coordinate_list, display_hangman_coordinates
        self.controller = controller
        tk.Frame.__init__(self, parent)
        display_hangman_coordinates = [{'rope': [230, 82, 1]}, {'face': [230, 143, 2]}, {'body': [230, 213, 3]},
                                       {'left_hand': [200, 195, 4]}, {'right_hand': [260, 195, 5]},
                                       {'left_leg': [210, 300, 6]}, {'right_leg': [250, 300, 7]}]
        word_canvas = tk.Canvas(self, bg='#40434E', height='500', width='620', highlightthickness=0)
        word_canvas.grid(row=1, column=0, sticky='e')
        coordinate_list = []
        self.word_length = 0
        reset_btn = tk.Button(word_canvas, text="Reset Score", width=11, height=1, bg='#83bca9', fg="black",
                              activebackground='#465e56', font=("Verdana", 11, 'bold'), command=self.reset_btn)
        word_canvas.create_window(170, 430, window=reset_btn)
        close_btn = tk.Button(word_canvas, text="Close", width=7, height=1, bg='#83bca9', fg="black",
                              activebackground='#465e56', font=("Verdana", 11, 'bold'), command=self.close_btn)
        word_canvas.create_window(320, 430, window=close_btn)
        word_canvas.bind('<Configure>', self.dashes)

    @staticmethod
    def reset_btn():

        """This method is called when the reset score button is clicked. It resets the score of the game."""

        global word_canvas, score_lbl, win_score, total_score
        win_score = total_score = 0
        word_canvas.itemconfig(score_lbl, text="{}/{}".format(win_score, total_score))

    def close_btn(self):

        """This method is called when the close button is clicked. It closes the game window."""

        self.controller.destroy()

    @staticmethod
    def populate_coordinate_list():

        """This method is responsible for generating a coordinate list which will be referred for displaying the
        dash lines on the window."""

        x_odd, x_even = 210, 235
        for i in range(len(word)):
            if i % 2 == 0:
                coordinate_list.append(x_even)
                x_even += 25
            else:
                coordinate_list.insert(0, x_odd)
                x_odd -= 25

    def dashes(self, event=None):

        """This method is responsible for creating and displaying the dash lines on the window."""

        global word_canvas
        word_canvas.delete("dashes")
        self.populate_coordinate_list()
        y = 230
        self.word_length = len(word)
        for i, let in enumerate(word):
            if let == ' ':
                self.word_length -= 1
                pass
            else:
                word_canvas.create_line([(coordinate_list[i], y), (coordinate_list[i] + 20, y)],
                                        tag='dashes', width=4, fill="#ff3c3c")
        self.other_elements()

    def other_elements(self):

        """This method used to display the other element present in this frame which are the hint, score and
        number of letters in the word."""

        global word_letters_lbl, hint_lbl, score_lbl
        word_letters_lbl = word_canvas.create_text(250, 80, text="{} LETTER WORD".format(self.word_length),
                                                   font=("Verdana", 15, 'bold'), fill='#465e56')
        hint_lbl = word_canvas.create_text(250, 50, text="This is a {}".format(hint_word), font=("Verdana", 16, 'bold'),
                                           fill='#465e56')
        score_lbl = word_canvas.create_text(250, 320, text="{}/{}".format(win_score, total_score),
                                            font=("Verdana", 14, 'bold'), fill='#83bca9')

    def next_btn(self):

        """This button is called when the next word button on the window is clicked.
        It is responsible for setting up the new word and makes the necessary changes associated with it."""

        global word_canvas, word_letters_lbl, coordinate_list, word, hint_word
        self.wrong_guesses = 0
        self.clicked_btns = []
        coordinate_list = []
        [hangman_canvas.delete(i) for j in display_hangman_coordinates for i in j.keys()]
        for i in self.buttons:
            i.config(state="normal", relief='raised')
        word_canvas.itemconfig(word_letters_lbl, text=" ")
        word_canvas.delete("display_letters")
        word_canvas.itemconfig(score_lbl, text=" ")
        hint_word = random.choice(list(v.word_dict.keys()))
        word = random.choice(v.word_dict[hint_word]).lower()
        self.dashes()
        next_word_btn.config(state='disabled')


class SecondFrame(ThirdFrame):

    """This class is responsible for displaying the hangman in the frame.
    It is the super class of the FirstFrame and sub class of the ThirdFrame"""

    def __init__(self, parent, controller):

        """This method is called as soon as SecondFrame object is created.
        It holds all the necessary parameters, class variables required for the SecondFrame class execution."""

        global hangman_canvas
        tk.Frame.__init__(self, parent)
        hangman_canvas = tk.Canvas(self, bg='#40434E', height='500', width='350', highlightthickness=0)
        hangman_canvas.grid(row=1, column=0, sticky='w')
        self.load_images()
        hangman_canvas.create_image(150, 240, tag='pole', image=all_images[0])

    def load_images(self):

        """This method is responsible for loading the images from the external folders into the program.
        It is called only once inside the SecondFrame’s init method."""

        image_name = ['pole', 'rope', 'face', 'body', 'left_hand', 'right_hand', 'left_leg', 'right_leg']
        for i in image_name:
            name = "hangman pics/{}.png".format(i)
            image1 = tk.PhotoImage(file=name)
            all_images.append(image1)

    def show_hangman(self):

        """This method  is responsible for displaying the hangman parts as necessary on the window."""

        for key, value in display_hangman_coordinates[self.wrong_guesses].items():
            hangman_canvas.create_image(value[0], value[1], tag=key, image=all_images[value[2]])
        self.wrong_guesses += 1
        if self.wrong_guesses > 6:
            self.win_or_lose(False)

    def win_or_lose(self, value):

        """This method is responsible for deciding whether a player has won or lost the game."""

        for i in self.buttons:
            i.config(state="disabled")
        global word_letters_lbl, total_score, win_score, next_word_btn, hint_lbl, score_lbl
        if value:
            word_canvas.itemconfig(word_letters_lbl, text=self.win_statements[random.randint(0, 4)],
                                   font=("Verdana", 16, 'bold'), fill='white')
            win_score += 1
        else:
            word_canvas.itemconfig(word_letters_lbl,
                                   text= self.lose_statements[random.randint(0, 4)].format(word.upper()),
                                   font=("Verdana", 16, 'bold'), fill='white')
        total_score += 1
        word_canvas.itemconfig(hint_lbl, text=" ")
        word_canvas.itemconfig(score_lbl, text="{}/{}".format(win_score, total_score))
        next_word_btn.config(state="normal")


class FirstFrame(SecondFrame):

    """This class Is responsible for the generation and functionality of all the letter buttons displayed on the top
    of the frame. It’s super class is the SecondFrame."""

    def __init__(self, parent, controller):

        """This method is called as soon as FirstFrame object is created.
        It holds all the necessary parameters, class variables required for the FirstFrame class execution."""

        global word_canvas, coordinate_list, next_word_btn, hangman_canvas
        self.controller = controller
        tk.Frame.__init__(self, parent, height='100', width='970', bg='#40434E', highlightthickness=0)
        self.clicked_btns = []
        self.buttons = []
        self.wrong_guesses = 0
        self.win_statements = ["Awesome! Correct answer.", "You did it! Well played.", "Great Going!",
                               "That's correct!", "Wonderful! It's the right answer."]
        self.lose_statements = ["Sorry! The word is {}", "Oops! The right answer is {}",
                                "Well tried! It is {}", "Great effort! The word is {}",
                                "Great game. The answer is {}"]
        next_word_btn = tk.Button(word_canvas, text="Next Word", width=10, height=1, state="disabled",
                                  bg='#83bca9', fg="black", activebackground='#465e56', font=("Verdana", 11, 'bold'),
                                  command=lambda: self.next_btn())
        word_canvas.create_window(400, 320, window=next_word_btn)
        self.bind('<Configure>', self.create_buttons)

    def all_match(self):

        """This method is responsible for matching the original word with the word guessed by the player"""

        if set(list(word.replace(" ", ''))) == set(self.clicked_btns):
            super().win_or_lose(True)

    def letter_in_word(self, letter):

        """This method is responsible for checking whether the letter choosen by the player is a part of the original
        word or not."""

        if letter in word:
            position = [match.start() for match in re.finditer(letter, word)]
            if position:
                for i in position:
                    self.clicked_btns.insert(i, letter)
                    word_canvas.create_text(coordinate_list[i]+10, 215, text=letter.upper(),
                                            font=("Verdana", 17, 'bold'), fill='#83bca9', tag="display_letters")
            self.all_match()
        else:
            if self.wrong_guesses <= 6:
                super().show_hangman()
            else:
                super().win_or_lose(False)

    def on_btn_click(self, index, letter):

        """This method is bound with the letter buttons command option.
        It is used to change the features of the button like the state, relief, etc."""

        self.buttons[index].config(relief="sunken", state="disabled")  # Change state and relief of the button by index
        self.letter_in_word(letter.lower())

    def create_buttons(self, event=None):

        """This method is used to generate and handle the functionality of the letter buttons displayed on the frame"""

        letters = []
        for c in range(65, 91):
            letters.append(chr(c))

        # A collection (list) to hold the references to the buttons created below
        for index in range(len(letters)):
            n = letters[index]

            button = tk.Button(self, bg='#83bca9', fg="white", activebackground='#465e56',
                               font=("Verdana", 11, 'bold'), text=n, width=5, height=1,
                               command=lambda index1=index, n1=n: self.on_btn_click(index1, n1))

            # Add the button to the window
            if n <= 'M':
                button.grid(row=0, column=index, sticky='n', padx=(6.5, 6.5), pady=(6.5, 3.5))
            else:
                button.grid(row=1, column=index-13, sticky='n', padx=(6.5, 6.5), pady=(6.5, 3.5))
            # Add a reference to the button to 'buttons'
            self.buttons.append(button)


app = MainFrame()
app.title("Hangman")
app.resizable(0, 0)
app.mainloop()

