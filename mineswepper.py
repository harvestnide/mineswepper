from tkinter import *
import random
from datetime import datetime

rows = 10
columns = 10
bombs = 25
btn = []


class Cell(object):
    def __init__(self, tk, x, y):
        self.x = x;
        self.y = y
        self.mine = False
        self.value = -1
        self.window = tk
        self.text = StringVar()
        self.text.set("")
        self.button = Button(tk, textvariable=self.text, bg='white', fg='red', padx="10", pady="7")
        self.state = 0  # 0 - закрыта, 1 - открыта, 2 - флаг, 3 - ?
        self.button.bind('<Button-1>', lambda event, state=1: self.set_state(event, state))
        self.button.bind('<Button-3>', lambda event, state=2: self.set_state(event, state))

    def get_button(self):
        return self.button

    def set_state(self, event, state):
        btn_text = ["", "F", "?"]
        if state == 1:
            self.reveal()
        elif state == 2:
            self.state = (self.state + 1) % 3
            self.text.set(btn_text[self.state])

    def reveal(self):
        self.value = get_value(self.x, self.y)
        if self.mine:
            gameover(self.window)
        self.button.config(highlightthickness=0)
        if self.value == 0:
            for dx in range(self.x - 1, self.x + 2):
                for dy in range(self.y - 1, self.y + 2):
                    if 0 <= dx < rows and 0 <= dy < columns and not (dx == self.x and dy == self.y):
                        if btn[dx][dy].state == 0:
                            btn[dx][dy].reveal()
        else:
            self.text.set(str(self.value))


def get_value(x, y):
    global btn
    if btn[x][y].value == -1:
        value = 0
        for dx in range(x - 1, x + 2):
            for dy in range(y - 1, y + 2):
                if 0 <= dx < rows and 0 <= dy < columns and btn[dx][dy].mine:
                    value += 1
        btn[x][y].value = value
        return value
    else:
        return btn[x][y].value


def start(settings, bombs_str, rows_str, columns_str):
    if bombs_str != "\n":
        global bombs
        bombs = int(bombs_str)
    if rows_str != "\n":
        global rows
        rows = int(rows_str)
    if columns_str != "\n":
        global columns
        columns = int(columns_str)
    settings.destroy()
    root = Tk()
    root.title('Сапер')
    frame = Frame(root)
    frame.grid(row=0, column=0)
    global btn
    btn = [[Cell(root, x, y) for x in range(rows)] for y in range(columns)]
    for x in range(rows):
        for y in range(columns):
            btn[x][y].get_button().grid(column=x, row=y)
    root.resizable(False, False)
    for i in range(bombs):
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)
        if btn[x][y].mine:
            i -= 1
        else:
            btn[x][y].mine = True
    root.mainloop()


def gameover(tk):
    tk.destroy()
    gg = Tk()
    print('gg')
    gg.title('GG')
    gg.geometry('210x150')
    Label(gg, text='Вы проиграли.').place(x=5, y=30)
    Label(gg, text='В следующий раз повезет больше!').place(x=5, y=47)
    Button(gg, text='Перезапустить', command=lambda: [f() for f in [gg.destroy, main]]).place(x=60, y=75)
    Button(gg, text='Выход', fg='#000000', command=lambda: exit(0)).place(x=80, y=105)
    gg.mainloop()


def main():
    settings = Tk()
    settings.title('Настройки')
    settings.geometry('200x150')
    mine = Text(settings, width=5, height=1)
    mine_lab = Label(settings, height=1, text='Бомбы:')
    rows = Text(settings, width=5, height=1)
    rows_lab = Label(settings, height=1, text='Ширина:')
    columns = Text(settings, width=5, height=1)
    columns_lab = Label(settings, height=1, text='Высота:')
    but = Button(settings, text='Начать:', fg='#ffffff',
                 command=lambda settings=settings, bombs=mine.get('1.0', END), rows=rows.get('1.0', END),
                                columns=columns.get('1.0', END): start(settings, bombs, rows, columns))
    but.place(x=70, y=90)
    mine.place(x=75, y=5)
    mine_lab.place(x=5, y=5)
    rows.place(x=75, y=30)
    rows_lab.place(x=5, y=30)
    columns.place(x=75, y=55)
    columns_lab.place(x=5, y=55)
    settings.mainloop()


if __name__ == "__main__": main()
