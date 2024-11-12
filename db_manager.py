import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT e.name, COUNT(v.id) 
        FROM employers e
        LEFT JOIN vacancies v ON e.id = v.employer_id
        GROUP BY e.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT e.name AS employer_name, v.title AS vacancy_name, v.salary_to AS salary, v.url 
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = "SELECT AVG(salary_to) FROM vacancies;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []  # Возвращаем пустой список, если нет зарплат
        query = """
        SELECT e.name AS employer_name, v.title, v.salary_to AS salary, v.url 
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.id 
        WHERE v.salary_to > %s;  -- Исправлено на v.salary_to
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        query = """
        SELECT e.name AS employer_name, v.title AS vacancy_name, v.salary_to AS salary, v.url 
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.id
        WHERE v.title ILIKE %s;  -- Исправлено на v.title
        """
        self.cursor.execute(query, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
