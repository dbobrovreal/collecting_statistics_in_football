import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from tour import request_to_receive_a_tour_id


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.directory = None
        self.filename_open = None
        self.title("Football data")
        self.geometry("500x400")

        group_file_open = tk.LabelFrame(self, padx=15, pady=10, text="Файл с данными игры")
        group_file_open.pack(padx=10, pady=5)

        btn_file = tk.Button(group_file_open, text="Выбрать файл", command=self.choose_file)
        btn_file.grid(row=0, padx=10, pady=5)

        self.open_file = tk.Text(group_file_open, height=1, width=30)
        self.open_file.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        group_file_save = tk.LabelFrame(self, padx=15, pady=10, text="Сохранить результат в папку")
        group_file_save.pack(padx=10, pady=5)

        btn_file_save = tk.Button(group_file_save, text="Обзор", command=self.save_file)
        btn_file_save.grid(row=0, padx=10, pady=5)

        self.path_to_folder = tk.Text(group_file_save, height=1, width=30)
        self.path_to_folder.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        group_tour = tk.LabelFrame(self, padx=15, pady=10, text="Туры")
        group_tour.pack(padx=10, pady=5)

        self.combo = ttk.Combobox(group_tour, values=[f"{tour_number}" for tour_number in range(1, 39)])
        self.combo.current(0)
        self.combo.grid(row=0, padx=10, pady=5)

        self.button = ttk.Button(self, text="Получить данные", command=self.on_button_click)
        self.button.pack()

    def choose_file(self):
        filetypes = ((".xlsx", "*.xlsx"), ("*", "*"))
        self.filename_open = filedialog.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        self.open_file.delete("1.0", "end")
        self.open_file.insert(tk.END, self.filename_open)

    def save_file(self):
        self.directory = filedialog.askdirectory(title="Открыть папку", initialdir="/")
        self.path_to_folder.delete("1.0", "end")
        self.path_to_folder.insert(tk.END, self.directory)

    def on_button_click(self):
        if not self.open_file.get("1.0", "end"):
            showerror(title="Error", message="Вы не указали файл с игроками")
        elif not self.path_to_folder.get("1.0", "end"):
            showerror(title="Error", message="Вы не указали папку куда сохранить")
        else:
            path = self.open_file.get("1.0", "end").replace('/', '\\').rstrip()
            path_dir = self.path_to_folder.get("1.0", "end").replace('/', '\\').rstrip()

            if not os.path.exists(path):
                showerror(title="Error", message="Не верно указан путь до файла")
            elif not os.path.isdir(path_dir):
                showerror(title="Error", message="Не верно указан путь до папки")

            else:
                selected_item = self.combo.get()
                responses_app = {
                    "file_path": path,
                    "path_dir_save": path_dir,
                    "num_tour": selected_item
                }

                with open('responses.json', 'w', encoding='utf-8') as file:
                    json.dump(responses_app, file, indent=4, ensure_ascii=False)

                request_to_receive_a_tour_id()
                showinfo(message='Успешно')


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
