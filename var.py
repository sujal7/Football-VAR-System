import tkinter
from tkinter.constants import ANCHOR
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time
from pygame import mixer
from numpy.core.fromnumeric import size

mixer.init()
mixer.music.load("media/music.mp3")
mixer.music.play()
music_flag = 1
stream = cv2.VideoCapture("media/clip1.mp4")
flag = True
def play(speed):
    global flag
    print(f"Play. Your Speed is {speed}.")
    # Play video in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    if not grabbed: # exits when video footage is ended
        exit()
    frame = imutils.resize(frame, width=900)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)
    if flag:    # blinks Checking Goal text
        canvas.create_text(770, 480, fill="black", font="Arial 25 bold", text="Checking Goal")
    flag = not flag
    # Play video in forward
# Width and Height of our main screen
SET_WIDTH = 900
SET_HEIGHT = 650

def pending(decision):
    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread("img/pending.jpeg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=900, height=506)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)
    
    # Wait for few seconds
    time.sleep(2)

    # Display sponsor image
    frame = cv2.cvtColor(cv2.imread("img/sponsor.jpeg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=900, height=506)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)

    # Wait for few seconds
    time.sleep(2)

    # Display decision image
    if decision == 'goal':
        decision_img = "img/goal.jpeg"
    else:
        decision_img = "img/no_goal.jpeg"
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=900, height=506)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)


def goal():
    thread = threading.Thread(target= pending, args=("goal",))
    thread.daemon = 1
    thread.start()
    print("GOAL!")

def no_goal():
    thread = threading.Thread(target= pending, args=("no goal",))
    thread.daemon = 1
    thread.start()
    print("OFFSIDE! NO GOAL!")

def play_music():
    global music_flag
    if music_flag == 1:
        music_flag = 0
        mixer.music.pause()
    else:
        music_flag= 1
        mixer.music.unpause()


# Tkinter GUI starts from here
window = tkinter.Tk()
window.title("VAR System by Sujal Duwa")
cv_img = cv2.cvtColor(cv2.imread("img/main_menu.jpeg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_cavnas = canvas.create_image(0,0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="Play/Pause Music", width=25, command=play_music)
btn.pack()
btn.place(x=375, y=530)
btn = tkinter.Button(window, text="<<< Previous (Fast)", width=25, command=partial(play, -25))
btn.pack()
btn.place(x=20, y=570)
btn = tkinter.Button(window, text="<< Previous (Slow)", width=25, command=partial(play, -2))
btn.pack()
btn.place(x=250, y=570)
btn = tkinter.Button(window, text="Next (Slow) >>", width=25, command=partial(play, 2))
btn.pack()
btn.place(x=480, y=570)
btn = tkinter.Button(window, text="Next (Fast) >>>", width=25, command=partial(play, 25))
btn.pack()
btn.place(x=710, y=570)
btn = tkinter.Button(window, text="GOAL", width=25, command=goal)
btn.pack()
btn.place(x=250, y=610)
btn = tkinter.Button(window, text="NO GOAL - OFFSIDE", width=25, command=no_goal)
btn.pack()
btn.place(x=480, y=610)

window.mainloop()

