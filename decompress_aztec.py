#!/usr/bin/env python3
"""
Декомпрессия и расширенный анализ данных Aztec кода
"""
import zlib
import gzip
import io

# Hex данные
hex_data = """
fc 27 a0 60 24 aa 89 7f   43 d3 29 47 52 0d f4 6e
9a df ff 48 d1 5d fe 43   08 ce fe c4 5c c1 49 74
e8 cd c0 e9 ea 53 0e 3c   0c 7d 81 bc 1b b4 e3 c0
ad 93 fb f2 f9 ca e6 17   aa 1e b9 eb 91 d3 e1 f4
dc b7 b3 f2 63 da 31 e9   40 48 70 b4 22 91 c7 07
f8 57 c7 3d 3f a1 b5 c3   71 32 df d7 b2 1a 1f 28
fb e3 7f fd eb cd 2f b9   f4 55 e3 f0 7b 5c b7 fc
e5 fe b7 bb 53 d8 8f ed   12 af 22 c9 af c7 52 e5
fe 16 a7 44 af d7 b8 4c   ce 68 44 54 04 00 23 e1
d4 11 28 54 00 00 01 59   11 58 45 5b ff 88 60 72
17 cd e0 70 20 df 6a 25   38 57 b3 2e 8c 5d 20 2d
be fb 1d f2 f4 5b f1 a9   e3 59 aa ab ff 5c 37 4b
97 a1 96 6e 36 02 62 bb   16 5a 11 92 58 f4 d7 66
a2 06 fb 24 7b 56 a2 09   eb ea 1e 63 fe 93 b9 61
94 b3 ff 55 5f 1e f5 1f   51 fd 19 42 e4 24 e4 22
b4 56 91 e7 c2 15 3d 07   b3 56 a7 3e 7f a0 03 6b
a0 50 4b cd f2 48 1b fd   42 36 d8 dd 2c ef 71 8b
77 71 6f c9 57 99 39 f2   ff 31 78 32 e8 43 13 27
65 d3 09 e4 16 81 64 6a   5e 9c ca 50 a9 53 e7 06
69 0e 6f 4f f4 b1 7d de   f4 2c 27 46 07 cb 26 f7
e5 16 bc 1f 88 b1 1b 06   87 60 71 54 e9 89 25 62
7f 8d d1 5a 47 bd 9b 87   4e 9a cd 5f 94 ca 02 58
f4 bc 71 57 2b d2 da e7   cb e7 00 30 28 49 e9 4d
72 df e3 11 02 21 e0
"""

hex_clean = hex_data.replace('\n', '').replace(' ', '').strip()
data_bytes = bytes.fromhex(hex_clean)

print("="*70)
print("🔓 ПОПЫТКИ ДЕКОМПРЕССИИ ДАННЫХ")
print("="*70)

# 1. ZLIB декомпрессия
print("\n1️⃣ ZLIB декомпрессия...")
try:
    decompressed = zlib.decompress(data_bytes)
    print("✅ УСПЕШНО! Декомпрессировано с zlib:")
    print("-"*70)
    print(decompressed.decode('utf-8', errors='ignore'))
    print("-"*70)
except Exception as e:
    print(f"❌ Zlib не сработал: {e}")

# 2. GZIP декомпрессия
print("\n2️⃣ GZIP декомпрессия...")
try:
    with gzip.GzipFile(fileobj=io.BytesIO(data_bytes)) as f:
        decompressed = f.read()
    print("✅ УСПЕШНО! Декомпрессировано с gzip:")
    print("-"*70)
    print(decompressed.decode('utf-8', errors='ignore'))
    print("-"*70)
except Exception as e:
    print(f"❌ Gzip не сработал: {e}")

# 3. ZLIB с разными wbits (для raw deflate)
print("\n3️⃣ ZLIB с различными параметрами...")
for wbits in [-15, -9, 15, 9]:
    try:
        decompressed = zlib.decompress(data_bytes, wbits)
        print(f"✅ УСПЕШНО с wbits={wbits}:")
        print("-"*70)
        try:
            print(decompressed.decode('utf-8'))
        except:
            print(decompressed.decode('latin-1', errors='ignore'))
        print("-"*70)
        break
    except Exception as e:
        print(f"❌ wbits={wbits}: {e}")

