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
        self.value = 0
        self.window = tk
        self.text = StringVar()
        self.text.set("")
        self.button = Button(tk, textvariable=self.text, bg='white', fg='red', padx="10", pady="7")
        self.state = 0  # 0 - закрыта, 1 - открыта, 2 - флаг, 3 - ?
        self.button.bind('<Button-1>', lambda event, state=1: self.set_state(event, state))
        self.button.bind('<Button-3>', lambda event, state=2: self.set_state(event, state))

    def get_button(self):
        return self.button

    def get_state(self):
        return self.state

    def set_state(self, event, state):
        btn_text = ["", "F", "?"]
        if state == 1:
            if self.mine:
                gameover(self.window)
            self.reveal()
        elif state == 2:
            self.state = (self.state + 1) % 3
            self.text.set(btn_text[self.state])

    def reveal(self):
        self.value = get_value(self.x, self.y)
        if self.value == 0:
            for dx in range(self.x - 1, self.x + 2):
                for dy in range(self.y - 1, self.y + 2):
                    if 0 < dx < rows and 0 < dy < columns and not (dx == self.x and dy == self.y):
                        btn[dx][dy].reveal()
        else:
            self.text.set(str(self.value))


def get_value(x, y):
    global btn
    value = 0
    for dx in range(x - 1, x + 2):
        for dy in range(y - 1, y + 2):
            if 0 < dx < rows and 0 < dy < columns and btn[dx][dy].mine:
                value += 1
    return value


def start(settings):
    global bombs, rows, columns
    # if settings.mineText.get('1.0', END) == '\n':
    #     bombs = 10
    # else:
    #     bombs = int(settings.mineText.get('1.0', END))
    # settings.destroy()
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
    mineText = Text(settings, width=5, height=1)
    mineLabe = Label(settings, height=1, text='Бомбы:')
    highText = Text(settings, width=5, height=1)
    highLabe = Label(settings, height=1, text='Ширина:')
    lenghtText = Text(settings, width=5, height=1)
    lenghtLabe = Label(settings, height=1, text='Высота:')
    mineBut = Button(settings, text='Начать:', fg='#ffffff', command=lambda settings=settings: start(settings))
    mineBut.place(x=70, y=90)
    mineText.place(x=75, y=5)
    mineLabe.place(x=5, y=5)
    highText.place(x=75, y=30)
    highLabe.place(x=5, y=30)
    lenghtText.place(x=75, y=55)
    lenghtLabe.place(x=5, y=55)
    settings.mainloop()


if __name__ == "__main__": main()
