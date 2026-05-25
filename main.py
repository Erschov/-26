import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.filename = 'weather_data.json'
        self.data = self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.precip_var).grid(row=3, column=1)

        # Кнопки
        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Фильтры
        tk.Label(root, text="Фильтр (Мин. темп):").grid(row=5, column=0)
        self.filter_temp = tk.Entry(root)
        self.filter_temp.grid(row=5, column=1)
        tk.Button(root, text="Применить фильтр", command=self.update_table).grid(row=6, column=0, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Темп", "Описание", "Осадки"), show='headings')
        for col in ("Дата", "Темп", "Описание", "Осадки"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=7, column=0, columnspan=2, pady=10)

        self.update_table()

    def validate(self):
        # Простая валидация
        if not self.date_entry.get() or "." not in self.date_entry.get():
            return "Неверный формат даты."
        try:
            float(self.temp_entry.get())
        except ValueError:
            return "Температура должна быть числом."
        if not self.desc_entry.get():
            return "Описание не может быть пустым."
        return None

    def add_entry(self):
        error = self.validate()
        if error:
            messagebox.showerror("Ошибка", error)
            return

        new_entry = {
            "date": self.date_entry.get(),
            "temp": float(self.temp_entry.get()),
            "desc": self.desc_entry.get(),
            "precip": "Да" if self.precip_var.get() else "Нет"
        }
        self.data.append(new_entry)
        self.save_data()
        self.update_table()
        messagebox.showinfo("Успех", "Запись добавлена!")

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        min_temp = self.filter_temp.get()
        
        for entry in self.data:
            if min_temp:
                try:
                    if entry['temp'] < float(min_temp): continue
                except: pass
            
            self.tree.insert("", "end", values=(entry['date'], entry['temp'], entry['desc'], entry['precip']))

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
