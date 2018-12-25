from tkinter import *
import random

rows = 6
columns = 6
bombs = 9
btn = []


class Cell(object):
    def __init__(self, tk, x, y):
        self.x = x
        self.y = y  # координаты в таблице
        self.mine = False  # является ли миной
        self.value = 0  # количество мин среди "соседей"
        self.window = tk  # окно с игрой
        self.text = StringVar()  # текст на кнопке
        self.text.set("")
        self.button = Button(tk, textvariable=self.text, bg='white', fg='red', padx="10",
                             pady="7")  # кнопка. Передаем окно игры, текст, цвет фона и отступы
        self.state = 0  # 0 - закрыта, 1 - флаг, 2 - ?
        self.button.bind('<Button-1>', lambda event, state=0: self.set_state(state))  # нажатие ЛКМ
        self.button.bind('<Button-3>', lambda event, state=1: self.set_state(state))  # нажатие ПКМ

    def set_state(self, state):
        btn_text = ["", "F", "?"]  # спец. символы
        if state == 0 and self.state == 0:  # не откроется, если флаг или вопросик
            self.reveal()  # открытие клетки
        elif state == 1:
            self.state = self.state + 1
            self.text.set(btn_text[self.state % 3])  # текст на кнопке, переключается ПКМ

    def reveal(self):
        if self.mine:
            gameover(self.window)  # взрыв
        if self.value == 0:
            for dx in range(self.x - 1, self.x + 2):
                for dy in range(self.y - 1, self.y + 2):
                    if 0 <= dx < rows and 0 <= dy < columns and not (dx == self.x and dy == self.y):
                        if btn[dy][dx].state == 0:  # рекурсивно открываем соседние клетки, пока вокруг нет мин
                            btn[dy][dx].reveal()
        else:
            self.text.set(str(self.value))  # выводим значение с количеством мин вокруг


def start():
    root = Tk()  # создаем новое окно
    root.title('Сапер')
    frame = Frame(root)
    frame.grid(row=0, column=0)  # создаем таблицу для кнопок
    global btn
    btn = [[Cell(root, x, y) for x in range(rows)] for y in range(columns)]  # массив ячеек таблицы
    for x in range(rows):
        for y in range(columns):
            btn[x][y].button.grid(column=x, row=y)  # расставляем кнопки по таблице
    root.resizable(False, False)  # запрещаем изменение размеров окна с игрой
    for i in range(bombs):
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)  # генерация координат бомб
        if btn[x][y].mine:
            i -= 1  # если координаты двух бомб совпали, ставим еще одну
        else:
            btn[x][y].mine = True
            for dx in range(x - 1, x + 2):
                if -1 < dx < rows:
                    for dy in range(y - 1, y + 2):
                        if -1 < dy < columns:
                            btn[dx][dy].value += 1  # добавляем 1 к счетчику бомб среди соседей клетки
    root.mainloop()


def gameover(tk):
    tk.destroy()  # закрываем окно с игрой
    gg = Tk()  # создаем новое окно
    gg.title('GG')
    gg.geometry('210x150')  # задаем название окна и размер
    Label(gg, text='Вы проиграли.').place(x=5, y=30)
    Label(gg, text='В следующий раз повезет больше!').place(x=5, y=47)
    Button(gg, text='Перезапустить', command=lambda: [f() for f in [gg.destroy, start]]).place(x=60,
                                                                                               y=75)  # кнопка вызывает метод start, перезапуская игру и уничтожает это окно
    Button(gg, text='Выход', fg='#000000', command=lambda: exit()).place(x=80,
                                                                         y=105)  # выходит из программы, все окна закрываются автоматически
    gg.mainloop()


if __name__ == "__main__": start()
