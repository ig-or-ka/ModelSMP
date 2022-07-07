from tkinter import *
from PIL import Image, ImageTk



root = Tk()
canvas = Canvas(root, width = 900, height = 630)
root.title("СМП путь")
root.geometry("900x630+400+60")
canvas.pack()


photo = Image.open("map_img.png")
resized = photo.resize((900, 583), Image.ANTIALIAS)
resized_photo = ImageTk.PhotoImage(resized)
map_ph = Label(root, image=resized_photo, width=895, height=583)
map_ph.grid(row=0, column=0, columnspan=3)


counter = 0
count_label = Label(root, text=f"{counter}", pady=5)
count_label.grid(row=1, column=1)


button_minus = Button(root, text="   -   ", pady=5, command=lambda: count_label.config(text=f"{counter}"))
button_minus.grid(row=1, column=0)


button_plus = Button(root, text="   +   ", pady=5)
button_plus.grid(row=1, column=2)




def circle(center_x, center_y, radius, color = "rad", fill = "rad"):
    return canvas.create_oval(center_x - radius, center_y - radius,
                              center_x + radius, center_y + radius,
                              outline=color, fill = fill)

def point(x, y, color = "rad"):
    return circle(x, y, 10, color, color)


if __name__ == '__main__':
    root.mainloop()
    point(200, 300)

