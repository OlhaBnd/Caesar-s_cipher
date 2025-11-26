class CaesarCipher:
    def __init__(self):
        self.ukrainian_alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def validate_key(self, key, language):
        """Валідація ключа шифрування"""
        try:
            key = int(key)
            if language == "ukrainian":
                alphabet_length = len(self.ukrainian_alphabet) // 2
            else:
                alphabet_length = len(self.english_alphabet) // 2

            if key < 1 or key >= alphabet_length:
                return False, f"Ключ повинен бути в діапазоні від 1 до {alphabet_length - 1}"
            return True, key
        except ValueError:
            return False, "Ключ повинен бути цілим числом"

    def encrypt(self, text, key, language):
        if language == "ukrainian":
            alphabet = self.ukrainian_alphabet
            alphabet_length = len(alphabet) // 2
        else:
            alphabet = self.english_alphabet
            alphabet_length = len(alphabet) // 2

        result = []

        for char in text:
            if char in alphabet:
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
        if language == "ukrainian":
            alphabet = self.ukrainian_alphabet
            alphabet_length = len(alphabet) // 2
        else:
            alphabet = self.english_alphabet
            alphabet_length = len(alphabet) // 2

        result = []

        for char in text:
            if char in alphabet:
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


class TrithemiusCipher:
    def __init__(self):
        self.ukrainian_alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
        self.english_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def validate_key(self, key_type, key_values, language):
        """Валідація ключів для лінійного, нелінійного або гасла"""
        if key_type in ["linear", "nonlinear"]:
            try:
                key_numbers = [int(k) for k in key_values]
            except ValueError:
                return False, "Коефіцієнти мають бути числами"
            if key_type == "linear" and len(key_numbers) != 2:
                return False, "Лінійний ключ повинен містити 2 числа"
            if key_type == "nonlinear" and len(key_numbers) != 3:
                return False, "Нелінійний ключ повинен містити 3 числа"
            return True, key_numbers
        elif key_type == "password":
            if not key_values:
                return False, "Гасло не може бути порожнім"
            alphabet = self.ukrainian_alphabet if language == "ukrainian" else self.english_alphabet
            for ch in key_values.upper():
                if ch not in alphabet:
                    return False, "Гасло містить недопустимі символи"
            return True, key_values.upper()
        else:
            return False, "Невідомий тип ключа"

    def encrypt(self, text, key_type, key_values, language):
        alphabet = self.ukrainian_alphabet if language == "ukrainian" else self.english_alphabet
        n = len(alphabet)
        result = []

        text = text.upper() if language == "ukrainian" else text.upper()
        key = key_values

        for i, ch in enumerate(text):
            if ch in alphabet:
                if key_type == "linear":
                    k = key[0]*i + key[1]
                elif key_type == "nonlinear":
                    k = key[0]*i*i + key[1]*i + key[2]
                elif key_type == "password":
                    k = alphabet.index(key[i % len(key)])
                else:
                    k = 0
                index = (alphabet.index(ch) + k) % n
                result.append(alphabet[index])
            else:
                result.append(ch)
        return ''.join(result)

    def decrypt(self, text, key_type, key_values, language):
        alphabet = self.ukrainian_alphabet if language == "ukrainian" else self.english_alphabet
        n = len(alphabet)
        result = []

        text = text.upper() if language == "ukrainian" else text.upper()
        key = key_values

        for i, ch in enumerate(text):
            if ch in alphabet:
                if key_type == "linear":
                    k = key[0]*i + key[1]
                elif key_type == "nonlinear":
                    k = key[0]*i*i + key[1]*i + key[2]
                elif key_type == "password":
                    k = alphabet.index(key[i % len(key)])
                else:
                    k = 0
                index = (alphabet.index(ch) - k) % n
                result.append(alphabet[index])
            else:
                result.append(ch)
        return ''.join(result)
