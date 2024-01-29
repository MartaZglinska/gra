# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 22:16:16 2024

@author: Admin
"""

import tkinter as tk
import random

# lista słów do zgadywania
word_list = []

# definiowanie tablicy grafik
hangman_art = ['''
   +---+
       |
       |
       |
      ===''', '''
   +---+
   O   |
       |
       |
      ===''', '''
   +---+
   O   |
   |   |
       |
      ===''', '''
   +---+
   O   |
  /|   |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
  /    |
      ===''', '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''']


with open('passwords.txt') as file:
    file_content = file.read()
    word_list = file_content.split()


# funkcja do zwracania losowego słowa z puli
def choose_word():
    return random.choice(word_list)


# funkcja do aktualizowania obrazku wisielca
def update_hangman(mistakes):
    hangman_label.config(text=hangman_art[mistakes])


# funkcja do sprawdzania czy podana litera zawiera się w wylosowanym słowie
def check_guessed_letter(guess):
    global word_with_blanks
    guess_entry.delete(0, tk.END)
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                word_with_blanks = word_with_blanks[:i] + guess + word_with_blanks[i+1:]
        word_label.config(text=word_with_blanks)
        if '_' not in word_with_blanks:
            end_game("win")
    else:
        global mistakes
        mistakes += 1
        update_hangman(mistakes)
        if mistakes == 6:
            end_game("lose")


# funckja do zakończenia gry
def end_game(result):
    if result == 'win':
        result_text = "Zwycięstwo!"
    else:
        result_text = "Przegrana.\nSzukane słowo to \n'" + word + "'"
    result_label.config(text=result_text)
    guess_entry.config(state="disabled")
    guess_button.config(state="disabled")


# funkcja do ograniczenia możliwości wpisywania słów w pole guess_entry (tylko pojedyńcze litery)
def on_keypress(event):
    guess_value = guess_entry.get()
    if len(guess_value) >= 1:
        guess_entry.delete(0, tk.END)


# tworzenie głównego okna
root = tk.Tk()
root.title("Wisielec")
root.minsize(width=800, height=800)
root.grid_columnconfigure(0, weight=1)

# label do wyświetlania wisielca
hangman_label = tk.Label(root, font=("CourierK", 30))
hangman_label.grid(row=0, column=0, sticky='')

# label do wyświetlania wylosowanego słowa
word = choose_word()
word_with_blanks ='_' * len(word)
word_label = tk.Label(root, text=word_with_blanks, font=("Arial", 40))
word_label.grid(row=1, column=0)

# pole do wpisywania liter oraz przycisk do zatwierdzania
entry_frame = tk.Frame(root)
entry_frame.grid(row=2, column=0)
entry_frame.grid_columnconfigure([0, 1], weight=1)
guess_entry = tk.Entry(entry_frame, width=3, font=("Arial", 40))
guess_entry.bind("<KeyPress>", on_keypress)
guess_entry.grid(row=0, column=0, sticky='e', padx=10)
guess_button = tk.Button(entry_frame, text="Sprawdź", command=lambda: check_guessed_letter(guess_entry.get()))
guess_button.grid(row=0, column=1, sticky='w', padx=10)

# label wyniku
result_label = tk.Label(root, font=("Arial", 40))
result_label.grid(row=3, column=0)

# inicjalizacja gry
mistakes = 0
update_hangman(mistakes)

# główna pętla tkintera
root.mainloop()