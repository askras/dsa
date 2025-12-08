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

### Криптоалгоритмы
## Шифр Виженера

```python
import random
import math
from typing import Tuple, List

class VigenereCipher:
    
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    
    def prepare_key(self, text: str, key: str) -> str:
        key = key.upper()
        prepared_key = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                prepared_key += key[key_index % len(key)]
                key_index += 1
            else:
                prepared_key += char
                
        return prepared_key
    
    def encrypt(self, plaintext: str, key: str) -> str:
        prepared_key = self.prepare_key(plaintext, key)
        ciphertext = ""
        
        for i, char in enumerate(plaintext):
            if char.isupper():
                shift = self.alphabet.index(prepared_key[i])
                original_pos = self.alphabet.index(char)
                new_pos = (original_pos + shift) % 26
                ciphertext += self.alphabet[new_pos]
            elif char.islower():
                shift = self.alphabet.index(prepared_key[i].upper())
                original_pos = self.alphabet_lower.index(char)
                new_pos = (original_pos + shift) % 26
                ciphertext += self.alphabet_lower[new_pos]
            else:
                ciphertext += char
                
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        prepared_key = self.prepare_key(ciphertext, key)
        plaintext = ""
        
        for i, char in enumerate(ciphertext):
            if char.isupper():
                shift = self.alphabet.index(prepared_key[i])
                original_pos = self.alphabet.index(char)
                new_pos = (original_pos - shift) % 26
                plaintext += self.alphabet[new_pos]
            elif char.islower():
                shift = self.alphabet.index(prepared_key[i].upper())
                original_pos = self.alphabet_lower.index(char)
                new_pos = (original_pos - shift) % 26
                plaintext += self.alphabet_lower[new_pos]
            else:
                plaintext += char
                
        return plaintext
```

### Криптосистема Пэйе

```python
class PaillierCryptosystem:
    
    def __init__(self, key_length: int = 64):
        self.key_length = key_length
    
    def gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a
    
    def lcm(self, a: int, b: int) -> int:
        return abs(a * b) // self.gcd(a, b)
    
    def mod_inverse(self, a: int, m: int) -> int:
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Inverse doesn't exist")
        return (x % m + m) % m
    
    def is_prime(self, n: int, k: int = 5) -> bool:
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        
        s, d = 0, n - 1
        while d % 2 == 0:
            s += 1
            d //= 2
        
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def generate_prime(self) -> int:
        while True:
            p = random.getrandbits(self.key_length // 2)
            p |= (1 << (self.key_length // 2 - 1)) | 1
            if self.is_prime(p):
                return p
    
    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        p = self.generate_prime()
        q = self.generate_prime()
        
        while p == q:
            q = self.generate_prime()
        
        n = p * q
        lambda_val = self.lcm(p - 1, q - 1)
        
        g = n + 1
        
        n_sq = n * n
        L_val = (pow(g, lambda_val, n_sq) - 1) // n
        mu = self.mod_inverse(L_val, n)
        
        public_key = (n, g)
        private_key = (lambda_val, mu)
        
        return public_key, private_key
    
    def L(self, x: int, n: int) -> int:
        return (x - 1) // n
    
    def encrypt(self, m: int, public_key: Tuple[int, int]) -> int:
        n, g = public_key
        n_sq = n * n
        
        while True:
            r = random.randint(1, n - 1)
            if self.gcd(r, n) == 1:
                break
        
        c = (pow(g, m, n_sq) * pow(r, n, n_sq)) % n_sq
        return c
    
    def decrypt(self, c: int, public_key: Tuple[int, int], private_key: Tuple[int, int]) -> int:
        n, g = public_key
        lambda_val, mu = private_key
        n_sq = n * n
        
        m = (self.L(pow(c, lambda_val, n_sq), n) * mu) % n
        return m
    
    def text_to_numbers(self, text: str) -> List[int]:
        return [ord(char) for char in text]
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        return ''.join(chr(num) for num in numbers)



```

Генерация ключей:
Выбираем два больших простых числа p и q

Вычисляем n = p * q (публичный модуль)

Вычисляем λ = НОК(p-1, q-1) (секретный параметр)

Выбираем g = n + 1 (публичный параметр)

Публичный ключ: (n, g)
Приватный ключ: (λ, μ)

Шифрование:
Для шифрования числа m:

Выбираем случайное r (1 < r < n)

Вычисляем: c = (gᵐ * rⁿ) mod n²

Важно: Одно и то же m с разными r дает разные c!

Дешифрование:
m = L(c^λ mod n²) * μ mod n

```python
p = 541, q = 619
n = p*q = 334879
g = n+1 = 334880
λ = НОК(540, 618) = 55620
μ = вычисляется...


Выбираем r=123456
c = (334880⁴² * 123456³³⁴⁸⁷⁹) mod n²
c = 83274619823... (очень большое число)


m = специальная_формула(c) = 42
```

```python

```
