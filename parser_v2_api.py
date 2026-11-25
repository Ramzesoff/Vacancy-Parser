from locale import currency

import requests


def get_vacancies_habr_api(query="Python"):
    # Публичное API Хабр Карьеры для списка вакансий
    url = "https://career.habr.com/api/frontend/vacancies"

    params = {
        "q": query,
        "type": "all",
        "page": 1
    }

    # Эти заголовки помогают избежать блокировок и показывают, что мы ожидаем JSON
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

        # В ответе JSON список вакансий лежит в ключе 'list'
        vacancies = data.get("list", [])
        return vacancies

    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

def format_salary(salary_info):
    """Красиво форматирует зарплату из JSON Хабр Карьеры."""
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

def show_vacancies(vacancies):
    if not vacancies:
        print("Вакансий не найдено.")
        return

    print(f"\n--- Найдено вакансий: {len(vacancies)} ---")
    print(f"{'Название':<40} | {'Компания':<25} | {'Зарплата'}")
    print("-" * 85)

    for v in vacancies:
        # Данные в API Хабр Карьеры лежат прямо в объекте вакансии
        title = v.get("title", "Без названия")[:38]
        company = v.get("company", {}).get("title", "Без названия")[:23]
        salary = format_salary(v.get("salary"))

        print(f"{title:<40} | {company:<25} | {salary}")

if __name__ == "__main__":
    found = get_vacancies_habr_api("Python")
    show_vacancies(found)