from tkinter import *
from PIL import Image, ImageTk
# если здесь красным подчеркивается даже после установки библиотек, замените PIL на pillow,
# наведите курсор на подчеркнутое красным и выберете подсказку установить библиотеку,
# и когда установится, то обратно замените pillow на PIL
from PIL.Image import Resampling




# Размеры элементов в пикселях
map_width = 900
map_height = 583
node_radius = 5
edge_min_width = 1
edge_max_width = 10


# Цвета
node_color = "red"
edge_color = "blue"
goods_color = "brown"
ship_color = "gray"
icebreaker_color = "black"


# здесь координаты узлов
nodes = [(200, 300), (400, 450), (800, 200), (730, 500), (530, 400)]

# ребра между узлами из списка выше
edges = [(0, 4), (0, 1), (0, 4), (1, 2), (3, 4), (0, 2)]
# ширина ребер
edges_width = [1, 4, 6, 2, 9, 5]


root = Tk()
root.title("СМП путь")
root.geometry("900x630+400+60")


canvas = Canvas(root, width = 900, height = 583)
canvas.place(x=0, y=0)

photo = Image.open("map_img.png")
resized = photo.resize((900, 583), Resampling.LANCZOS)
resized_photo = ImageTk.PhotoImage(resized)

canvas.create_image(0,0, image=resized_photo, anchor='nw')


counter = 0
count_label = Label(root, text=f"{counter}", pady=5)
count_label.place(x=55, y=590)


button_minus = Button(root, text="   -   ", pady=5, command=lambda: count_label.config(text=f"{counter}"))
button_minus.place(x=10, y=590)


button_plus = Button(root, text="   +   ", pady=5)
button_plus.place(x=80, y=590)




def draw_node(x, y, color = node_color):
    return canvas.create_oval(x - node_radius, y - node_radius,
                              x + node_radius, y + node_radius,
                              outline=color, fill=color)

def draw_edge(node_a, node_b, width, color=edge_color):
    return canvas.create_line(node_a[0], node_a[1], node_b[0], node_b[1], width=width, fill=color)


def update():
    root.update_idletasks()
    root.update()

def draw_nodes(nodes):
    for node in nodes:
        draw_node(node[0], node[1])


def draw_edges(edges, nodes, width):
    for i in range(len(edges)):
        draw_edge(nodes[edges[i][0]], nodes[edges[i][1]], width[i])



if __name__ == '__main__':
    draw_edges(edges, nodes, edges_width)
    draw_nodes(nodes)
    update()
    root.mainloop()

