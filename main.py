from api import get_vacancies, get_employer
from database import create_database, create_tables, save_data
from db_manager import DBManager
import psycopg2


def main():
    # Database connection parameters
    dbname = 'hh_vacancies'
    user = 'postgres'
    password = 'damir_999'
    host = 'localhost'

    # Create database and tables
    create_database(dbname, user, password, host)
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    create_tables(conn)

    # List of company IDs (replace with actual company IDs)
    company_ids = ['1740', '2180', '3529', '15478', '78638', '87021', '740', '2748', '3776', '3127']

    # Fetch data from API
    employers_data = {}
    for company_id in company_ids:
        employer_info = get_employer(company_id)
        if employer_info:
            employers_data[company_id] = employer_info

    vacancies_data = get_vacancies(company_ids)

    # Save data to database
    save_data(conn, employers_data, vacancies_data)

    # Create DBManager instance
    db_manager = DBManager(dbname, user, password, host)

    # Use DBManager methods to interact with the data
    print("Companies and vacancy counts:")
    for company, count in db_manager.get_companies_and_vacancies_count():
        print(f"{company}: {count} vacancies")

    print("\nAll vacancies:")
    for vacancy in db_manager.get_all_vacancies():
        print(vacancy)

    avg_salary = db_manager.get_avg_salary()
    print(f"\nAverage salary: {avg_salary:.2f}")

    print("\nVacancies with higher than average salary:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    keyword = input("\nEnter a keyword to search for vacancies: ")
    print(f"\nVacancies with keyword '{keyword}':")
    for vacancy in db_manager.get_vacancies_with_keyword(keyword):
        print(vacancy)

    # Close connections
    db_manager.close()
    conn.close()


if __name__ == '__main__':
    main()
