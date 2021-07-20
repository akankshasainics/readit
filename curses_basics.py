import curses
from curses import wrapper
max_width = 50
new_line_char_ascii = 10
buffer = ""
i = 0
j = 0

def get_overall_index() -> int:
    global i
    global j
    index = 0
    count = 0
    k = 0
    while k < len(buffer) and count < j:
        index += 1
        c = buffer[k]
        if c == "\n":
            count += 1
        k += 1
    index += i
    return index
        
def get_length_of_prev_line() -> int:
    global i
    global j
    count = 0
    prev_line_length = 0
    for c in buffer:
        if c == "\n":
            count += 1
            if count == j+1:
                break
            prev_line_length = 0
        else:
            prev_line_length += 1
    return prev_line_length


def handle_backspace_key(stdscr: curses.window):
    global buffer
    global i
    global j
    if not (i == 0 and j == 0):
        stdscr.clear()
        i -= 1
        if i < 0 and j < 0:
            i = 0
            j = 0
            buffer = ""
            return
        x = get_overall_index()
        if i < 0:
            j -= 1
            i = get_length_of_prev_line()
        buffer = buffer[:x] + buffer[x+1:]
        stdscr.addstr(0, 0, buffer)

      
def handle_new_line(stdscr: curses.window):
    global i
    global j
    global buffer
    x = get_overall_index()
    buffer = buffer[:x] + chr(10) + buffer[x:]
    stdscr.addstr(0, 0, buffer)
    i = 0
    j += 1


def display_char(stdscr: curses.window, c: int):
    global i
    global j
    global buffer
    y,x = stdscr.getyx()
    if x == max_width:
        handle_new_line(stdscr) 
    stdscr.clear()
    index = get_overall_index()
    first_split = buffer[:index]
    second_split = buffer[index:]
    stdscr.addstr(0, 0, first_split)
    stdscr.addch(j, i, chr(c))
    i += 1
    stdscr.addstr(j, i, second_split)
    buffer = first_split + chr(c) + second_split

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
    global buffer
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
                handle_new_line(stdscr)
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