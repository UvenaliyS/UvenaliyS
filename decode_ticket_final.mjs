#!/usr/bin/env node
/**
 * Декодер UIC 918.3 билетов (Deutschlandticket)
 * Использует библиотеку uic-918-3
 */

import { interpretBarcode } from 'uic-918-3';

// Hex данные от пользователя
const hexData = `
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
`.replace(/\s+/g, '');

console.log('='.repeat(70));
console.log('🎫 ДЕКОДЕР DEUTSCHLANDTICKET UIC 918.3');
console.log('='.repeat(70));

try {
  // Конвертируем hex в Buffer
  const buffer = Buffer.from(hexData, 'hex');

  console.log(`\n📊 Размер данных: ${buffer.length} байт`);
  console.log(`🔐 Формат: UIC 918.3 (версия 0x${buffer[0].toString(16)})\n`);

  // Декодируем билет
  console.log('🔍 Декодирование билета...\n');
  const result = await interpretBarcode(buffer, false); // false = не проверять подпись

  // Красиво выводим результат
  console.log('='.repeat(70));
  console.log('✅ ДЕКОДИРОВАННЫЕ ДАННЫЕ БИЛЕТА');
  console.log('='.repeat(70));

  console.log('\n📝 Полные данные билета:');
  console.log(JSON.stringify(result, null, 2));

  console.log('\n' + '='.repeat(70));
  console.log('✅ Декодирование успешно завершено!');
  console.log('='.repeat(70));

} catch (error) {
  console.error('\n❌ ОШИБКА ПРИ ДЕКОДИРОВАНИИ:');
  console.error(error.message);
  console.error('\n📋 Детали ошибки:');
  console.error(error.stack);

  console.log('\n' + '='.repeat(70));
  console.log('💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:');
  console.log('='.repeat(70));
  console.log(`
  1. Данные могут быть повреждены при сканировании
  2. Формат может отличаться от стандартного UIC 918.3
  3. Может требоваться декомпрессия или предварительная обработка
  4. Библиотека может не поддерживать этот конкретный вариант формата

  Попробуйте:
  - Отсканировать билет заново в лучшем качестве
  - Использовать официальное приложение DB Navigator
  - Проверить билет на https://www.bahn.de
  `);
}

console.log('\n' + '='.repeat(70));
console.log('📚 ИСТОЧНИКИ:');
console.log('='.repeat(70));
console.log('• GitHub: https://github.com/justusjonas74/uic-918-3');
console.log('• NPM: https://www.npmjs.com/package/uic-918-3');
console.log('='.repeat(70));
