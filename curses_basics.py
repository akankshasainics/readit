import curses
from curses import wrapper
max_width = 50
new_line_char_ascii = 10
line_end_positions = []
user_inputs = []
user_input = ""
i = 0
j = 0



def handle_backspace_key(stdscr: curses.window):
    global user_input
    global i
    global j
    global user_inputs
    stdscr.clear()
    i -= 1
    if i < 0 and j < 0:
        i = 0
        j = 0
        user_input = ""
        user_inputs = []
        return
    if i == -1:
        j = j-1
        if len(user_inputs) > 0:
            prev_string = user_inputs.pop() 
            i = len(prev_string)
            user_input = prev_string + user_input
            handle_backspace_key(stdscr)
            return
    if i >= 0 and j >= 0:
        user_input = user_input[:i] + user_input[i+1:]
        display_prev_lines(stdscr)
        stdscr.addstr(j,0, user_input)

def handle_new_line():
    global i
    global j
    global user_input
    global user_inputs
    i = 0
    j += 1
    user_inputs.append(user_input[:i] + chr(10))
    user_input = user_input[i:]

def display_prev_lines(stdscr: curses.window):
    global user_inputs
    for count, user_string in enumerate(user_inputs):
        stdscr.addstr(count, 0, user_string)



def display_char(stdscr: curses.window, c: int):
    global i
    global j
    global user_input
    y,x = stdscr.getyx()
    if x == max_width:
        handle_new_line() 
    stdscr.clear()
    display_prev_lines(stdscr)
    first_split = user_input[:i]
    second_split = user_input[i:]
    stdscr.addstr(j, 0, first_split)
    i = len(first_split)
    stdscr.addch(j, i, chr(c))
    i += 1
    stdscr.addstr(j, i, second_split)
    user_input = first_split + chr(c) + second_split

def handle_arrow_right_key(stdscr: curses.window):
    global i
    global j
    i = min(max_width, i+1)
    stdscr.move(j, i)

def handle_arrow_left_key(stdscr: curses.window):
    global i
    global j
    i = max(0, i-1)
    stdscr.move(j, i)
   
def main(stdscr: curses.window):
    global user_input
    global i
    global j
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.clear()
    while True:
        try:
            c = stdscr.getch()
            if c == 127: 
                handle_backspace_key(stdscr)
            elif c == 260: 
                handle_arrow_left_key(stdscr)
            elif c == 261:
                handle_arrow_right_key(stdscr)
            elif c == 10:
                handle_new_line()
            else:
                display_char(stdscr, c)
            stdscr.move(j, i) 
            stdscr.refresh()
        except curses.error as e:
            b = e 
            print(e)
            pass

try:
    wrapper(main)
except KeyboardInterrupt:
    print("Keyboard Interrupt")