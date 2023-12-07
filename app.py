import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, Label, LabelFrame, Button, Text
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Combobox

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
        self.geometry("700x800")

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

        group_coefficients_decisive_action: LabelFrame = tk.LabelFrame(self, padx=15, pady=10,
                                                                       text="Коэфициенты решительных действий")
        group_coefficients_decisive_action.pack(padx=10, pady=5)

        saves: Label = tk.Label(group_coefficients_decisive_action, text='Save')
        saves.grid(row=0, column=0, padx=10, pady=5)

        self.saves_coefficients = tk.Entry(group_coefficients_decisive_action, textvariable=tk.IntVar(self, 1))
        self.saves_coefficients.grid(row=0, column=1, padx=10, pady=5)

        clean_sheets: Label = tk.Label(group_coefficients_decisive_action, text='Clean Sheets')
        clean_sheets.grid(row=0, column=2, padx=10, pady=5)

        self.clean_sheets_coefficients = tk.Entry(group_coefficients_decisive_action, textvariable=tk.IntVar(self, 1))
        self.clean_sheets_coefficients.grid(row=0, column=3, padx=10, pady=5)

        assists: Label = tk.Label(group_coefficients_decisive_action, text='Assists')
        assists.grid(row=1, column=0, padx=10, pady=5)

        self.assists_coefficients = tk.Entry(group_coefficients_decisive_action, textvariable=tk.IntVar(self, 1))
        self.assists_coefficients.grid(row=1, column=1, padx=10, pady=5)

        defensive_actions: Label = tk.Label(group_coefficients_decisive_action, text='Defensive Actions')
        defensive_actions.grid(row=1, column=2, padx=10, pady=5)

        self.defensive_actions_coefficients = tk.Entry(group_coefficients_decisive_action,
                                                       textvariable=tk.IntVar(self, 1))
        self.defensive_actions_coefficients.grid(row=1, column=3, padx=10, pady=5)

        chances_created: Label = tk.Label(group_coefficients_decisive_action, text='Chances Created')
        chances_created.grid(row=2, column=0, padx=10, pady=5)

        self.chances_created_coefficients = tk.Entry(group_coefficients_decisive_action,
                                                     textvariable=tk.IntVar(self, 1))
        self.chances_created_coefficients.grid(row=2, column=1, padx=10, pady=5)

        shots: Label = tk.Label(group_coefficients_decisive_action, text='Shots')
        shots.grid(row=2, column=2, padx=10, pady=5)

        self.shots_coefficients = tk.Entry(group_coefficients_decisive_action, textvariable=tk.IntVar(self, 1))
        self.shots_coefficients.grid(row=2, column=3, padx=10, pady=5)

        goals: Label = tk.Label(group_coefficients_decisive_action, text='Goals')
        goals.grid(row=3, padx=10, pady=5)

        self.goals_coefficients = tk.Entry(group_coefficients_decisive_action, textvariable=tk.IntVar(self, 1))
        self.goals_coefficients.grid(row=3, column=1, padx=10, pady=5)

        group_coefficients_goal: LabelFrame = tk.LabelFrame(self, padx=15, pady=10, text="Коэффициент за гол")
        group_coefficients_goal.pack(padx=10, pady=5)

        self.goals_ratio = tk.Entry(group_coefficients_goal, textvariable=tk.IntVar(self, 1))
        self.goals_ratio.grid(padx=10, pady=5)

        group_coefficients_clean_sheet: LabelFrame = tk.LabelFrame(self, padx=15, pady=10,
                                                                   text="Коэфициент за химию в защите")
        group_coefficients_clean_sheet.pack(padx=10, pady=5)

        for_one = tk.Label(group_coefficients_clean_sheet, text='За 1 совпадение')
        for_one.grid(row=0, column=0, padx=10, pady=5)

        self.coefficients_for_one = tk.Entry(group_coefficients_clean_sheet, textvariable=tk.IntVar(self, 1))
        self.coefficients_for_one.grid(row=0, column=1, padx=10, pady=5)

        in_two = tk.Label(group_coefficients_clean_sheet, text='За 2 совпадения')
        in_two.grid(row=0, column=2, padx=10, pady=5)

        self.coefficients_in_two = tk.Entry(group_coefficients_clean_sheet, textvariable=tk.IntVar(self, 1))
        self.coefficients_in_two.grid(row=0, column=3, padx=10, pady=5)

        for_three = tk.Label(group_coefficients_clean_sheet, text='За 3 совпадения')
        for_three.grid(row=1, column=0, padx=10, pady=5)

        self.coefficients_for_three = tk.Entry(group_coefficients_clean_sheet, textvariable=tk.IntVar(self, 1))
        self.coefficients_for_three.grid(row=1, column=1, padx=10, pady=5)

        for_four = tk.Label(group_coefficients_clean_sheet, text='За 4 совпадения')
        for_four.grid(row=1, column=2, padx=10, pady=5)

        self.coefficients_for_four = tk.Entry(group_coefficients_clean_sheet, textvariable=tk.IntVar(self, 1))
        self.coefficients_for_four.grid(row=1, column=3, padx=10, pady=5)

        group_coefficients_goal_and_assist: LabelFrame = tk.LabelFrame(self, padx=15, pady=10,
                                                                       text="Коэфициент за химию в атаке")
        group_coefficients_goal_and_assist.pack(padx=10, pady=5)

        one_plus = tk.Label(group_coefficients_goal_and_assist, text='За 1 совпадение')
        one_plus.grid(row=0, column=0, padx=10, pady=5)

        self.coefficients_one_plus = tk.Entry(group_coefficients_goal_and_assist, textvariable=tk.IntVar(self, 1))
        self.coefficients_one_plus.grid(row=0, column=1, padx=10, pady=5)

        two_plus = tk.Label(group_coefficients_goal_and_assist, text='За 2 совпадение')
        two_plus.grid(row=0, column=2, padx=10, pady=5)

        self.coefficients_two_plus = tk.Entry(group_coefficients_goal_and_assist, textvariable=tk.IntVar(self, 1))
        self.coefficients_two_plus.grid(row=0, column=3, padx=10, pady=5)

        three_plus = tk.Label(group_coefficients_goal_and_assist, text='За 3 совпадение')
        three_plus.grid(row=1, column=0, padx=10, pady=5)

        self.coefficients_three_plus = tk.Entry(group_coefficients_goal_and_assist, textvariable=tk.IntVar(self, 1))
        self.coefficients_three_plus.grid(row=1, column=1, padx=10, pady=5)

        four_plus = tk.Label(group_coefficients_goal_and_assist, text='За 4 совпадение')
        four_plus.grid(row=1, column=2, padx=10, pady=5)

        self.coefficients_four_plus = tk.Entry(group_coefficients_goal_and_assist, textvariable=tk.IntVar(self, 1))
        self.coefficients_four_plus.grid(row=1, column=3, padx=10, pady=5)

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
                coefficients_decisive_action = {
                    'save': float(self.saves_coefficients.get().replace(',', '.')),
                    'clean_sheets': float(self.clean_sheets_coefficients.get().replace(',', '.')),
                    'assist': float(self.assists_coefficients.get().replace(',', '.')),
                    'defensive_actions': float(self.defensive_actions_coefficients.get().replace(',', '.')),
                    'chances_created': float(self.chances_created_coefficients.get().replace(',', '.')),
                    'shots': float(self.shots_coefficients.get().replace(',', '.')),
                    'goals': float(self.goals_coefficients.get().replace(',', '.'))
                }

                coefficients_goal = float(self.goals_ratio.get().replace(',', '.'))

                coefficients_clean_sheet = {
                    "for_one": float(self.coefficients_for_one.get().replace(',', '.')),
                    'in_two': float(self.coefficients_in_two.get().replace(',', '.')),
                    'for_three': float(self.coefficients_for_three.get().replace(',', '.')),
                    'for_four': float(self.coefficients_for_four.get().replace(',', '.'))
                }

                coefficients_goal_and_assist = {
                    "for_one": float(self.coefficients_one_plus.get().replace(',', '.')),
                    'in_two': float(self.coefficients_two_plus.get().replace(',', '.')),
                    'for_three': float(self.coefficients_three_plus.get().replace(',', '.')),
                    'for_four': float(self.coefficients_four_plus.get().replace(',', '.'))
                }

                responses_app = {
                    "file_path": path,
                    "path_dir_save": path_dir,
                    "num_tour": selected_item,
                    "coefficients_decisive_action": coefficients_decisive_action,
                    "coefficients_goal": coefficients_goal,
                    "coefficients_clean_sheet": coefficients_clean_sheet,
                    "coefficients_goal_and_assist": coefficients_goal_and_assist
                }
                with open('responses.json', 'w', encoding='utf-8') as file:
                    json.dump(responses_app, file, indent=4, ensure_ascii=False)

                flag: bool = request_to_receive_a_tour_id()

                if not flag:
                    showerror(message='Этот тур еще не начался')
                else:
                    showinfo(message='Успешно')


if __name__ == '__main__':
    app: MainWindow = MainWindow()
    app.mainloop()
