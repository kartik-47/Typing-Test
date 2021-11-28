import curses
from curses import wrapper # it is used to initializes the curses module to use the terminal
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!") # 1 and 0 is basically saying that go 1 line down and start from 0 (row,column)
    stdscr.addstr("\nPress any key to begin!")
    # and if we copy the above line and put a coordinates which are on the same row then they can be overright on the previous mssg
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time() # its keeping track of the start time which is basically a large set of no. generally called as 'epoch'
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) # to calculate the Words Per Minute(WPM)
        #        this above is characters per min. and if we divide it by 5 then it becomes WPM

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey() # cause if we didnt press any keys it will throw exception so we handled it
        except:
            continue 

        if current_text == []: # this will start the wpm counter only when the user types
            start_time = time.time()

        #if ord(key) == 27: (this doesn't work maybe on this version or os) # ord is basically a ordinal value which is like ascii or unicode value of any character i.e. in this 27 is for esc key
        if key in ["\x1b"]:
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)       

def main(stdscr): #std screen
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)       
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue....")
        key = stdscr.getkey()

        if key in ["\x1b"]:
            break

wrapper(main)
