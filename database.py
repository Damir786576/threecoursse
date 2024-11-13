import psycopg2


# Create a new database
def create_database(database_name, user, password, host):
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()


# Create employers and vacancies tables
def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE,
                name VARCHAR(255),
                url TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE,
                title VARCHAR(255),
                employer_id INTEGER REFERENCES employers(id),
                salary_from INTEGER,
                salary_to INTEGER,
                url TEXT
            )
        """)
    conn.commit()


# Update employer data
def insert_employer(cur, employer):
    cur.execute("""
        INSERT INTO employers (hh_id, name, url) 
        VALUES (%s, %s, %s)
        ON CONFLICT (hh_id) DO UPDATE SET
            name = EXCLUDED.name,
            url = EXCLUDED.url
        RETURNING id
    """, (employer['id'], employer['name'], employer['alternate_url']))
    return cur.fetchone()[0]


# Update vacancy data
def insert_vacancy(cur, vacancy, employer_id):
    salary_from = vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary']['from'] else None
    salary_to = vacancy['salary']['to'] if vacancy['salary'] and vacancy['salary']['to'] else None

    cur.execute("""
        INSERT INTO vacancies (hh_id, title, employer_id, salary_from, salary_to, url) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (hh_id) DO UPDATE SET
            title = EXCLUDED.title,
            salary_from = EXCLUDED.salary_from,
            salary_to = EXCLUDED.salary_to,
            url = EXCLUDED.url
    """, (vacancy['id'], vacancy['name'], employer_id, salary_from, salary_to, vacancy['alternate_url']))


# Save both employer and vacancy data
def save_data(conn, employers_data, vacancies_data):
    with conn.cursor() as cur:
        for employer_id, employer_info in employers_data.items():
            employer_db_id = insert_employer(cur, employer_info)
            if employer_id in vacancies_data:
                for vacancy in vacancies_data[employer_id]['items']:
                    insert_vacancy(cur, vacancy, employer_db_id)

    conn.commit()
