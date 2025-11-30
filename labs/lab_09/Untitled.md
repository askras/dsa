---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Лабораторная работа 9

```python
import random
import math
from typing import Tuple, List

class CryptoSystem:
    def __init__(self):
        self.caesar_key = None
        self.bg_public_key = None
        self.bg_private_key = None
    
    def generate_key_from_seed(self, seed_key: str) -> int:
        """Генерация числового ключа на основе произвольного ключа пользователя"""
        key_hash = 0
        for char in seed_key:
            key_hash = (key_hash * 31 + ord(char)) % 1000000
        return max(1, key_hash % 95)  # Для шифра Цезаря (0-94 для печатных символов)
    
    def caesar_encrypt(self, text: str, seed_key: str) -> str:
        """Шифрование методом Цезаря"""
        self.caesar_key = self.generate_key_from_seed(seed_key)
        encrypted = []
        
        for char in text:
            if 32 <= ord(char) <= 126:  # Печатные ASCII символы
                new_char_code = 32 + (ord(char) - 32 + self.caesar_key) % 95
                encrypted.append(chr(new_char_code))
            else:
                encrypted.append(char)
        
        return ''.join(encrypted)
    
    def caesar_decrypt(self, encrypted_text: str, seed_key: str) -> str:
        """Дешифрование методом Цезаря"""
        key = self.generate_key_from_seed(seed_key)
        decrypted = []
        
        for char in encrypted_text:
            if 32 <= ord(char) <= 126:
                new_char_code = 32 + (ord(char) - 32 - key) % 95
                decrypted.append(chr(new_char_code))
            else:
                decrypted.append(char)
        
        return ''.join(decrypted)
    
    def generate_blum_goldwasser_keys(self, seed_key: str) -> Tuple[int, int]:
        """Генерация ключей для криптосистемы Блюма-Гольдвассер"""
        # Используем ключ пользователя для детерминистической генерации
        random.seed(sum(ord(c) for c in seed_key))
        
        # Генерация двух простых чисел вида 4k+3
        def generate_blum_prime():
            while True:
                p = random.randint(100, 1000)
                if self.is_prime(p) and p % 4 == 3:
                    return p
        
        p = generate_blum_prime()
        q = generate_blum_prime()
        
        n = p * q
        self.bg_public_key = n
        self.bg_private_key = (p, q)
        
        return n, (p, q)
    
    def is_prime(self, n: int) -> bool:
        """Проверка числа на простоту"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def bg_encrypt(self, text: str, seed_key: str) -> Tuple[List[int], int]:
        """Шифрование методом Блюма-Гольдвассера"""
        n, _ = self.generate_blum_goldwasser_keys(seed_key)
        
        # Преобразование текста в биты
        bits = []
        for char in text:
            bits.extend([int(b) for b in format(ord(char), '08b')])
        
        # Генерация псевдослучайной последовательности
        x = random.randint(2, n-1)
        cipher_bits = []
        
        for bit in bits:
            x = (x * x) % n
            pseudo_random_bit = x % 2
            cipher_bits.append(bit ^ pseudo_random_bit)
        
        return cipher_bits, x  # Возвращаем шифртекст и последнее состояние x
    
    def bg_decrypt(self, cipher_bits: List[int], final_x: int, seed_key: str) -> str:
        """Дешифрование методом Блюма-Гольдвассера"""
        _, (p, q) = self.generate_blum_goldwasser_keys(seed_key)
        n = p * q
        
        # Восстановление псевдослучайной последовательности
        x = final_x
        original_bits = []
        
        for cipher_bit in cipher_bits:
            x = (x * x) % n
            pseudo_random_bit = x % 2
            original_bits.append(cipher_bit ^ pseudo_random_bit)
        
        # Преобразование битов обратно в текст
        text = ""
        for i in range(0, len(original_bits), 8):
            if i + 8 <= len(original_bits):
                byte_bits = original_bits[i:i+8]
                char_code = int(''.join(map(str, byte_bits)), 2)
                text += chr(char_code)
        
        return text
    
    def demo(self):
        """Демонстрация работы обоих методов"""
        print("=== ДЕМОНСТРАЦИЯ ШИФРОВАНИЯ ===\n")
        
        # Исходный текст
        original_text = "Hello, World! 123"
        seed_key = "фф12К52"  # Пример ключа из задания
        
        print(f"Исходный текст: {original_text}")
        print(f"Ключ: {seed_key}\n")
        
        # Шифр Цезаря
        print("=== ШИФР ЦЕЗАРЯ ===")
        caesar_encrypted = self.caesar_encrypt(original_text, seed_key)
        caesar_decrypted = self.caesar_decrypt(caesar_encrypted, seed_key)
        
        print(f"Зашифрованный: {caesar_encrypted}")
        print(f"Расшифрованный: {caesar_decrypted}")
        print(f"Идентичны: {original_text == caesar_decrypted}\n")
        
        # Криптосистема Блюма-Гольдвассера
        print("=== КРИПТОСИСТЕМА БЛЮМА-ГОЛЬДВАССЕРА ===")
        bg_cipher_bits, final_x = self.bg_encrypt(original_text, seed_key)
        bg_decrypted = self.bg_decrypt(bg_cipher_bits, final_x, seed_key)
        
        print(f"Зашифрованный (биты): {bg_cipher_bits[:32]}...")  # Показываем первые 32 бита
        print(f"Расшифрованный: {bg_decrypted}")
        print(f"Идентичны: {original_text == bg_decrypted}\n")
        
        # Сводка
        print("=== РЕЗУЛЬТАТ ===")
        print(f"Цезарь: {'Успешно' if original_text == caesar_decrypted else 'Не успешно'}")
        print(f"Блюм-Гольдвассер: {'Успешно' if original_text == bg_decrypted else 'Не успешно'}")

# Дополнительная утилита для проверки работы
def test_crypto_system():
    """Тестирование криптосистемы"""
    crypto = CryptoSystem()
    
    test_cases = [
        "Hello, World!",
        "Test 123",
        "Простой текст",
        "Short",
        "A" * 10  # Повторяющиеся символы
    ]
    
    seed_key = "фф12К52"
    
    print("=== ТЕСТИРОВАНИЕ ===\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"Тест {i}: '{text}'")
        
        # Тест Цезаря
        encrypted = crypto.caesar_encrypt(text, seed_key)
        decrypted = crypto.caesar_decrypt(encrypted, seed_key)
        caesar_ok = text == decrypted
        
        # Тест Блюма-Гольдвассера
        bg_cipher, final_x = crypto.bg_encrypt(text, seed_key)
        bg_decrypted = crypto.bg_decrypt(bg_cipher, final_x, seed_key)
        bg_ok = text == bg_decrypted
        
        print(f"  Цезарь: {'Успешно' if caesar_ok else 'Не успешно'}")
        print(f"  Блюм-Гольдвассер: {'Успешно' if bg_ok else 'Не успешно'}")
        
        if not caesar_ok or not bg_ok:
            print(f"  Ошибка! Исходный: '{text}'")
            if not caesar_ok:
                print(f"  Цезарь расшифровал: '{decrypted}'")
            if not bg_ok:
                print(f"  БГ расшифровал: '{bg_decrypted}'")
        print()

if __name__ == "__main__":
    # Основная демонстрация
    crypto = CryptoSystem()
    crypto.demo()
    
    # Дополнительное тестирование
    test_crypto_system()
    

```

```python

```
