import numpy as np
import pandas as pd

# 1. Загрузка данных
df = pd.read_csv('dirty_sales.csv')

# 2. Первичный обзор данных
print("-" * 100)
print("=== Обзор данных ===".center(70))
print(df.head(5))
print("-" * 100)
print(df.info())
print("-" * 100)
print(df.describe())
print("-" * 100)
print("-" * 100)

print("=== Стандартизация форматов текста и даты ===".center(70))
# 3. Стандартизируем названия колонок: убираем пробелы и переводим в нижний регистр
print(f"\nПроверка названий колонок:\n{df.columns}")
df.columns = df.columns.str.strip().str.lower()
print("[OK] Названия колонок приведены к нижнему регистру без пробелов")

# 4. Исправление формата даты
print("\nУникальные форматы дат в файле:")
# Поиск уникальных шаблонов дат через маскирование цифр регулярным выражением
# Примечание: также эту проверку шаблонов можно выполнить с помощью цикла for и условий 'in' / 'not in'
print(df['order_date'].str.replace(r'\d', 'X', regex=True).value_counts())
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, format='mixed')
print("[OK] Даты приведены к единому стандарту datetime")

print("-" * 100)
print("-" * 100)

# 5. Проверяем пропуски и дубликаты
print("=== Работа с пропусками и дубликатами ===".center(70))
print(f"Кол-во пропусков:\n{df.isnull().sum()}")
print(f"\nКол-во дубликатов: {df.duplicated().sum()}")

# === Очистка данных ===
df = df.drop_duplicates()
print("\n[OK] Дубликаты успешно удалены")

# 6. Удаляем строки с отрицательными значениями (которые мы увидели в describe)
df = df[df['quantity'] > 0]
df = df[df['unit_price'] > 0]
print("[OK] Строки с отрицательным количеством и ценой удалены")

# 7. Работа с пропусками
# Регион заполняем 'Unknown', чтобы сохранить факт продажи и выручку в общих отчётах
df['region'] = df['region'].fillna('Unknown')
# Строки без цены удаляем: без цены нельзя посчитать выручку, а придумывать финансовые данные нельзя
df = df.dropna(subset=['unit_price'])
print("[OK] Пропуски в регионе заполнены на 'Unknown', строки без цены удалены")

# 8. Убираем лишние пробелы в тексте и исправляем регистр значений
text_columns = ['customer_name', 'region', 'category', 'product_name']
for col in text_columns:
    df[col] = df[col].str.strip().str.title()
print("[OK] Текстовые поля очищены от пробелов и приведены к формату Title Case")

# 9. Сортируем данные по дате заказа от старых к новым
df = df.sort_values('order_date')
print("[OK] Данные отсортированы по дате заказа")

print("-" * 100)
print("-" * 100)

# 10. Финальный просмотр и сохранение чистого файла
print("=== Контроль качества данных (Data Quality Check) ===".center(70))
print(f"Осталось строк: {df.shape[0]}, колонок: {df.shape[1]}")
print(f"Кол-во дубликатов: {df.duplicated().sum()}")
print(f"\nКол-во пропусков:\n{df.isnull().sum()}")
print(f"\nМинимальное количество: {df['quantity'].min()}")
print(f"Минимальная цена: {df['unit_price'].min()}")

df.to_csv('clean_sales.csv', index=False)
print("\n[OK] Готово! Файл clean_sales.csv успешно сохранен.")
