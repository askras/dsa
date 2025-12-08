# Лабораторная работа 9
# Криптоалгоритмы
## Цель работы
Получение практических навыков защиты программного обеспечения от несанкционированного доступа путем шифрования с использованием криптоалгоритмов.
## Задачи лабораторной работы
1. Изучение различных алгоритмов шифрования
2. Реализация двух индивидуальных алгоритмов
3. Применение алгоритмов для шифровки и дешифровки сообщений
## Словесная постановка задачи
1. Изучить какие существуют виды шифров
2. Реализовать два вида шифрования 
3. Применить это шифрования для сообщения
## Реализация алгоритмов шифрования
Первая часть реализует класс для Великого шифра Россиньоля
``` Python
#1

import math

class VelikiyCipher:
    def __init__(self, key1, key2):
        self.key1 = self.validate_key(key1)
        self.key2 = self.validate_key(key2)

    def validate_key(self, key):
        key = [int(k) for k in key]
        
        return key
        
    def create_permutation_order(self, key):
        indexed_key = list(enumerate(key))
        sorted_key = sorted(indexed_key, key=lambda x: x[1])
        return [i for i, _ in sorted_key]
    
    def apply_transposition(self, text, key, encrypt=True):
        key_order = self.create_permutation_order(key)
        n_cols = len(key)
        n_rows = math.ceil(len(text) / n_cols)
        
        empty_cells = n_rows * n_cols - len(text)
        
        matrix = [['' for _ in range(n_cols)] for _ in range(n_rows)]
        
        if encrypt:
            pos = 0
            for row in range(n_rows):
                for col in range(n_cols):
                    if pos < len(text):
                        matrix[row][col] = text[pos]
                        pos += 1
                    else:
                        matrix[row][col] = ''
            
            result = []
            for col_idx in key_order:
                for row in range(n_rows):
                    if matrix[row][col_idx]:
                        result.append(matrix[row][col_idx])
                        
        else:
            chars_per_col = [0] * n_cols
            full_cols = len(text) % n_cols
            if full_cols == 0:
                full_cols = n_cols
            
            for col_idx in key_order:
                if col_idx < full_cols:
                    chars_per_col[col_idx] = n_rows
                else:
                    chars_per_col[col_idx] = n_rows - 1
            
            pos = 0
            for col_idx in key_order:
                for row in range(chars_per_col[col_idx]):
                    if pos < len(text):
                        matrix[row][col_idx] = text[pos]
                        pos += 1
            result = []
            for row in range(n_rows):
                for col in range(n_cols):
                    if matrix[row][col]:
                        result.append(matrix[row][col])
        
        return ''.join(result)
    
    def encrypt(self, plaintext):
        text = ''.join(plaintext.upper().split())
        
        step1 = self.apply_transposition(text, self.key1, encrypt=True)
        ciphertext = self.apply_transposition(step1, self.key2, encrypt=True)
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        text = ciphertext.upper()
        
        step1 = self.apply_transposition(text, self.key2, encrypt=False)
        plaintext = self.apply_transposition(step1, self.key1, encrypt=False)
        
        return plaintext

def input_key(key_number):
    while True:
        try:
            key_str = input(f"Введите ключ {key_number}: ").strip()
            
            if not key_str:
                print("Ключ не может быть пустым")
                continue
                
            key_list = [int(x) for x in key_str.split()]
            
            if len(key_list) < 2:
                print("Ключ должен содержать минимум 2 цифры")
                continue
                
            return key_list
            
        except ValueError:
            print("Ошибка: вводите только цифры, разделенные пробелами")
        except Exception as e:
            print(f"Ошибка: {e}")

def input_operation():
    while True:
        print("\nВыберите операцию:")
        print("1 - Зашифровать текст")
        print("2 - Расшифровать текст")
        print("3 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Неверный выбор. Попробуйте снова.")

def run_cipher_program():
    print("\nВведите ключи:")
    key1 = input_key(1)
    key2 = input_key(2)
    
    try:
        cipher = VelikiyCipher(key1, key2)
        print(f"\nКлюч 1: {key1}")
        print(f"Ключ 2: {key2}")
        print("Шифр успешно инициализирован!")
    except ValueError as e:
        print(f"\nОшибка инициализации шифра: {e}")
        return
    
    while True:
        operation = input_operation()
        
        if operation == '1': 
            plaintext = input("\nВведите текст для шифрования: ").strip()
            if plaintext:
                try:
                    encrypted = cipher.encrypt(plaintext)
                    print(f"\nИсходный текст: {plaintext}")
                    print(f"Зашифрованный текст: {encrypted}")
                except Exception as e:
                    print(f"Ошибка при шифровании: {e}")
            else:
                print("Текст не может быть пустым")
                
        elif operation == '2': 
            ciphertext = input("\nВведите текст для дешифрования: ").strip()
            if ciphertext:
                try:
                    decrypted = cipher.decrypt(ciphertext)
                    print(f"\nЗашифрованный текст: {ciphertext}")
                    print(f"Расшифрованный текст: {decrypted}")
                except Exception as e:
                    print(f"Ошибка при дешифровании: {e}")
            else:
                print("Текст не может быть пустым")
                
        elif operation == '3':
            print("\nВыход из программы.")
            break

if __name__ == "__main__":
    try:
        run_cipher_program()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
```
Вторая часть реализует класс для алгоритма ECIES
``` Python
#2

import random
import hashlib
import hmac
import os


import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid')

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class Point:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __eq__(self, other):
        if self.infinity and other.infinity: return True
        if self.infinity or other.infinity: return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.infinity: return "Point(Infinity)"
        return f"Point({hex(self.x)}, {hex(self.y)})"

def mod_inverse(a, m):
    return pow(a, m - 2, m)

def point_add(p1, p2):
    if p1.infinity: return p2
    if p2.infinity: return p1

    if p1.x == p2.x and p1.y != p2.y:
        return Point(0, 0, True)

    if p1.x == p2.x and p1.y == p2.y:
        
        if p1.y == 0: return Point(0, 0, True)
        lam = (3 * p1.x**2 + A) * mod_inverse(2 * p1.y, P)
    else:

        lam = (p2.y - p1.y) * mod_inverse(p2.x - p1.x, P)
    
    lam %= P
    x3 = (lam**2 - p1.x - p2.x) % P
    y3 = (lam * (p1.x - x3) - p1.y) % P
    return Point(x3, y3)

def scalar_mult(k, point):
    result = Point(0, 0, True)
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

G = Point(Gx, Gy)

class ECIES:
    def __init__(self):
        pass

    def generate_keys(self):
        priv = random.randint(1, N - 1)
        pub = scalar_mult(priv, G)
        return priv, pub

    def kdf(self, secret_point):
        x_bytes = secret_point.x.to_bytes(32, 'big')
        hash_bytes = hashlib.sha512(x_bytes).digest()
        return hash_bytes[:32], hash_bytes[32:] 

    def encrypt_symmetric(self, key, plaintext):
        ciphertext = bytearray()
        for i, b in enumerate(plaintext):
            ciphertext.append(b ^ key[i % len(key)])
        return bytes(ciphertext)

    def decrypt_symmetric(self, key, ciphertext):
        return self.encrypt_symmetric(key, ciphertext)

    def encrypt(self, pub_key, message):
        k = random.randint(1, N - 1)
        R = scalar_mult(k, G)

        S = scalar_mult(k, pub_key)
        if S.infinity:
            raise ValueError("Invalid shared secret")

        Ke, Km = self.kdf(S)

        if isinstance(message, str):
            message = message.encode('utf-8')
        C = self.encrypt_symmetric(Ke, message)

        tag = hmac.new(Km, C, hashlib.sha256).digest()

        return R, C, tag

    def decrypt(self, priv_key, R, C, tag):
        S = scalar_mult(priv_key, R)
        if S.infinity:
            raise ValueError("Invalid shared secret")

        Ke, Km = self.kdf(S)

        calc_tag = hmac.new(Km, C, hashlib.sha256).digest()
        if not hmac.compare_digest(tag, calc_tag):
            raise ValueError("MAC verification failed! Message corrupted.")

        plaintext = self.decrypt_symmetric(Ke, C)
        return plaintext.decode('utf-8')

ecies = ECIES()

alice_priv, alice_pub = ecies.generate_keys()
print(f"Alice Private: {hex(alice_priv)}")
print(f"Alice Public: {alice_pub}")

msg = "Hello, Elliptic Curve World!"
print(f"\nOriginal Message: {msg}")

R, C, tag = ecies.encrypt(alice_pub, msg)
print(f"Encrypted (R): {R}")
print(f"Encrypted (C hex): {C.hex()}")
print(f"Tag (hex): {tag.hex()}")


decrypted = ecies.decrypt(alice_priv, R, C, tag)
print(f"\nDecrypted: {decrypted}")
```