from locale import currency

import requests
import json
import os

def get_vacancies_habr_api(query="Python"):
    url = "https://career.habr.com/api/frontend/vacancies"
    params = {
        "q": query,
        "type": "all",
        "page": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://career.habr.com/vacancies"
    }

    print(f"Запрашиваем вакансии '{query}' через API Хабр Карьеры.")

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("list", [])
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

def get_salary_value(salary_info):
    """Возвращает числовое значение зарплаты для сравнения (берет 'from')."""
    if not salary_info or not isinstance(salary_info, dict):
        return 0
    # Если есть 'from', берем его. Если нет, но есть 'to', берем 'to' (как минимум)
    return salary_info.get("from") or salary_info.get("to") or 0

def format_salary(salary_info):
    if not salary_info or not isinstance(salary_info, dict):
        return "Не указана"
    salary_from = salary_info.get("from")
    salary_to = salary_info.get("to")
    currency = salary_info.get("currency", "руб.")

    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} {currency}"
    elif salary_from:
        return f"от {salary_from} {currency}"
    elif salary_to:
        return f"до {salary_to} {currency}"
    return "Не указана"

def save_to_json(vacancies, filename="vacancies.json"):
    """Сохраняет список вакансий в JSON файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)
    print(f"\n[+] Данные сохранены в файл '{filename}'")

def show_vacancies(vacancies, min_salary=0):
    if not vacancies:
        print("Вакансий не найдено.")
        return

    filtered = []
    for v in vacancies:
        salary_val = get_salary_value(v.get("salary"))
        # Если указана минималка и зарплата меньше (или не указана), пропускаем
        if min_salary > 0 and salary_val < min_salary:
            continue
        filtered.append(v)

    if not filtered:
        print(f"\nВакансий с зарплатой от {min_salary} не найдено.")
        return

    print(f"\n--- Найдено вакансий (после фильтра): {len(filtered)} ---")
    print(f"{'Название':<40} | {'Компания':<25} | {'Зарплата'}")
    print("-" * 85)

    for v in filtered:
        title = v.get("title", "Без названия")[:38]
        company = v.get("company", {}).get("title", "Без компании")[:23]
        salary = format_salary(v.get("salary"))
        print(f"{title:<40} | {company:<25} | {salary}")

    return filtered

if __name__ == "__main__":
    # Настройки
    QUERY = "Python"
    MIN_SALARY = 0  # Фильтр: ищем от 0 руб.

    # 1. Получаем данные
    found = get_vacancies_habr_api(QUERY)

    # 2. Выводим и фильтруем
    filtered_found = show_vacancies(found, min_salary=MIN_SALARY)

    # 3. Сохраняем в JSON (сохраняем отфильтрованные)
    if filtered_found:
        save_to_json(filtered_found)
    else:
        print("Нечего сохранять.")