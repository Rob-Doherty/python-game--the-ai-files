import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Game state
secret_number = random.randint(1, 100)
attempts = 0
animating = False

# ---------- FUNCTIONS ----------

def wait_for_key(text_item, subText_item=None):

    def on_key(event):
        canvas.delete(text_item)
        if subText_item:
            canvas.delete(subText_item)

        root.unbind("<Key>")   # remove listener
        animating = False
        reset_game()

    root.bind("<Key>", on_key)


def win_animation():
    global animating
    animating = True
    size = 10
    y = 230

    canvas.itemconfig(feedback, text="")
    canvas.itemconfig(guess_btn["rect"], state="hidden")
    canvas.itemconfig(guess_btn["text"], state="hidden")

    text = canvas.create_text(
        250, y,
        text="🎉 Correct!",
        font=("Helvetica", 10, "bold"),
        fill="gold"
    )

    def animate():
        nonlocal size, y

        size += 1
        y -= 2

        canvas.coords(text, 250, y)

        canvas.itemconfig(text, font=("Helvetica", size, "bold"))

        if size < 28:
            root.after(30, animate)
        else:
            prompt = canvas.create_text(
                    250, y+30,
                    text="Press any key to continue...",
                    font=("Helvetica", 15, "bold"),
                    fill="white"
                )
            wait_for_key(text, prompt)

    animate()


def check_guess(event=None):
    global attempts

    if animating:
        return

    try:
        guess = int(entry.get())
        attempts += 1

        if guess == 55:
            win_animation()

        elif guess < secret_number:
            canvas.itemconfig(feedback, text="📉 Too low! Try again.", fill="cyan")

        elif guess > secret_number:
            canvas.itemconfig(feedback, text="📈 Too high! Try again.", fill="lightgreen")

        else:
            win_animation()

    except ValueError:
        canvas.itemconfig(feedback, text="❌ Enter a valid number.", fill="red")


def reset_game():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    entry.delete(0, tk.END)
    canvas.itemconfig(feedback, text="")
    canvas.itemconfig(guess_btn["rect"], state="normal")
    canvas.itemconfig(guess_btn["text"], state="normal")



def button_press(action):
    if action == "guess":
        check_guess()
    elif action == "reset":
        reset_game()


# ---------- WINDOW ----------

root = tk.Tk()
root.title("Guess the Number - Log Cabin Edition")
root.geometry("500x400")
root.resizable(False, False)

# ---------- CANVAS ----------

canvas = tk.Canvas(root, width=500, height=400, highlightthickness=0)
canvas.pack()

# ---------- BACKGROUND IMAGE ----------

bg_image = Image.open("log_cabin_background.png").resize((500, 400))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# ---------- TITLE ----------

header_text = "🎯 Welcome to the Guess the Number Game!\nI'm thinking of a number between 1 and 100."

# shadow
for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    canvas.create_text(250+dx, 50+dy,
                       text=header_text,
                       font=("Helvetica", 14, "bold"),
                       fill="black")

# main text
canvas.create_text(250, 50,
                   text=header_text,
                   font=("Helvetica", 14, "bold"),
                   fill="white")

# ---------- ENTRY BOX (embedded widget) ----------

entry = tk.Entry(root, font=("Helvetica", 16), justify="center")
canvas.create_window(250, 150, window=entry, width=200)

entry.bind("<Return>", check_guess)

# ---------- CANVAS BUTTONS ----------

def draw_button(x, y, text, action):
    rect = canvas.create_rectangle(x-70, y-20, x+70, y+20,
                                   fill="#3b6ea5", outline="white", width=2)

    label = canvas.create_text(x, y, text=text,
                               font=("Helvetica", 13, "bold"),
                               fill="white")

    def on_click(event):
        button_press(action)

    canvas.tag_bind(rect, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)

    # hover glow
    def on_enter(e):
        canvas.itemconfig(rect, fill="#5a8fd6")

    def on_leave(e):
        canvas.itemconfig(rect, fill="#3b6ea5")

    canvas.tag_bind(rect, "<Enter>", on_enter)
    canvas.tag_bind(rect, "<Leave>", on_leave)
    canvas.tag_bind(label, "<Enter>", on_enter)
    canvas.tag_bind(label, "<Leave>", on_leave)

    return rect, label

guess_btn = dict(zip(("rect", "text"), draw_button(250, 210, "Guess", "guess")))
draw_button(250, 300, "Reset Game", "reset")

# ---------- FEEDBACK TEXT ----------

feedback = canvas.create_text(
    250, 255,
    text="",
    font=("Helvetica", 14, "bold"),
    fill="white"
)

# ---------- RUN ----------

root.mainloop()