# 4. Анализ как UIC 918.3 формат
print("\n" + "="*70)
print("🎫 АНАЛИЗ ФОРМАТА UIC 918.3 (билеты DB)")
print("="*70)

# UIC 918.3 использует ASN.1 кодирование
# Первые байты могут содержать метаданные
print(f"\nПервый байт (версия/тип): 0x{data_bytes[0]:02x} ({data_bytes[0]})")

# Ищем поля данных
if data_bytes[0] == 0xfc or data_bytes[0] == 0xfd:
    print("✅ Похоже на UIC 918.3 формат (начинается с 0xfc/0xfd)")
    print("\nВозможная структура:")
    print(f"  - Версия формата: {data_bytes[0]}")
    print(f"  - Следующие байты: {data_bytes[1:10].hex(' ')}")

# 5. Поиск временных меток (Unix timestamp)
print("\n" + "="*70)
print("📅 ПОИСК ВРЕМЕННЫХ МЕТОК")
print("="*70)

import struct
from datetime import datetime

# Ищем возможные timestamps (4 байта)
for i in range(0, len(data_bytes) - 4):
    try:
        # Big-endian
        timestamp_be = struct.unpack('>I', data_bytes[i:i+4])[0]
        # Проверяем разумность (2020-2030)
        if 1577836800 < timestamp_be < 1893456000:  # 2020-01-01 to 2030-01-01
            dt = datetime.fromtimestamp(timestamp_be)
            print(f"✅ Возможный timestamp на позиции {i} (BE): {dt}")

        # Little-endian
        timestamp_le = struct.unpack('<I', data_bytes[i:i+4])[0]
        if 1577836800 < timestamp_le < 1893456000:
            dt = datetime.fromtimestamp(timestamp_le)
            print(f"✅ Возможный timestamp на позиции {i} (LE): {dt}")
    except:
        pass

# 6. Анализ энтропии
print("\n" + "="*70)
print("📊 АНАЛИЗ ЭНТРОПИИ (случайность данных)")
print("="*70)

from collections import Counter
byte_freq = Counter(data_bytes)
entropy = -sum((count/len(data_bytes)) * (count/len(data_bytes)).bit_length()
               for count in byte_freq.values())

print(f"Энтропия: {entropy:.2f} бит")
if entropy > 7:
    print("⚠️  Высокая энтропия - данные могут быть зашифрованы или сжаты")
elif entropy < 5:
    print("✅ Низкая энтропия - данные, вероятно, текстовые")
else:
    print("ℹ️  Средняя энтропия - смешанный контент")

# 7. Попытка найти читаемые части
print("\n" + "="*70)
print("🔍 ИЗВЛЕЧЕНИЕ ЧИТАЕМЫХ ФРАГМЕНТОВ")
print("="*70)

# Декодируем с игнорированием ошибок и ищем слова
decoded = data_bytes.decode('latin-1', errors='ignore')
import re

# Ищем последовательности букв и цифр
words = re.findall(r'[A-Za-z]{3,}', decoded)
if words:
    print("📝 Найденные слова:")
    for word in set(words):
        print(f"   • {word}")

numbers = re.findall(r'\d+', decoded)
if numbers:
    print("\n🔢 Найденные числа:")
    for num in set(numbers):
        if len(num) >= 3:
            print(f"   • {num}")

print("\n" + "="*70)
print("💡 РЕКОМЕНДАЦИИ")
print("="*70)
print("""
Данные выглядят как закодированный/сжатый бинарный формат билета.

Для полной расшифровки нужно:
1. Использовать специализированную библиотеку для UIC 918.3
2. Или загрузить изображение на онлайн-декодер:
   • https://www.bahn-auskunft.de/bin/query.exe/dn (DB онлайн проверка)
   • https://uic-barcode.de/ (специализированный декодер)

Если это Deutschlandticket, попробуйте отсканировать его в приложении
DB Navigator - оно покажет все данные билета.
""")
