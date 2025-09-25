class CaesarCipher:
    def __init__(self):
        self.ukrainian_alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def validate_key(self, key, language):
        """Валідація ключа шифрування"""
        try:
            key = int(key)
            if language == "ukrainian":
                alphabet_length = len(self.ukrainian_alphabet) // 2  # Враховуємо тільки великі літери
            else:
                alphabet_length = len(self.english_alphabet) // 2

            if key < 1 or key >= alphabet_length:
                return False, f"Ключ повинен бути в діапазоні від 1 до {alphabet_length - 1}"
            return True, key
        except ValueError:
            return False, "Ключ повинен бути цілим числом"

    def encrypt(self, text, key, language):
        """Шифрування тексту"""
        if language == "ukrainian":
            alphabet = self.ukrainian_alphabet
            alphabet_length = len(alphabet) // 2
        else:
            alphabet = self.english_alphabet
            alphabet_length = len(alphabet) // 2

        result = []

        for char in text:
            if char in alphabet:
                # Визначаємо позицію символу в алфавіті
                if char.isupper():
                    index = alphabet.index(char)
                    new_index = (index + key) % alphabet_length
                    result.append(alphabet[new_index])
                else:
                    index = alphabet.index(char)
                    new_index = (index + key) % alphabet_length + alphabet_length
                    result.append(alphabet[new_index])
            else:
                result.append(char)

        return ''.join(result)

    def decrypt(self, text, key, language):
        """Розшифрування тексту"""
        if language == "ukrainian":
            alphabet = self.ukrainian_alphabet
            alphabet_length = len(alphabet) // 2
        else:
            alphabet = self.english_alphabet
            alphabet_length = len(alphabet) // 2

        result = []

        for char in text:
            if char in alphabet:
                # Визначаємо позицію символу в алфавіті
                if char.isupper():
                    index = alphabet.index(char)
                    new_index = (index - key) % alphabet_length
                    result.append(alphabet[new_index])
                else:
                    index = alphabet.index(char)
                    new_index = (index - key) % alphabet_length + alphabet_length
                    result.append(alphabet[new_index])
            else:
                result.append(char)

        return ''.join(result)