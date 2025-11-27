import customtkinter as ctk
from tkinter import messagebox
from cipher import CaesarCipher, TrithemiusCipher, BookCipher
from file_handler import FileHandler

class CryptoApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Криптосистема")
        self.root.geometry("900x650")

        self.caesar_cipher = CaesarCipher()
        self.trit_cipher = TrithemiusCipher()
        self.book_cipher = BookCipher()
        self.file_handler = FileHandler()

        self.setup_ui()
        self.file_handler.set_text_widget(self.text_area)

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Панель файлів
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=5)
        ctk.CTkButton(file_frame, text="Новий", command=self.file_handler.new_file).pack(side="left", padx=3)
        ctk.CTkButton(file_frame, text="Відкрити", command=self.file_handler.open_file).pack(side="left", padx=3)
        ctk.CTkButton(file_frame, text="Зберегти", command=self.file_handler.save_file).pack(side="left", padx=3)
        ctk.CTkButton(file_frame, text="Зберегти як", command=self.file_handler.save_as_file).pack(side="left", padx=3)
        ctk.CTkButton(file_frame, text="Друк", command=self.file_handler.print_file).pack(side="left", padx=3)

        # Панель шифрів
        cipher_frame = ctk.CTkFrame(main_frame)
        cipher_frame.pack(fill="x", pady=5)

        # Вибір шифру
        ctk.CTkLabel(cipher_frame, text="Шифр:").pack(side="left", padx=5)
        self.cipher_var = ctk.StringVar(value="caesar")
        ctk.CTkOptionMenu(cipher_frame, values=["caesar", "trithemius", "book"], variable=self.cipher_var).pack(side="left", padx=5)

        # Вибір мови
        ctk.CTkLabel(cipher_frame, text="Мова:").pack(side="left", padx=5)
        self.language_var = ctk.StringVar(value="ukrainian")
        ctk.CTkRadioButton(cipher_frame, text="Українська", variable=self.language_var, value="ukrainian").pack(side="left")
        ctk.CTkRadioButton(cipher_frame, text="Англійська", variable=self.language_var, value="english").pack(side="left")

        # Ключ
        ctk.CTkLabel(cipher_frame, text="Ключ / Вірш:").pack(side="left", padx=5)
        self.key_entry = ctk.CTkEntry(cipher_frame, width=200)
        self.key_entry.pack(side="left", padx=5)

        # Тип ключа для Тритеміуса
        ctk.CTkLabel(cipher_frame, text="Тип ключа:").pack(side="left", padx=5)
        self.trit_key_type_var = ctk.StringVar(value="linear")
        ctk.CTkOptionMenu(cipher_frame, values=["linear", "nonlinear", "password"], variable=self.trit_key_type_var).pack(side="left", padx=5)

        # Панель дій
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", pady=5)
        ctk.CTkButton(action_frame, text="Зашифрувати", command=self.encrypt_text).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Розшифрувати", command=self.decrypt_text).pack(side="left", padx=5)

        # Текстова область
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=5)
        self.text_area = ctk.CTkTextbox(text_frame, wrap="word")
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

    def encrypt_text(self):
        cipher_type = self.cipher_var.get()
        language = self.language_var.get()
        key_text = self.key_entry.get()
        text = self.text_area.get(1.0, "end-1c")

        if cipher_type == "caesar":
            is_valid, key = self.caesar_cipher.validate_key(key_text, language)
            if not is_valid:
                messagebox.showerror("Помилка", key)
                return
            encrypted = self.caesar_cipher.encrypt(text, key, language)
        elif cipher_type == "trithemius":
            trit_type = self.trit_key_type_var.get()
            key_values = key_text.split(",") if trit_type != "password" else key_text
            is_valid, key = self.trit_cipher.validate_key(trit_type, key_values, language)
            if not is_valid:
                messagebox.showerror("Помилка", key)
                return
            encrypted = self.trit_cipher.encrypt(text, trit_type, key, language)
        elif cipher_type == "book":
            encrypted = self.book_cipher.encrypt(text, key_text)
        else:
            messagebox.showerror("Помилка", "Невідомий шифр")
            return

        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, encrypted)
        messagebox.showinfo("Успіх", "Текст зашифровано")

    def decrypt_text(self):
        cipher_type = self.cipher_var.get()
        language = self.language_var.get()
        key_text = self.key_entry.get()
        text = self.text_area.get(1.0, "end-1c")

        if cipher_type == "caesar":
            is_valid, key = self.caesar_cipher.validate_key(key_text, language)
            if not is_valid:
                messagebox.showerror("Помилка", key)
                return
            decrypted = self.caesar_cipher.decrypt(text, key, language)
        elif cipher_type == "trithemius":
            trit_type = self.trit_key_type_var.get()
            key_values = key_text.split(",") if trit_type != "password" else key_text
            is_valid, key = self.trit_cipher.validate_key(trit_type, key_values, language)
            if not is_valid:
                messagebox.showerror("Помилка", key)
                return
            decrypted = self.trit_cipher.decrypt(text, trit_type, key, language)
        elif cipher_type == "book":
            decrypted = self.book_cipher.decrypt(text, key_text)
        else:
            messagebox.showerror("Помилка", "Невідомий шифр")
            return

        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, decrypted)
        messagebox.showinfo("Успіх", "Текст розшифровано")

    def run(self):
        self.root.mainloop()
