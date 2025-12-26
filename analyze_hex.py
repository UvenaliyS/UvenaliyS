#!/usr/bin/env python3
"""
Анализатор hex-данных из Aztec кода
"""

# Hex данные от пользователя
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

# Очищаем данные
hex_clean = hex_data.replace('\n', '').replace(' ', '').strip()

# Конвертируем в байты
data_bytes = bytes.fromhex(hex_clean)

print("="*70)
print("📊 АНАЛИЗ HEX-ДАННЫХ ИЗ AZTEC КОДА")
print("="*70)
print(f"\n📏 Размер данных: {len(data_bytes)} байт")
print()

# Пытаемся декодировать как UTF-8
print("-"*70)
print("🔤 ПОПЫТКА ДЕКОДИРОВАНИЯ КАК UTF-8:")
print("-"*70)
try:
    decoded_utf8 = data_bytes.decode('utf-8')
    print(decoded_utf8)
except UnicodeDecodeError as e:
    print(f"❌ Ошибка UTF-8 декодирования: {e}")
    print("⚠️  Данные содержат не-UTF8 байты")

# Пытаемся декодировать как Latin-1 (ISO-8859-1)
print("\n" + "-"*70)
print("🔤 ПОПЫТКА ДЕКОДИРОВАНИЯ КАК LATIN-1 (ISO-8859-1):")
print("-"*70)
try:
    decoded_latin1 = data_bytes.decode('latin-1')
    print(decoded_latin1)
    print()
    # Показываем читаемые символы
    readable = ''.join(c if c.isprintable() else '.' for c in decoded_latin1)
    print("Читаемые символы:")
    print(readable)
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Пытаемся декодировать как Windows-1252
print("\n" + "-"*70)
print("🔤 ПОПЫТКА ДЕКОДИРОВАНИЯ КАК WINDOWS-1252:")
print("-"*70)
try:
    decoded_cp1252 = data_bytes.decode('cp1252', errors='ignore')
    print(decoded_cp1252)
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Анализируем структуру
print("\n" + "-"*70)
print("🔍 АНАЛИЗ СТРУКТУРЫ ДАННЫХ:")
print("-"*70)

# Ищем ASCII строки (последовательности печатных символов длиной >= 4)
print("\n📝 Найденные ASCII строки (длина >= 4):")
current_string = []
for byte in data_bytes:
    if 32 <= byte <= 126:  # Печатные ASCII символы
        current_string.append(chr(byte))
    else:
        if len(current_string) >= 4:
            print(f"   • {''.join(current_string)}")
        current_string = []
if len(current_string) >= 4:
    print(f"   • {''.join(current_string)}")

# Показываем первые байты в разных форматах
print("\n" + "-"*70)
print("📊 ПЕРВЫЕ 32 БАЙТА В РАЗНЫХ ФОРМАТАХ:")
print("-"*70)
print(f"HEX:    {data_bytes[:32].hex(' ')}")
print(f"DEC:    {' '.join(f'{b:3d}' for b in data_bytes[:32])}")
print(f"ASCII:  {' '.join(chr(b) if 32 <= b <= 126 else '.' for b in data_bytes[:32])}")

# Ищем паттерны
print("\n" + "-"*70)
print("🔎 ПОИСК ИЗВЕСТНЫХ ПАТТЕРНОВ:")
print("-"*70)

# Ищем маркеры UIC билетов
uic_markers = [b'#V1#', b'#UT', b'U_TLAY', b'U_HEAD', b'080BL']
for marker in uic_markers:
    if marker in data_bytes:
        idx = data_bytes.index(marker)
        print(f"✅ Найден UIC маркер: {marker.decode('latin-1')} на позиции {idx}")
        # Показываем контекст
        context_start = max(0, idx - 10)
        context_end = min(len(data_bytes), idx + 30)
        context = data_bytes[context_start:context_end]
        print(f"   Контекст: {context}")

# Ищем числа (последовательности цифр)
import re
latin1_str = data_bytes.decode('latin-1', errors='ignore')
numbers = re.findall(r'\d{4,}', latin1_str)
if numbers:
    print(f"\n🔢 Найденные числа (4+ цифры):")
    for num in numbers[:10]:  # Первые 10
        print(f"   • {num}")

# Показываем hex dump в красивом формате
print("\n" + "="*70)
print("📋 HEX DUMP (первые 256 байт):")
print("="*70)
for i in range(0, min(256, len(data_bytes)), 16):
    hex_part = ' '.join(f'{b:02x}' for b in data_bytes[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data_bytes[i:i+16])
    print(f"{i:04x}  {hex_part:<48}  {ascii_part}")

print("\n" + "="*70)
