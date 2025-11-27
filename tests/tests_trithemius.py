import unittest
from cipher import TrithemiusCipher

class TestTrithemiusCipher(unittest.TestCase):
    """Тести для шифру Тритеміуса (регістронезалежні)"""

    def setUp(self):
        self.cipher = TrithemiusCipher()

    def check_cipher(self, text, key, mode, **kwargs):
        encrypted = self.cipher.encrypt(text, key, mode, language="uk", **kwargs)
        decrypted = self.cipher.decrypt(encrypted, key, mode, language="uk", **kwargs)
        self.assertEqual(decrypted.upper(), text.upper())

    def test_linear_cipher(self):
        text = "Привіт, Світ! 123"
        key = (3, 5)  # лінійний ключ із 2 елементів
        self.check_cipher(text, key, mode="linear")

    def test_nonlinear_cipher(self):
        text = "Тест Нелінійного!"
        key = (2, 3, 4)  # нелінійний ключ із 3 елементів
        self.check_cipher(text, key, mode="nonlinear")

    def test_password_cipher(self):
        text = "Гасло123! Тест"
        key = "МоєГасло"  # текстовий ключ
        self.check_cipher(text, key, mode="password")

if __name__ == "__main__":
    unittest.main()
