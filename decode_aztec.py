#!/usr/bin/env python3
"""
Aztec Barcode Decoder
Декодирует Aztec штрихкоды из изображений
"""

import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
    from pyzbar import pyzbar
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Установите зависимости: pip install -r requirements.txt")
    sys.exit(1)


def decode_aztec(image_path):
    """
    Декодирует Aztec-код из изображения

    Args:
        image_path: путь к файлу изображения

    Returns:
        list: список декодированных данных
    """
    try:
        # Загружаем изображение
        img = Image.open(image_path)

        # Декодируем все штрихкоды на изображении
        decoded_objects = pyzbar.decode(img)

        if not decoded_objects:
            print("⚠️  Штрихкоды не найдены на изображении")
            return []

        results = []
        for obj in decoded_objects:
            # Извлекаем данные
            barcode_type = obj.type
            barcode_data = obj.data.decode('utf-8', errors='ignore')

            result = {
                'type': barcode_type,
                'data': barcode_data,
                'raw_data': obj.data,
                'rect': obj.rect,
                'polygon': obj.polygon
            }
            results.append(result)

        return results

    except FileNotFoundError:
        print(f"❌ Файл не найден: {image_path}")
        return []
    except Exception as e:
        print(f"❌ Ошибка при обработке изображения: {e}")
        return []


def print_results(results):
    """Красиво выводит результаты декодирования"""
    if not results:
        return

    print("\n" + "="*60)
    print("🔍 РЕЗУЛЬТАТЫ ДЕКОДИРОВАНИЯ")
    print("="*60)

    for i, result in enumerate(results, 1):
        print(f"\n📊 Штрихкод #{i}")
        print(f"   Тип: {result['type']}")
        print(f"   Позиция: {result['rect']}")
        print("\n" + "-"*60)
        print("📝 Декодированные данные:")
        print("-"*60)
        print(result['data'])
        print("-"*60)

        # Попытка распарсить данные, если это структурированный формат
        data = result['data']
        if '\n' in data or ';' in data:
            print("\n📋 Структурированные данные:")
            lines = data.replace(';', '\n').split('\n')
            for line in lines:
                if line.strip():
                    print(f"   • {line.strip()}")

        print()


def main():
    parser = argparse.ArgumentParser(
        description='Декодирует Aztec и другие штрихкоды из изображения',
        epilog='Пример: python decode_aztec.py ticket.png'
    )
    parser.add_argument('image', help='Путь к изображению со штрихкодом')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Подробный вывод')
    parser.add_argument('-o', '--output', help='Сохранить результат в файл')

    args = parser.parse_args()

    # Проверяем файл
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Файл не существует: {image_path}")
        return 1

    print(f"🔍 Обрабатываю изображение: {image_path}")

    # Декодируем
    results = decode_aztec(image_path)

    # Выводим результаты
    print_results(results)

    # Сохраняем в файл если указано
    if args.output and results:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"Type: {result['type']}\n")
                    f.write(f"Data: {result['data']}\n")
                    f.write("\n" + "="*60 + "\n\n")
            print(f"✅ Результаты сохранены в: {args.output}")
        except Exception as e:
            print(f"⚠️  Не удалось сохранить в файл: {e}")

    return 0 if results else 1


if __name__ == '__main__':
    sys.exit(main())
