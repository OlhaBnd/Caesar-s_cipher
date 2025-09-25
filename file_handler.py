import os
from tkinter import filedialog, messagebox


class FileHandler:
    def __init__(self, text_widget=None):
        self.text_widget = text_widget
        self.current_file = None

    def set_text_widget(self, text_widget):
        """Встановити текстову область після ініціалізації"""
        self.text_widget = text_widget

    def new_file(self):
        """Створення нового файлу"""
        if self.text_widget:
            self.text_widget.delete(1.0, "end")
            self.current_file = None

    def open_file(self):
        """Відкриття файлу"""
        if not self.text_widget:
            messagebox.showerror("Помилка", "Текстова область не ініціалізована")
            return

        file_path = filedialog.askopenfilename(
            title="Відкрити файл",
            filetypes=[("Текстові файли", "*.txt"), ("Всі файли", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_widget.delete(1.0, "end")
                    self.text_widget.insert(1.0, content)
                    self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл: {str(e)}")

    def save_file(self):
        """Збереження файлу"""
        if not self.text_widget:
            messagebox.showerror("Помилка", "Текстова область не ініціалізована")
            return

        if self.current_file:
            try:
                content = self.text_widget.get(1.0, "end-1c")
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Успіх", "Файл успішно збережено")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """Збереження файлу як..."""
        if not self.text_widget:
            messagebox.showerror("Помилка", "Текстова область не ініціалізована")
            return

        file_path = filedialog.asksaveasfilename(
            title="Зберегти файл як",
            defaultextension=".txt",
            filetypes=[("Текстові файли", "*.txt"), ("Всі файли", "*.*")]
        )

        if file_path:
            try:
                content = self.text_widget.get(1.0, "end-1c")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = file_path
                messagebox.showinfo("Успіх", "Файл успішно збережено")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {str(e)}")

    def print_file(self):
        """Друк файлу (симуляція)"""
        if not self.text_widget:
            messagebox.showerror("Помилка", "Текстова область не ініціалізована")
            return

        content = self.text_widget.get(1.0, "end-1c")
        if content:
            messagebox.showinfo("Друк", "Функція друку симульована. Вміст буде виведено в консоль.")
            print("=== Друк вмісту ===")
            print(content)
            print("===================")
        else:
            messagebox.showwarning("Попередження", "Немає вмісту для друку")