from tkinter import *
from constants import APP_TITLE, BACKGROUND_COLOR, CANVAS_WIDTH, CANVAS_HEIGHT, FRENCH, ENGLISH, LANGUAGE_FONT, WORD_FONT, PADDING
import random

import pandas

words = []
words_to_learn = []
timer = None
current_word = {}


def read_word_file():
    global words

    try:
        data = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data = pandas.read_csv("data/french_words.csv")
    words = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text=ENGLISH, fill="white")
    canvas.itemconfig(word_text, text=current_word[ENGLISH], fill="white")


def next_card():
    global timer, current_word

    window.after_cancel(timer)
    current_word = random.choice(words)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text=FRENCH, fill="black")
    canvas.itemconfig(word_text, text=current_word[FRENCH], fill="black")
    timer = window.after(3000, flip_card)


def on_click_know():
    words.remove(current_word)
    data = pandas.DataFrame(words)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title(APP_TITLE)
window.config(padx=PADDING, pady=PADDING, bg=BACKGROUND_COLOR)
timer = window.after(3000, flip_card)

canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=card_front_img)
language_text = canvas.create_text(CANVAS_WIDTH / 2, 150, text="", font=LANGUAGE_FONT)
word_text = canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

dont_know_img = PhotoImage(file="images/wrong.png")
dont_know_button = Button(image=dont_know_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
dont_know_button.grid(row=1, column=0)

know_img = PhotoImage(file="images/right.png")
know_button = Button(image=know_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=on_click_know)
know_button.grid(row=1, column=1)

read_word_file()
next_card()
window.mainloop()
