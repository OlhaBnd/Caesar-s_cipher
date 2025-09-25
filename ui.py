import customtkinter as ctk
from tkinter import messagebox
from cipher import CaesarCipher
from file_handler import FileHandler


class CryptoApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Криптосистема Цезаря")
        self.root.geometry("800x600")

        # Ініціалізація компонентів
        self.cipher = CaesarCipher()
        self.file_handler = FileHandler()  # Спочатку без текстової області

        self.setup_ui()

        # Тепер встановлюємо текстову область для file_handler
        self.file_handler.set_text_widget(self.text_area)

    def setup_ui(self):
        """Налаштування графічного інтерфейсу"""
        # Налаштування теми
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Створення меню
        self.create_menu()

        # Створення основного фрейму
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Панель інструментів
        toolbar = ctk.CTkFrame(main_frame)
        toolbar.pack(fill="x", padx=5, pady=5)

        # Кнопки панелі інструментів
        ctk.CTkButton(toolbar, text="Новий", command=self.file_handler.new_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Відкрити", command=self.file_handler.open_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Зберегти", command=self.file_handler.save_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Зберегти як", command=self.file_handler.save_as_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Друк", command=self.file_handler.print_file).pack(side="left", padx=2)

        # Розділювач
        ctk.CTkLabel(toolbar, text="|").pack(side="left", padx=5)

        ctk.CTkButton(toolbar, text="Зашифрувати", command=self.encrypt_text).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Розшифрувати", command=self.decrypt_text).pack(side="left", padx=2)

        # Панель налаштувань
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(settings_frame, text="Ключ:").pack(side="left", padx=5)
        self.key_entry = ctk.CTkEntry(settings_frame, width=50)
        self.key_entry.pack(side="left", padx=5)
        self.key_entry.insert(0, "3")

        ctk.CTkLabel(settings_frame, text="Мова:").pack(side="left", padx=5)
        self.language_var = ctk.StringVar(value="ukrainian")
        ctk.CTkRadioButton(settings_frame, text="Українська", variable=self.language_var, value="ukrainian").pack(
            side="left", padx=5)
        ctk.CTkRadioButton(settings_frame, text="Англійська", variable=self.language_var, value="english").pack(
            side="left", padx=5)

        # Текстова область
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.text_area = ctk.CTkTextbox(text_frame, wrap="word")
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

    # ... решта методів залишається без змін ...
    def create_menu(self):
        """Створення меню"""
        menu_bar = ctk.CTkFrame(self.root, height=30)
        menu_bar.pack(fill="x")

        # Меню Файл
        file_menu_btn = ctk.CTkButton(menu_bar, text="Файл", width=60, command=self.show_file_menu)
        file_menu_btn.pack(side="left", padx=2)

        # Меню Шифрування
        crypto_menu_btn = ctk.CTkButton(menu_bar, text="Шифрування", width=100, command=self.show_crypto_menu)
        crypto_menu_btn.pack(side="left", padx=2)

        # Меню Довідка
        help_menu_btn = ctk.CTkButton(menu_bar, text="Довідка", width=80, command=self.show_help_menu)
        help_menu_btn.pack(side="left", padx=2)

    def show_file_menu(self):
        """Показати меню файлу"""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Файл")
        menu.geometry("200x150")
        menu.transient(self.root)
        menu.grab_set()

        ctk.CTkButton(menu, text="Новий", command=lambda: [self.file_handler.new_file(), menu.destroy()]).pack(pady=5)
        ctk.CTkButton(menu, text="Відкрити", command=lambda: [self.file_handler.open_file(), menu.destroy()]).pack(
            pady=5)
        ctk.CTkButton(menu, text="Зберегти", command=lambda: [self.file_handler.save_file(), menu.destroy()]).pack(
            pady=5)
        ctk.CTkButton(menu, text="Зберегти як",
                      command=lambda: [self.file_handler.save_as_file(), menu.destroy()]).pack(pady=5)
        ctk.CTkButton(menu, text="Друк", command=lambda: [self.file_handler.print_file(), menu.destroy()]).pack(pady=5)
        ctk.CTkButton(menu, text="Вихід", command=self.root.quit).pack(pady=5)

    def show_crypto_menu(self):
        """Показати меню шифрування"""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Шифрування")
        menu.geometry("200x100")
        menu.transient(self.root)
        menu.grab_set()

        ctk.CTkButton(menu, text="Зашифрувати", command=lambda: [self.encrypt_text(), menu.destroy()]).pack(pady=5)
        ctk.CTkButton(menu, text="Розшифрувати", command=lambda: [self.decrypt_text(), menu.destroy()]).pack(pady=5)

    def show_help_menu(self):
        """Показати меню довідки"""
        menu = ctk.CTkToplevel(self.root)
        menu.title("Довідка")
        menu.geometry("300x150")
        menu.transient(self.root)
        menu.grab_set()

        ctk.CTkButton(menu, text="Про програму", command=lambda: [self.show_about(), menu.destroy()]).pack(pady=5)
        ctk.CTkButton(menu, text="Про розробника", command=lambda: [self.show_developer_info(), menu.destroy()]).pack(
            pady=5)

    def encrypt_text(self):
        """Шифрування тексту"""
        key = self.key_entry.get()
        language = self.language_var.get()

        # Валідація ключа
        is_valid, result = self.cipher.validate_key(key, language)
        if not is_valid:
            messagebox.showerror("Помилка", result)
            return

        key = result
        text = self.text_area.get(1.0, "end-1c")

        if not text:
            messagebox.showwarning("Попередження", "Введіть текст для шифрування")
            return

        encrypted_text = self.cipher.encrypt(text, key, language)
        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, encrypted_text)
        messagebox.showinfo("Успіх", "Текст успішно зашифровано")

    def decrypt_text(self):
        """Розшифрування тексту"""
        key = self.key_entry.get()
        language = self.language_var.get()

        # Валідація ключа
        is_valid, result = self.cipher.validate_key(key, language)
        if not is_valid:
            messagebox.showerror("Помилка", result)
            return

        key = result
        text = self.text_area.get(1.0, "end-1c")

        if not text:
            messagebox.showwarning("Попередження", "Введіть текст для розшифрування")
            return

        decrypted_text = self.cipher.decrypt(text, key, language)
        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, decrypted_text)
        messagebox.showinfo("Успіх", "Текст успішно розшифровано")

    def show_about(self):
        """Показати інформацію про програму"""
        about_text = """
Криптосистема на основі шифру Цезаря

Ця програма дозволяє шифрувати та розшифровувати тексти 
українською та англійською мовами за допомогою шифру Цезаря.

Шифр Цезаря - це один з найстаріших і найпростіших методів шифрування, 
в якому кожна літера в тексті замінюється на літеру, що знаходиться 
на фіксовану кількість позицій далі в алфавіті.
        """
        messagebox.showinfo("Про програму", about_text)

    def show_developer_info(self):
        """Показати інформацію про розробника"""
        info_text = """
Розробник: Ольга Бунда ТВ-23

Ця програма була розроблена як приклад реалізації 
криптографічної системи на основі шифру Цезаря.

Рік розробки: 2025
        """
        messagebox.showinfo("Про розробника", info_text)

    def run(self):
        """Запуск програми"""
        self.root.mainloop()