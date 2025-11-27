import unittest
from cipher import BookCipher

class TestBookCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = BookCipher(columns=10)
        self.key_text = (
            "Білі мухи налетіли —\n"
            "Все подвір'я стало біле.\n"
            "Не злічити білих мух,\n"
            "Що летять, неначе пух."
        )

    def test_encrypt_decrypt_letters(self):
        text = "Цей шифр"
        encrypted = self.cipher.encrypt(text, self.key_text)
        decrypted = self.cipher.decrypt(encrypted, self.key_text)
        self.assertEqual(decrypted.lower(), text.lower())  # регістр можна ігнорувати

    def test_encrypt_decrypt_with_spaces(self):
        text = "Цей шифр на стільки секретний"
        encrypted = self.cipher.encrypt(text, self.key_text)
        decrypted = self.cipher.decrypt(encrypted, self.key_text)
        self.assertEqual(decrypted.lower(), text.lower())

    def test_encrypt_decrypt_with_punctuation(self):
        text = "Привіт, друзі!"
        encrypted = self.cipher.encrypt(text, self.key_text)
        decrypted = self.cipher.decrypt(encrypted, self.key_text)
        self.assertEqual(decrypted.lower(), text.lower())

    def test_unknown_characters_remain(self):
        text = "12345 @#$%"
        encrypted = self.cipher.encrypt(text, self.key_text)
        decrypted = self.cipher.decrypt(encrypted, self.key_text)
        self.assertEqual(decrypted, text)  # цифри та символи не змінюються

    def test_empty_text(self):
        text = ""
        encrypted = self.cipher.encrypt(text, self.key_text)
        decrypted = self.cipher.decrypt(encrypted, self.key_text)
        self.assertEqual(decrypted, "")

if __name__ == "__main__":
    unittest.main()
