import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from tour import request_to_receive_a_tour_id


class MainWindow(tk.Tk):
    """
    Класс MainWindow создает оконное приложение с помощью модуля tkinder. Наследуется от tkinder.TK

    :methods choose_file - Метод запускается, когда нажать кнопку `Открыть файл` в оконном приложение.
                           Задача этого метода указать путь к excel файлу, где указаны собранные команды игроков

    :methods save_file - Метод запускается, когда нажать кнопку `Обзор` в оконном приложение.
                         Задача этого метода указать путь куда сохранить excel файл с результатом
                         работы программы

    :methods on_button_click - Метод класса запускается, когда нажать кнопку `Получить данные` в оконном приложение.
                               Задача этого метода запустить основную логику приложение.
    """
    def __init__(self) -> None:
        super().__init__()
        self.directory: None = None
        self.filename_open: None = None
        self.title("Football data")
        self.geometry("500x400")

        group_file_open: LabelFrame = tk.LabelFrame(self, padx=15, pady=10, text="Файл с данными игры")
        group_file_open.pack(padx=10, pady=5)

        btn_file: Button = tk.Button(group_file_open, text="Выбрать файл", command=self.choose_file)
        btn_file.grid(row=0, padx=10, pady=5)

        self.open_file: Text = tk.Text(group_file_open, height=1, width=30)
        self.open_file.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        group_file_save: LabelFrame = tk.LabelFrame(self, padx=15, pady=10, text="Сохранить результат в папку")
        group_file_save.pack(padx=10, pady=5)

        btn_file_save: Button = tk.Button(group_file_save, text="Обзор", command=self.save_file)
        btn_file_save.grid(row=0, padx=10, pady=5)

        self.path_to_folder: Text = tk.Text(group_file_save, height=1, width=30)
        self.path_to_folder.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        group_tour: LabelFrame = tk.LabelFrame(self, padx=15, pady=10, text="Туры")
        group_tour.pack(padx=10, pady=5)

        self.combo: Combobox = ttk.Combobox(group_tour, values=[f"{tour_number}" for tour_number in range(1, 39)])
        self.combo.current(0)
        self.combo.grid(row=0, padx=10, pady=5)

        self.button: Button = ttk.Button(self, text="Получить данные", command=self.on_button_click)
        self.button.pack()

    def choose_file(self) -> None:
        """
        Метод класса запускается, когда нажать кнопку `Открыть файл` в оконном приложение.
        Задача этого метода указать путь к excel файлу, где указаны собранные команды игроков.
        :return: None
        """
        filetypes: tuple[tuple[str, str], tuple[str, str]] = ((".xlsx", "*.xlsx"), ("*", "*"))
        self.filename_open: str = filedialog.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        self.open_file.delete("1.0", "end")
        self.open_file.insert(tk.END, self.filename_open)

    def save_file(self) -> None:
        """
        Метод класса запускается, когда нажать кнопку `Обзор` в оконном приложение.
        Задача этого метода указать путь куда сохранить excel файл с результатом
        работы программы
        :return: None
        """
        self.directory: str = filedialog.askdirectory(title="Открыть папку", initialdir="/")
        self.path_to_folder.delete("1.0", "end")
        self.path_to_folder.insert(tk.END, self.directory)

    def on_button_click(self) -> None:
        """
        Метод класса запускается, когда нажать кнопку `Получить данные` в оконном приложение.
        Задача этого метода запустить основную логику приложение.
        :return: None
        """
        if not self.open_file.get("1.0", "end"):
            showerror(title="Error", message="Вы не указали файл с игроками")
        elif not self.path_to_folder.get("1.0", "end"):
            showerror(title="Error", message="Вы не указали папку куда сохранить")
        else:
            path: str = self.open_file.get("1.0", "end").replace('/', '\\').rstrip()
            path_dir: str = self.path_to_folder.get("1.0", "end").replace('/', '\\').rstrip()

            if not os.path.exists(path):
                showerror(title="Error", message="Не верно указан путь до файла")
            elif not os.path.isdir(path_dir):
                showerror(title="Error", message="Не верно указан путь до папки")

            else:
                selected_item: str = self.combo.get()
                responses_app = {
                    "file_path": path,
                    "path_dir_save": path_dir,
                    "num_tour": selected_item
                }

                with open('responses.json', 'w', encoding='utf-8') as file:
                    json.dump(responses_app, file, indent=4, ensure_ascii=False)

                flag: bool = request_to_receive_a_tour_id()

                if not flag:
                    showerror(message='Этот тур еще не начался')
                else:
                    showinfo(message='Успешно')

                if os.path.exists('responses.json'):
                    os.remove('responses.json')


if __name__ == '__main__':
    app: MainWindow = MainWindow()
    app.mainloop()
