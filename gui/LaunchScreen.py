from tkinter import *
from PIL import Image, ImageTk
# если здесь красным подчеркивается даже после установки библиотек, замените PIL на pillow,
# наведите курсор на подчеркнутое красным и выберете подсказку установить библиотеку,
# и когда установится, то обратно замените pillow на PIL
from PIL.Image import Resampling

root = Tk()
root.title("СМП путь")
root.geometry("900x630+400+60")


canvas = Canvas(root, width = 900, height = 583)
canvas.place(x=0, y=0)

photo = Image.open("map_img.png")
resized = photo.resize((900, 583), Resampling.LANCZOS)
resized_photo = ImageTk.PhotoImage(resized)
# map_ph = Label(root, image=resized_photo, width=900, height=583)
# map_ph.place(x=0, y=0)

canvas.create_image(0,0, image=resized_photo, anchor='nw')


counter = 0
count_label = Label(root, text=f"{counter}", pady=5)
count_label.place(x=55, y=590)


button_minus = Button(root, text="   -   ", pady=5, command=lambda: count_label.config(text=f"{counter}"))
button_minus.place(x=10, y=590)


button_plus = Button(root, text="   +   ", pady=5)
button_plus.place(x=80, y=590)




def circle(center_x, center_y, radius, color = "black", fill = "black"):
    return canvas.create_oval(center_x - radius, center_y - radius,
                              center_x + radius, center_y + radius,
                              outline=color, fill = fill)

def point(x, y, color = "black"):
    return circle(x, y, 100, color, color)


def update():
    root.update_idletasks()
    root.update()


if __name__ == '__main__':
    root.mainloop()
    point(200, 300)
    update()

