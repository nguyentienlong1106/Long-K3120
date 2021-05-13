def draw_loglines(self):
        self.screen.clear()
        status_col = 4
        bytes_col = 6 
        remote_host_col = 20
        status_start = 0 
        bytes_start = 4 
        remote_host_start = 10
        line_start = 26 
        logline_cols = curses.COLS - status_col - bytes_col - remote_host_col - 1
        for i in range(curses.LINES):
            c = self.curr_topline
            try:
                curr_line = self.loglines[c]
            except IndexError:
                break
            self.screen.addstr(i, status_start, str(curr_line[2]))
            self.screen.addstr(i, bytes_start, str(curr_line[3]))
            self.screen.addstr(i, remote_host_start, str(curr_line[1]))
            #self.screen.addstr(i, line_start, str(curr_line[4])[logline_cols])
            self.screen.addstr(i, line_start, str(curr_line[4]), logline_cols)
            self.curr_topline += 1 
        self.screen.refresh()