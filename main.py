from tkinter import *
from plyer import notification
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = .2
SHORT_BREAK_MIN = .3
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    #I need to reset the timer_text to 00:00
    canvas.itemconfig(timer_text, text=f"00:00")
    #the title_label "Timer"
    time_label.config(text="Timer", fg=RED)
    #reset the checkmarks
    check_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    # this function will be responsible for calling the countdown method:
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        time_label.config(text="Long break", fg = RED)
        count_down(long_break_sec)
        # sent a notification
        notification.notify(
        title = 'take a break',
        message = "Is time to take a long break.",
        app_icon = 'break.ico')

    elif reps % 2 == 0:
        time_label.config(text="Break", fg = PINK)
        count_down(short_break_sec)
        # sent a notification
        notification.notify(
        title = 'take a break',
        message = "Is time to take  break.",
        app_icon = 'break.ico')

    else:
        time_label.config(text="Work!", fg = GREEN)
        count_down(work_sec)
        # sent a notification
        notification.notify(
        title = 'time to work',
        message = "Is time to work.",
        app_icon = 'study.ico')

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    # ms stands for miliseconds
    # if we want to edit a canvas, we need to put the canvas and call the "itemconfig" method
    # and we pass the "text" as a *kwarg
    canvas.itemconfig(timer_text, text =f"{count_min}: {count_sec}")
    if count > 0:
        # we're giving a name of a variable in order to edit the variable to reset the timer
        global timer
        timer = window.after(1000, count_down, count -1)
    else:
        start_timer()
        check_marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            check_marks += "✔"
        check_label.config(text = check_marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("🍅Pomodoro Technique🍅")
# bg stands for background
window.config(padx= 100, pady= 50, bg = YELLOW)

# this canvas will help me lay images one on top of the other.
canvas = Canvas(width=200, height=224, bg = YELLOW, highlightthickness = 0)

# we're going to save this photo image into a variable
tomato_img = PhotoImage(file ="tomato.png")
canvas.create_image(100,112, image = tomato_img)
# we need to assign a variable as a timer_text for the countdown
timer_text = canvas.create_text(100, 130, text = "00:00", fill = "white", font= (FONT_NAME, 35, "bold"))
canvas.grid(column = 1, row = 1)

# Time Label
time_label = Label(text = "TIMER", fg = GREEN, bg = YELLOW, font = (FONT_NAME, 30, "italic", "bold"))
time_label.grid(column = 1, row = 0)

# check label
check_label = Label(fg = GREEN, bg = YELLOW, font = (FONT_NAME, 20, "bold"))
check_label.grid(column = 1, row= 3)

# buttons
# start button
start_button = Button(text = "Start", command = start_timer)
start_button.grid(column = 0, row =2)

# reset button
reset_button = Button(text = "Reset", command = reset_timer)
reset_button.grid(column = 2, row = 2)

window.mainloop()