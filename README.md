# Hangman

This is my version of the Hangman game.
This desktop application is a simple implementation of Python3 programming using GUI support.

## Description

Hangman is a paper and pencil guessing game for two or more players. One player thinks of a word,
phrase or sentence and the other(s) tries to guess it by suggesting letters within a certain number of guesses.
If the guessing player suggests a letter which occurs in the word, the other player writes it in all
its correct positions. If the suggested letter does not occur in the word, the other player draws one element of a
hanged man stick figure as a tally mark.

## About

For this project I have - 
1) Used Object Oriented Programming approach
2) Used Python3 for coding and tkinter for GUI support 
3) Internal code documentation.
4) Built an .exe for checking the execution of the program

## Contents
The uploaded folder consists of - 

1) A code file, named hangman.py.
2) A folder containing the images used for the game, named Images-Hangman.
3) A file holding the word dictionary, named words_dictionary.py
4) An .exe file which works on 64 bit windows operating systems, named Hangman.exe.

## Requirements

Apart from Python3, you will also need the tkinter package which is used for the GUI support.
It is a built-in package provided by Python, but in any case just cross check the same by running a small 
code in Python.

```bash
import tkinter
tkinter._test()
```

This should pop up a small window; the first line at the top of the window should say "This is Tcl/Tk version 8.5"
If this happens, you are good to go.
