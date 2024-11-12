import logging
from database import save_data
from db_manager import DBManager  # Импортируем ваш класс DBManager

# Настройка логирования (можно оставить, если нужно для отладки)
logging.basicConfig(level=logging.INFO)


def main():
    # Параметры подключения к базе данных
    dbname = 'postgres'
    user = 'postgres'
    password = 'damir_999'
    host = 'localhost'

    # Создание экземпляра DBManager
    db_manager = DBManager(dbname, user, password, host)

    try:
        # Получение количества вакансий по компаниям
        print("Получение количества вакансий по компаниям...")
        companies_and_counts = db_manager.get_companies_and_vacancies_count()
        for company, count in companies_and_counts:
            print(f"Компания: {company}, Количество вакансий: {count}")

        # Получение всех вакансий
        print("\nПолучение всех вакансий...")
        all_vacancies = db_manager.get_all_vacancies()
        for employer_name, vacancy_name, salary, url in all_vacancies:
            print(f"Работодатель: {employer_name}, Вакансия: {vacancy_name}, Зарплата: {salary}, URL: {url}")

        # Получение средней зарплаты
        print("\nПолучение средней зарплаты...")
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата: {avg_salary}")

        # Получение вакансий с зарплатой выше средней
        print("\nПолучение вакансий с зарплатой выше средней...")
        higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        for employer_name, vacancy_name, salary, url in higher_salary_vacancies:
            print(f"Работодатель: {employer_name}, Вакансия: {vacancy_name}, Зарплата: {salary}, URL: {url}")

        # Поиск вакансий по ключевому слову
        keyword = input("\nВведите ключевое слово для поиска вакансий: ")
        print(f"\nПоиск вакансий с ключевым словом '{keyword}'...")
        keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
        for employer_name, vacancy_name, salary, url in keyword_vacancies:
            print(f"Работодатель: {employer_name}, Вакансия: {vacancy_name}, Зарплата: {salary}, URL: {url}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        db_manager.close()  # Закрываем соединение с базой данных


if __name__ == '__main__':
    main()
