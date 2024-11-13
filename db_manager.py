import psycopg2


class DBManager:
    # Initialize database connection
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.conn.autocommit = True

    # Get the count of vacancies for each company
    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    # Get all vacancies with company name, salary, and URL
    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    # Calculate the average salary of all vacancies
    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    # Get vacancies with salary higher than average
    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id 
                WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 > %s
            """, (avg_salary,))
            return cur.fetchall()

    # Search for vacancies by keyword
    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.title ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()

    def close(self):
        self.conn.close()
