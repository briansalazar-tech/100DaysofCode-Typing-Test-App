from tkinter import *

RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
timer = 60
typing = False

### APP FUNCTIONS ###
def pass_one():
    display_prompt(1)


def pass_two():
    display_prompt(2)


def pass_three():
    display_prompt(3)


def pass_four():
    display_prompt(4)


def display_prompt(prompt_number):
    """Based on which prompt button is pressed, the test with the corresponding prompt number is dispalyed onscreen."""
    with open(f"./prompts/test{prompt_number}.txt") as file:
        test_prompt = file.read()
        typing_test_text.config(state="normal")
        typing_test_text.delete("1.0", END)
        typing_test_text.insert(index=END, chars=test_prompt)
        typing_test_text.config(state="disabled", spacing2=5)


def count_down(seconds):
    """Timer mechanism that manages the typing test. If at 0 seconds, test is over."""
    global timer
    canvas.itemconfig(time_countdown, text=seconds)
    if typing == True:
        if seconds == 0: 
            user_entry_text.unbind("<KeyPress>")
            user_entry_text.config(state="disabled")
            calculate_score()

        if seconds > 0:
            timer = window.after(1000, count_down, seconds-1)


def key_pressed(event):
    """Once a key is pressed and character is entered in the user entry box, typing test and countdown begin."""
    global typing
    if typing == False:
        typing = True
        count_down(timer)


def calculate_score():
    """Calculates gross words-per-minute, accuracy, and net words-per-minute."""
    typed_characters = 0
    user_correct = 0
    user_errors = 0
    
    # Typing prompt values
    test_textbox_text = typing_test_text.get("1.0", END)
    test_textbox_words = test_textbox_text.split()
    test_textbox_characters = []
    
    # Users typed words and characters typed on-screen
    user_textbox_text = user_entry_text.get("1.0", END)
    user_textbox_words = user_textbox_text.split()
    user_textbox_characters = []

    for word in test_textbox_words:
        for char in word:
            test_textbox_characters.append(char)
    
    for word in user_textbox_words:
        for char in word:
            user_textbox_characters.append(char)

    # Typed user characters are compared against the prompts characters to add up total characters, correct characters and errors
    for char in range(len(user_textbox_characters)):
        typed_characters += 1
        if user_textbox_characters[char] == test_textbox_characters[char]:
            user_correct += 1
        else:
            user_errors += 1
    
    # Formulas for WPM and accuracy. Forumulas used: https://www.typingtyping.com/wpm-calculator/
    gross_wpm = round((((typed_characters / 5) / 60) * 100), 2)
    error_rate = user_errors / 60
    net_wpm = round(((((typed_characters / 5) - error_rate) / 60) * 100), 2)
    accuracy = round((user_correct / typed_characters) * 100)
    
    # Redraw the labels on the screen to reflect the user's score
    typing_speed_label.config(text=f"Typing Speed: {gross_wpm}")
    accuracy_label.config(text=f"Accuracy: {accuracy}%")
    adjusted_speed_label.config(text=f"Adjusted Speed: {net_wpm}")


def reset():
    """Resets test to pre-test settings so a new test can be started."""
    global typing, timer
    typing = False
    timer = 60
    canvas.itemconfig(time_countdown, text=timer)
    user_entry_text.config(state="normal")
    user_entry_text.delete("1.0", END)
    user_entry_text.bind("<KeyPress>", key_pressed)
    typing_speed_label.config(text="Typing Speed: ??.??")
    accuracy_label.config(text="Accuracy: ??%")
    adjusted_speed_label.config(text="Adjusted Speed: ??.??")


### GUI SETUP ###
# Window Setup
window = Tk()
window.title("TKinter Typing Speed Test")
window.config(bg=YELLOW, highlightthickness=0)
window.minsize(height=910, width=1100)

# App Name Label
title = Label(text="Typing Speed Test", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 45, "bold"))
title.place(x=20, y=0)

# Time Label
time_label = Label(text="Time Remaining: ", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 25, "bold"))
time_label.place(x=20, y=100)

# Time Countdown
canvas = Canvas(width=60, height=40, bg=YELLOW)
time_countdown = canvas.create_text(20, 20, text="60", fill=RED, font=(FONT_NAME, 25, "bold"))
canvas.place(x=330, y=100)

# Typing Speed Label
typing_speed_label = Label(text="Typing Speed: ??.??", bg=YELLOW, fg="black", font=(FONT_NAME, 20, "bold"))
typing_speed_label.place(x=20, y=150)

# Accuracy Label
accuracy_label = Label(text="Accuracy: ??%", bg=YELLOW, fg="black", font=(FONT_NAME, 20, "bold"))
accuracy_label.place(x=350, y=150)

# Adjusted Speed Label
adjusted_speed_label = Label(text="Adjusted Speed: ??.??", bg=YELLOW, fg="black", font=(FONT_NAME, 20, "bold"))
adjusted_speed_label.place(x=625, y=150)

# Prompt 1 Button
prompt1_button = Button(text="Typing Prompt 1", highlightthickness=0, command=pass_one)
prompt1_button.place(x=20, y=200)

# Prompt 2 Button
prompt2_button = Button(text="Typing Prompt 2", highlightthickness=0, command=pass_two)
prompt2_button.place(x=160, y=200)

# Prompt 3 Button
prompt3_button = Button(text="Typing Prompt 3", highlightthickness=0, command=pass_three)
prompt3_button.place(x=300, y=200)

# Prompt 4 Button
prompt4_button = Button(text="Typing Prompt 4", highlightthickness=0, command=pass_four)
prompt4_button.place(x=440, y=200)

# Typing Test Label
typing_test_label = Label(text="Typing Speed Test Prompt", bg=YELLOW, fg="black", font=(FONT_NAME, 20))
typing_test_label.place(x=20, y=250)

# Typing Test Text Box
typing_test_text = Text(width=95, height=11, font=("Arial", 14), wrap="word", spacing2=5)
typing_test_text.place(x=15, y=300)

# User Entry Label
user_entry_label = Label(text="Press start and type away!", bg=YELLOW, fg="black", font=(FONT_NAME, 20))
user_entry_label.place(x=20, y=560)

# User Entry Text Box
user_entry_text = Text(width=95, height=11, font=("Arial", 14), wrap="word", spacing2=5)
user_entry_text.place(x=15, y=610)
user_entry_text.bind("<KeyPress>", key_pressed)

# Reset Button
reset_button = Button(text="Reset", highlightthickness=0, command=reset)
reset_button.place(x=20, y=870)

window.mainloop()