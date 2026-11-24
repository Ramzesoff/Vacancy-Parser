import requests
from bs4 import BeautifulSoup


def get_vacancies_habr_html(query="Python"):
    # Адрес страницы поиска вакансий на Хабр Карьере
    url = f"https://career.habr.com/vacancies?q={query}&type=all"

    # Заголовки, чтобы сайт не думал, что мы бот
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Парсим HTML с Хабр Карьеры по запросу '{query}' (v1.0)...")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        vacancies = []

        # Ищем карточки вакансий. На Хабре они лежат в <div class="vacancy-card">
        cards = soup.find_all("div", class_="vacancy-card")

        for card in cards:
            # Название вакансии
            title_tag = card.find("a", class_="vacancy-card__title-link")
            title = title_tag.text.strip() if title_tag else "Без названия"

            # Компания
            company_tag = card.find("div", class_="vacancy-card__company-title")
            company = company_tag.text.strip() if company_tag else "Без компании"

            # Зарплата (если указана)
            salary_tag = card.find("div", class_="vacancy-card__salary")
            salary = salary_tag.text.strip() if salary_tag else "З/П не указана"

            vacancies.append({
                "title": title,
                "company": company,
                "salary": salary
            })

        return vacancies

    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return []


def show_vacancies(vacancies):
    if not vacancies:
        print("\nВакансий не найдено. Возможно, Хабр изменил верстку.")
        return

    print(f"\n--- Найдено вакансий: {len(vacancies)} ---")
    print(f"{'Название':<35} | {'Компания':<25} | {'Зарплата'}")
    print("-" * 80)

    for v in vacancies[:10]:  # Показываем первые 10 для примера
        title = v['title'][:33]
        company = v['company'][:23]
        salary = v['salary']
        print(f"{title:<35} | {company:<25} | {salary}")


if __name__ == "__main__":
    found = get_vacancies_habr_html("Python")
    show_vacancies(found)
