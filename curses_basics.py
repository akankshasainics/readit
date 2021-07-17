import curses
from curses import wrapper
max_width = 50
new_line_char_ascii = 10
def main(stdscr: curses.window):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.clear()
    string = ""
    i = 0
    j = 0
    line_end_positions = []
    while True:
        try:
            c = stdscr.getch()
            if c == 127: # backspace key
                curses.setsyx(0, 0)
                stdscr.clear()
                i -= 1
                if i <= -1:
                    if j == 0:
                        i = 0
                    else:
                        if len(string) > 0 and ord(string[-1]) == 10:
                            j -= 1
                            if len(line_end_positions) > 0:
                                i = line_end_positions.pop()
                string = string[:-1]
                stdscr.addstr(0,0, string)
            else:
                y,x = stdscr.getyx()
                if x == max_width or c == 10:
                    line_end_positions.append(i)
                    stdscr.addch(j, i, chr(new_line_char_ascii))
                    string += chr(new_line_char_ascii)
                    j += 1
                    i = 0
                if c != 10:
                    string += chr(c)
                    stdscr.addch(j, i, chr(c))
                    i += 1

            stdscr.refresh()
        except curses.error as e:
            b = e 
            print(e)
            pass

try:
    wrapper(main)
except KeyboardInterrupt:
    print("Keyboard Interrupt")