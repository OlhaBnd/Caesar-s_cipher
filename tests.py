import unittest
import sys
import os
import tempfile
import tkinter as tk

# Додаємо шлях для імпорту модулів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cipher import CaesarCipher
from file_handler import FileHandler


class TestMainFunctionality(unittest.TestCase):
    """Загальний тест основної функціональності криптосистеми"""

    def setUp(self):
        """Налаштування перед тестом"""
        self.cipher = CaesarCipher()
        self.root = tk.Tk()
        self.root.withdraw()
        self.text_widget = tk.Text(self.root)
        self.file_handler = FileHandler(self.text_widget)

    def tearDown(self):
        """Очищення після тесту"""
        self.root.destroy()

    def test_complete_workflow_english(self):
        """Повний тест робочого процесу з англійським текстом"""
        print("\n=== Тест англійського тексту ===")

        # 1. Вхідні дані
        original_text = "Hello World! This is a secret message."
        key = 5
        language = "english"

        print(f"Оригінальний текст: {original_text}")
        print(f"Ключ: {key}, Мова: {language}")

        # 2. Валідація ключа
        is_valid, valid_key = self.cipher.validate_key(key, language)
        self.assertTrue(is_valid, "Ключ має бути валідним")
        self.assertEqual(valid_key, key, "Ключ має збігатися")
        print("Валідація ключа пройдена")

        # 3. Шифрування
        encrypted_text = self.cipher.encrypt(original_text, key, language)
        self.assertNotEqual(encrypted_text, original_text, "Зашифрований текст має відрізнятися")
        print(f"Зашифрований текст: {encrypted_text}")
        print("Шифрування пройдено")

        # 4. Розшифрування
        decrypted_text = self.cipher.decrypt(encrypted_text, key, language)
        self.assertEqual(decrypted_text, original_text, "Розшифрований текст має збігатися з оригіналом")
        print(f"Розшифрований текст: {decrypted_text}")
        print("Розшифрування пройдено")

        # 5. Робота з файлом
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name

        try:
            # Збереження зашифрованого тексту
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, encrypted_text)
            self.file_handler.current_file = temp_file
            self.file_handler.save_file()

            # Відкриття та перевірка
            with open(temp_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            self.assertEqual(file_content, encrypted_text, "Вміст файлу має збігатися")
            print("Робота з файлом пройдена")

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

        print("✅ Весь робочий процес пройдений успішно!\n")

    def test_complete_workflow_ukrainian(self):
        """Повний тест робочого процесу з українським текстом"""
        print("\n=== Тест українського тексту ===")

        # 1. Вхідні дані
        original_text = "Привіт Світ! Це секретне повідомлення."
        key = 7
        language = "ukrainian"

        print(f"Оригінальний текст: {original_text}")
        print(f"Ключ: {key}, Мова: {language}")

        # 2. Валідація ключа
        is_valid, valid_key = self.cipher.validate_key(key, language)
        self.assertTrue(is_valid, "Ключ має бути валідним")
        self.assertEqual(valid_key, key, "Ключ має збігатися")
        print("Валідація ключа пройдена")

        # 3. Шифрування
        encrypted_text = self.cipher.encrypt(original_text, key, language)
        self.assertNotEqual(encrypted_text, original_text, "Зашифрований текст має відрізнятися")
        print(f"Зашифрований текст: {encrypted_text}")
        print("Шифрування пройдено")

        # 4. Розшифрування
        decrypted_text = self.cipher.decrypt(encrypted_text, key, language)
        self.assertEqual(decrypted_text, original_text, "Розшифрований текст має збігатися з оригіналом")
        print(f"Розшифрований текст: {decrypted_text}")
        print("Розшифрування пройдено")
        print("Весь робочий процес пройдений успішно!\n")

    def test_key_validation(self):
        """Тест валідації різних ключів"""
        print("\n=== Тест валідації ключів ===")

        # Тест коректних ключів
        valid_cases = [
            (3, "english", True),
            (25, "english", True),
            (5, "ukrainian", True),
            (32, "ukrainian", True)
        ]

        for key, lang, expected in valid_cases:
            is_valid, result = self.cipher.validate_key(key, lang)
            self.assertEqual(is_valid, expected, f"Ключ {key} для {lang} має бути валідним")
            print(f"Ключ {key} для {lang} - валідний")

        # Тест некоректних ключів
        invalid_cases = [
            (0, "english", False),
            (26, "english", False),
            (0, "ukrainian", False),
            (33, "ukrainian", False),
            ("abc", "english", False),
            ("", "ukrainian", False)
        ]

        for key, lang, expected in invalid_cases:
            is_valid, result = self.cipher.validate_key(key, lang)
            self.assertEqual(is_valid, expected, f"Ключ {key} для {lang} має бути невалідним")
            print(f"Ключ {key} для {lang} - невалідний (як і очікувалось)")

        print("✅ Валідація ключів пройдена\n")

    def test_special_characters_preservation(self):
        """Тест збереження спеціальних символів"""
        print("\n=== Тест спеціальних символів ===")

        test_cases = [
            ("Hello, World! 123 #$%", 3, "english"),
            ("Привіт, Світ! 123 @#$", 5, "ukrainian"),
            ("Line 1\nLine 2\tTab", 7, "english"),
            ("Текст з: комами, крапками. І іншим!", 4, "ukrainian")
        ]

        for text, key, language in test_cases:
            encrypted = self.cipher.encrypt(text, key, language)
            decrypted = self.cipher.decrypt(encrypted, key, language)

            self.assertEqual(decrypted, text, f"Спецсимволи мають зберігатися для: {text}")

            # Перевіряємо, що числа та спецсимволи залишилися
            for char in "0123456789!@#$%^&*()\n\t ,.":
                if char in text:
                    self.assertIn(char, encrypted, f"Символ '{char}' має зберігатися")

            print(f"Текст з спецсимволами оброблено коректно: '{text[:20]}...'")

        print("✅ Збереження спеціальних символів пройдено\n")

    def test_case_sensitivity(self):
        """Тест чутливості до регістру"""
        print("\n=== Тест регістру ===")

        test_cases = [
            ("UpperCase LOWERCASE MixedCase", 10, "english"),
            ("ВЕЛИКІ МАЛІ Змішані", 8, "ukrainian")
        ]

        for text, key, language in test_cases:
            encrypted = self.cipher.encrypt(text, key, language)
            decrypted = self.cipher.decrypt(encrypted, key, language)

            self.assertEqual(decrypted, text, "Регістр має зберігатися")

            # Перевіряємо, що регістр зберігається в зашифрованому тексті
            for i, char in enumerate(text):
                if char.isupper():
                    self.assertTrue(encrypted[i].isupper(), f"Велика літера '{char}' має залишитися великою")
                elif char.islower():
                    self.assertTrue(encrypted[i].islower(), f"Мала літера '{char}' має залишитися малою")

            print(f"Регістр збережено для: '{text}'")

        print("✅ Тест чутливості до регістру пройдено\n")

    def test_file_operations(self):
        """Тест основних операцій з файлами"""
        print("\n=== Тест операцій з файлами ===")

        test_content = "Тестовий вміст для перевірки роботи з файлами.\nДругий рядок."

        # Створюємо тимчасовий файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name

        try:
            # Тест 1: Створення нового файлу
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, "Тимчасовий текст")
            self.file_handler.new_file()
            self.assertEqual(self.text_widget.get(1.0, tk.END).strip(), "", "Новий файл має бути пустим")
            print("Створення нового файлу пройдено")

            # Тест 2: Збереження файлу
            self.text_widget.insert(1.0, test_content)
            self.file_handler.current_file = temp_file
            self.file_handler.save_file()

            with open(temp_file, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            self.assertEqual(saved_content, test_content, "Збережений вміст має збігатися")
            print("Збереження файлу пройдено")

            # Тест 3: Відкриття файлу
            self.text_widget.delete(1.0, tk.END)
            with open(temp_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                self.text_widget.insert(1.0, file_content)

            loaded_content = self.text_widget.get(1.0, tk.END).strip()
            self.assertEqual(loaded_content, test_content, "Завантажений вміст має збігатися")
            print("Відкриття файлу пройдено")

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

        print("✅ Операції з файлами пройдені успішно!\n")


def run_main_test():
    """Запуск головного тесту"""
    print("=" * 60)
    print("ЗАПУСК ГОЛОВНОГО ТЕСТУ КРИПТОСИСТЕМИ ЦЕЗАРЯ")
    print("=" * 60)

    # Створюємо test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMainFunctionality)

    # Запускаємо тести
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    if result.wasSuccessful():
        print("ВСІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
        print("Криптосистема працює коректно")
        return 0
    else:
        print("ДЕЯКІ ТЕСТИ НЕ ПРОЙДЕНІ")
        return 1


if __name__ == '__main__':
    sys.exit(run_main_test())