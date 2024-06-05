import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont

'''Интерфейс для рисования'''
class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.pen_color = 'black'
        self.pen_color0 = 'black'  # переменная для сохранения цвета
        self.new_color = "white"  # переменная для цвета фона холста

        self.size = [1, 2, 5, 10]       # размеры кисти
        self.brush = tk.IntVar(self.root)
        self.brush.set(self.size[0])

        "Метка для просмотра цвета кисти"
        self.color_lbl = tk.Label(text="Цвет кисти", background="black", foreground="white",
                                  width=9, height=1, font="Arial 10")
        self.color_lbl.pack(anchor='ne')

        self.setup_ui()
        self.brush_size = 1
        self.width = 600
        self.height = 400

        self.last_x, self.last_y = None, None

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<ButtonRelease-3>', self.reset)

        '''Горячие клавиши'''
        self.root.bind('<Control-c>', self.choose_color)
        self.root.bind('<Control-s>', self.save_image)


    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.eraser)
        eraser_button.pack(side=tk.LEFT)

        change_button = tk.Button(control_frame, text="Размер холста", command=self.change_size)
        change_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, text="Текст", command=self.input_text)
        text_button.pack(side=tk.LEFT)

        bgd_button = tk.Button(control_frame, text="Изменить фон", command=self.input_bgd)
        bgd_button.pack(side=tk.LEFT)


        ''' Выбор размера кисти из выпадающего списка'''

        base_lbl = tk.Label(control_frame, text="Размер кисти")
        base_lbl.pack(side=tk.RIGHT)
        my_menu = tk.OptionMenu(self.root, self.brush, *self.size)
        my_menu.pack(side=tk.RIGHT)
        def choose_brush():
            self.brush_size = self.brush.get()
            self.pen_color = self.pen_color0  # возвращаем цвет после ластика
            self.brush_color()

        dr_button = tk.Button(control_frame, text='рисовать', command=choose_brush)
        dr_button.pack(side=tk.LEFT)

    ''' Рисование'''
    def paint(self, event):
        self.brush_size = self.brush.get()
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)
        self.last_x = event.x
        self.last_y = event.y

    ''' Сброс последних координат кисти'''
    def reset(self, event):
        self.last_x, self.last_y = None, None

    ''' Очищение холста'''
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    ''' Выбор цвета кисти'''
    def choose_color(self, *args):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.pen_color0 = self.pen_color  # Сохраняем цвет для использования после ластика
        self.brush_color()

    ''' Сохранить изображение в формате PNG'''
    def save_image(self, *args):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    ''' Ластик'''
    def eraser(self):
        self.brush_size = 10
        self.pen_color = 'white'

    ''' Пипетка для выбора цвета кисти  с холста'''
    def pick_color(self, event):
        self.last_x = event.x
        self.last_y = event.y
        p_color = self.image.getpixel((self.last_x, self.last_y))
        self.pen_color = "#%02x%02x%02x" % p_color  # преобразуем кортеж цвета в 16-й код
        self.pen_color0 = self.pen_color  # Сохраняем цвет для использования после ластика
        self.brush_color()

    ''' Предварительный просмотр цвета кисти'''
    def brush_color(self):
        self.color_lbl.config(bg=self.pen_color)
        self.color_lbl.pack(anchor='ne')

    ''' Изменение размера холста'''
    def change_size(self):
        self.width = tk.simpledialog.askinteger('Input', 'Введите ширину холста')
        self.height = tk.simpledialog.askinteger('Input', 'Введите высоту холста')
        self.canvas.config(width=self.width, height=self.height)
        self.canvas.pack()
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

    ''' Получение текста от пользователя'''
    def input_text(self):
        self.im_text = tk.simpledialog.askstring('Input', 'Введите текст')
        if self.im_text:
            self.canvas.bind('<Button-1>', self.text_img)

    ''' Добавление текста на изображение'''
    def text_img(self, event):
        self.last_x = event.x
        self.last_y = event.y
        font = ImageFont.truetype("arial.ttf", size=40)
        self.canvas.create_text(self.last_x, self.last_y, text=self.im_text,
                                font="Arial 40", fill=self.pen_color)
        self.draw.text([self.last_x, self.last_y], self.im_text, font=font, fill=self.pen_color)
        self.canvas.bind('<Button-1>', self.paint)

    ''' Изменение цвета фона холста'''
    def input_bgd(self):
        self.new_color = colorchooser.askcolor(color=self.new_color)[1]
        self.canvas.config(background=self.new_color)
        self.canvas.pack()


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
