from tkinter import *
from PIL import Image, ImageTk
# если здесь красным подчеркивается даже после установки библиотек, замените PIL на pillow,
# наведите курсор на подчеркнутое красным и выберете подсказку установить библиотеку,
# и когда установится, то обратно замените pillow на PIL
from PIL.Image import Resampling
from tkinter import ttk


def callback(e):
    x = e.x
    y = e.y
    print("Pointer is currently at %d, %d" % (x, y))


class Application:
    # Размеры элементов в пикселях
    map_width = 900
    map_height = 583
    window_width = map_width + 3
    window_height = 630
    element_pad = 10
    node_radius = 5
    edge_min_width = 1
    edge_max_width = 10

    # Цвета
    node_color = "red"
    edge_color = "blue"
    goods_color = "brown"
    ship_color = "gray"
    icebreaker_color = "black"

    # кол-во ледоколов
    counter = 0

    def __init__(self):
        self.window = Tk()

        # self.window.bind('<Motion>', callback)
        self.window.title("СМП путь")
        self.window.geometry(f"{self.window_width}x{self.window_height}+400+60")

        self.canvas = Canvas(self.window, width=self.map_width, height=self.map_height)
        self.canvas.place(x=0, y=0)

        photo = Image.open("map_img.png")
        resized = photo.resize((self.map_width, self.map_height), Resampling.LANCZOS)
        self.resized_photo = ImageTk.PhotoImage(resized)

        self.canvas.create_image(0, 0, image=self.resized_photo, anchor='nw')
        self.update()

        self.count_label = Label(self.window, text=f"{self.counter}", pady=5)
        self.count_label.place(x=55, y=self.map_height + self.element_pad)

        self.button_minus = Button(self.window, text="   -   ", pady=5, command=lambda: self.remove_icebreaker())
        self.button_minus.place(x=10, y=self.map_height + self.element_pad)

        self.button_plus = Button(self.window, text="   +   ", pady=5, command=lambda: self.add_icebreaker())
        self.button_plus.place(x=80, y=self.map_height + self.element_pad)

        self.ships = []
        self.icebreakers = []
        self.goods = []

        self.list_goods = ttk.Combobox(self.window, values=[1, 2, 3, 4, 5])
        self.list_goods.place(x=150, y=self.map_height + self.element_pad)  #self.button_plus.winfo_rootx() + self.button_plus.winfo_width() + self.element_pad
        self.list_goods.current(0)

    def add_goods(self, goods):
        self.goods.append(goods)

    def add_ship(self, ship):
        self.ships.append(ship)

    def add_icebreaker(self):
        self.counter += 1
        self.count_label.config(text=f"{self.counter}")

    def remove_icebreaker(self):
        if self.counter > 0:
            self.counter -= 1
            self.count_label.config(text=f"{self.counter}")

    def draw_goods(self):
        pass

    def draw_ship(self):
        pass

    def draw_icebreaker(self):
        pass

    def get_goods(self):
        return self.goods

    def get_ships(self):
        return self.ships

    def get_icebreakers(self):
        return self.icebreakers

    def draw_node(self, x, y, color=node_color):
        return self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                       x + self.node_radius, y + self.node_radius,
                                       outline=color, fill=color)

    def draw_edge(self, node_a, node_b, width, color=edge_color):
        return self.canvas.create_line(node_a[0], node_a[1], node_b[0], node_b[1], width=width, fill=color)

    def draw_nodes(self, nodes):
        for node in nodes:
            self.draw_node(node[0], node[1])
        self.update()

    def draw_edges(self, edges, nodes, width):
        for i in range(len(edges)):
            self.draw_edge(nodes[edges[i][0]], nodes[edges[i][1]], width[i])
        self.update()

    def update(self):
        self.window.update_idletasks()
        self.window.update()

    def end_drawing(self):
        self.window.mainloop()


# запускать тут (для теста)
if __name__ == '__main__':
    # здесь координаты узлов
    nodes = [(235, 207), (275, 239), (261, 252), (250, 261), (233, 233), (299, 219), (321, 217),
             (339, 203), (378, 194), (410, 163), (412, 201), (426, 224), (500, 164), (585, 185),
             (739, 207), (774, 212), (800, 257), (778, 241), (773, 263), (700, 334), (596, 392)]

    # ребра между узлами из списка выше
    edges = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (0, 5), (1, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),
             (9, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (16, 18), (17, 18), (16, 19), (17, 19), (18, 19), (19, 20)]
    # ширина ребер
    edges_width = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    app = Application()

    # рисуем сначала ребра, чтобы потом узлы отрисовывались поверх
    app.draw_edges(edges, nodes, edges_width)
    app.draw_nodes(nodes)

    app.end_drawing()
