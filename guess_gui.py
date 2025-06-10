import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Game state
secret_number = random.randint(1, 100)
attempts = 0

# Function to check the user's guess
def check_guess():
    global attempts
    try:
        guess = int(entry.get())
        attempts += 1
        if guess < secret_number:
            feedback_label.config(text="📉 Too low! Try again.")
        elif guess > secret_number:
            feedback_label.config(text="📈 Too high! Try again.")
        else:
            messagebox.showinfo("🎉 You Win!", f"Correct! You guessed it in {attempts} tries.")
            reset_game()
    except ValueError:
        feedback_label.config(text="❌ Please enter a valid number.")

# Reset game for replay
def reset_game():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    entry.delete(0, tk.END)
    feedback_label.config(text="")

# Set up the window
root = tk.Tk()
root.title("Guess the Number - Log Cabin Edition")
root.geometry("500x400")
root.resizable(False, False)

# Load and display the background image
bg_image = Image.open("log_cabin_background.png")
# bg_image = bg_image.resize((500, 400), Image.ANTIALIAS)
bg_image = bg_image.resize((500, 400))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Entry box for guesses
entry = tk.Entry(root, font=("Helvetica", 16))
entry.place(x=150, y=150, width=200)

# Guess button
guess_button = tk.Button(root, text="Guess", font=("Helvetica", 14), command=check_guess)
guess_button.place(x=210, y=200)

# Feedback label
feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="white")
feedback_label.place(x=150, y=250, width=200)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=("Helvetica", 12), command=reset_game)
reset_button.place(x=200, y=300)

# Run the GUI loop
root.mainloop()
