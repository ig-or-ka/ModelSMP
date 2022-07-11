from tkinter import *
from PIL import Image, ImageTk
# если здесь красным подчеркивается даже после установки библиотек, замените PIL на pillow,
# наведите курсор на подчеркнутое красным и выберете подсказку установить библиотеку,
# и когда установится, то обратно замените pillow на PIL
from PIL.Image import Resampling
from tkinter import ttk
from threading import Thread
import Classes


class Application:
    # Размеры элементов в пикселях
    map_width = 900
    map_height = 583
    window_width = map_width + 3
    window_height = 630
    element_pad = 10
    node_radius = 5
    goods_radius = 3
    edge_min_width = 1
    edge_max_width = 10

    # Цвета
    node_color = "red"
    edge_sea_color = "blue"
    edge_train_color = "green"
    edge_pipe_color = "orange"
    edge_loading_color = "gray"
    goods_color = "brown"
    ship_color = "gray"
    icebreaker_color = "black"

    # кол-во ледоколов
    counter = 0

    def __init__(self):
        self.window = Tk()

        # self.window.bind('<Motion>', callback)
        self.window.bind('<Button-1>', click)

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
        self.good = None

        self.list_goods = ttk.Combobox(self.window, values=[1, 2, 3, 4, 5])
        self.list_goods.place(x=150,
                              y=self.map_height + self.element_pad)  # self.button_plus.winfo_rootx() + self.button_plus.winfo_width() + self.element_pad
        self.list_goods.current(0)

        # Отрисовываем граф
        # рисуем сначала ребра, чтобы потом узлы отрисовывались поверх
        self.draw_edges()
        self.draw_nodes()

    def add_ship(self, ship):
        self.ships.append(ship)

    def add_icebreaker(self):
        self.counter += 1
        self.count_label.config(text=f"{self.counter}")

    def remove_icebreaker(self):
        if self.counter > 0:
            self.counter -= 1
            self.count_label.config(text=f"{self.counter}")

    def draw_goods(self, edge, percent):  # тут возможно еще надо передавать сам груз, какую то инфу о нем, чтоб я добавлял его в список. пока я просто его айди передаю
        node_a:Classes.node = Classes.indexes.node[edge.id_begin_node]
        node_b:Classes.node = Classes.indexes.node[edge.id_end_node]

        percent /= 100
        x = node_a.coordinate_X + (node_b.coordinate_X - node_a.coordinate_X) * percent
        y = node_a.coordinate_Y + (node_b.coordinate_Y - node_a.coordinate_Y) * percent

        oval = self.canvas.create_oval(x - self.goods_radius, y - self.goods_radius,
                                       x + self.goods_radius, y + self.goods_radius,
                                       outline=self.goods_color, fill=self.goods_color)
        if self.good != None:
            self.canvas.delete(self.good)
        self.good = oval

    def remove_goods(self):
        if self.good != None:
            self.canvas.delete(self.good)
            self.good = None

    def draw_ship(self):
        pass

    def draw_icebreaker(self):
        pass

    def get_ships(self):
        return self.ships

    def get_icebreakers(self):
        return self.icebreakers

    def draw_node(self, x, y, color=node_color):
        return self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                       x + self.node_radius, y + self.node_radius,
                                       outline=color, fill=color)

    def draw_edge(self, node_a:Classes.node, node_b:Classes.node, width, edge_type="sea"):
        color = {
            "sea": self.edge_sea_color,
            "train": self.edge_train_color,
            "pipe": self.edge_pipe_color,
            "loading": self.edge_loading_color
        }

        return self.canvas.create_line(node_a.coordinate_X, node_a.coordinate_Y, node_b.coordinate_X, node_b.coordinate_Y, width=width, fill=color[edge_type])

    def redraw_edge(self, edge): #width от 1 до 10 можешь отправлять
        self.canvas.delete(self.drawn_edges[edge.edge_id])
        node_a: Classes.node = Classes.indexes.node[edge.id_begin_node]
        node_b: Classes.node = Classes.indexes.node[edge.id_end_node]
        self.drawn_edges[edge.edge_id] = self.draw_edge(node_a, node_b, edge.edge_width, edge.edge_type)


    def draw_nodes(self):
        for node_id in Classes.indexes.node:
            node: Classes.node = Classes.indexes.node[node_id]
            self.draw_node(node.coordinate_X, node.coordinate_Y)
        self.update()


    drawn_edges = dict()

    def draw_edges(self):
        for edge_id in Classes.indexes.edges:
            edge: Classes.edges = Classes.indexes.edges[edge_id]
            node_a: Classes.node = Classes.indexes.node[edge.id_begin_node]
            node_b: Classes.node = Classes.indexes.node[edge.id_end_node]
            self.drawn_edges[edge_id] = self.draw_edge(node_a, node_b, edge.edge_width, edge.edge_type)
        self.update()

    def update(self):
        self.window.update_idletasks()
        self.window.update()

    def end_drawing(self):
        self.window.mainloop()


def callback(e):
    x = e.x
    y = e.y
    print("Pointer is currently at %d, %d" % (x, y))


def click(e):
    x = e.x
    y = e.y
    print("Pointer is currently at %d, %d" % (x, y))

class GUI:
    selected_cargo: Classes.consignment = None
    work = False
    app: Application = None
    @classmethod
    def gui_th(cls):
        cls.app = Application()
        cls.app.end_drawing()
        cls.work = False
    @classmethod
    def start(cls):
        cls.work = True
        Thread(target=cls.gui_th).start()

# запускать тут (для теста)
if __name__ == '__main__':
    Classes.full_info()
    Classes.preparing()
    app = Application()    
    """
    # тут пример просто, груз пробегает от 13 до 14 узла, но без пауз, так что почти незаметно
    for i in range(0, 100):
        app.draw_goods(edges(incident_nodes="13_14"), i / 100, 0)
    """

    app.end_drawing()