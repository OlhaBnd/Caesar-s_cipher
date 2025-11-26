import customtkinter as ctk
from tkinter import messagebox
from cipher import CaesarCipher, TrithemiusCipher
from file_handler import FileHandler


class CryptoApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Криптосистема")
        self.root.geometry("800x600")

        self.cipher = CaesarCipher()
        self.file_handler = FileHandler()
        self.trit_cipher = TrithemiusCipher()

        self.setup_ui()
        self.file_handler.set_text_widget(self.text_area)

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Панель інструментів
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        toolbar = ctk.CTkFrame(main_frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(toolbar, text="Новий", command=self.file_handler.new_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Відкрити", command=self.file_handler.open_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Зберегти", command=self.file_handler.save_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Зберегти як", command=self.file_handler.save_as_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Друк", command=self.file_handler.print_file).pack(side="left", padx=2)

        ctk.CTkLabel(toolbar, text="|").pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Зашифрувати", command=self.encrypt_text).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Розшифрувати", command=self.decrypt_text).pack(side="left", padx=2)

        # Налаштування
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(settings_frame, text="Ключ:").pack(side="left", padx=5)
        self.key_entry = ctk.CTkEntry(settings_frame, width=80)
        self.key_entry.pack(side="left", padx=5)
        self.key_entry.insert(0, "3")

        ctk.CTkLabel(settings_frame, text="Мова:").pack(side="left", padx=5)
        self.language_var = ctk.StringVar(value="ukrainian")
        ctk.CTkRadioButton(settings_frame, text="Українська", variable=self.language_var, value="ukrainian").pack(side="left")
        ctk.CTkRadioButton(settings_frame, text="Англійська", variable=self.language_var, value="english").pack(side="left")

        ctk.CTkLabel(settings_frame, text="Шифр:").pack(side="left", padx=5)
        self.cipher_type_var = ctk.StringVar(value="caesar")
        ctk.CTkRadioButton(settings_frame, text="Цезар", variable=self.cipher_type_var, value="caesar").pack(side="left")
        ctk.CTkRadioButton(settings_frame, text="Тритеміус", variable=self.cipher_type_var, value="trithemius").pack(side="left")

        ctk.CTkLabel(settings_frame, text="Тип ключа:").pack(side="left", padx=5)
        self.trit_key_type_var = ctk.StringVar(value="linear")
        ctk.CTkRadioButton(settings_frame, text="Лінійний", variable=self.trit_key_type_var, value="linear").pack(side="left")
        ctk.CTkRadioButton(settings_frame, text="Нелінійний", variable=self.trit_key_type_var, value="nonlinear").pack(side="left")
        ctk.CTkRadioButton(settings_frame, text="Гасло", variable=self.trit_key_type_var, value="password").pack(side="left")

        # Текстова область
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_area = ctk.CTkTextbox(text_frame, wrap="word")
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

    def encrypt_text(self):
        cipher_type = self.cipher_type_var.get()
        language = self.language_var.get()

        if cipher_type == "caesar":
            key = self.key_entry.get()
            is_valid, result = self.cipher.validate_key(key, language)
            if not is_valid:
                messagebox.showerror("Помилка", result)
                return
            text = self.text_area.get(1.0, "end-1c")
            encrypted_text = self.cipher.encrypt(text, result, language)
        else:
            trit_type = self.trit_key_type_var.get()
            key_input = self.key_entry.get()
            key_values = key_input.split(",") if trit_type != "password" else key_input
            is_valid, result = self.trit_cipher.validate_key(trit_type, key_values, language)
            if not is_valid:
                messagebox.showerror("Помилка", result)
                return
            text = self.text_area.get(1.0, "end-1c")
            encrypted_text = self.trit_cipher.encrypt(text, trit_type, result, language)

        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, encrypted_text)
        messagebox.showinfo("Успіх", "Текст зашифровано")

    def decrypt_text(self):
        cipher_type = self.cipher_type_var.get()
        language = self.language_var.get()

        if cipher_type == "caesar":
            key = self.key_entry.get()
            is_valid, result = self.cipher.validate_key(key, language)
            if not is_valid:
                messagebox.showerror("Помилка", result)
                return
            text = self.text_area.get(1.0, "end-1c")
            decrypted_text = self.cipher.decrypt(text, result, language)
        else:
            trit_type = self.trit_key_type_var.get()
            key_input = self.key_entry.get()
            key_values = key_input.split(",") if trit_type != "password" else key_input
            is_valid, result = self.trit_cipher.validate_key(trit_type, key_values, language)
            if not is_valid:
                messagebox.showerror("Помилка", result)
                return
            text = self.text_area.get(1.0, "end-1c")
            decrypted_text = self.trit_cipher.decrypt(text, trit_type, result, language)

        self.text_area.delete(1.0, "end")
        self.text_area.insert(1.0, decrypted_text)
        messagebox.showinfo("Успіх", "Текст розшифровано")

    def run(self):
        self.root.mainloop()
