import psycopg2


def insert_employer(cursor, employer):
    cursor.execute("""
        INSERT INTO employers (hh_id, name, url) 
        VALUES (%s, %s, %s)
        ON CONFLICT (hh_id) DO NOTHING
    """, (employer['id'], employer['name'], employer['url']))


def insert_vacancy(cursor, vacancy, employer_id):
    cursor.execute("""
        INSERT INTO vacancies (hh_id, title, employer_id, salary_min, salary_max, published_at, description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (hh_id) DO NOTHING
    """, (vacancy['id'], vacancy['name'], employer_id, vacancy.get('salary', {}).get('from'),
          vacancy.get('salary', {}).get('to'), vacancy['published_at'], vacancy['description']))


def save_data(vacancies_data):
    connection = psycopg2.connect(
        dbname='postgres', user='postgres', password='damir_999', host='localhost'
    )
    cursor = connection.cursor()

    for company_id, vacancies in vacancies_data.items():
        employer = {
            'id': vacancies['employer']['id'],
            'name': vacancies['employer']['name'],
            'url': vacancies['employer']['url']
        }
        insert_employer(cursor, employer)
        cursor.execute("SELECT id FROM employers WHERE hh_id = %s", (employer['id'],))
        employer_id = cursor.fetchone()[0]

        for vacancy in vacancies['items']:
            insert_vacancy(cursor, vacancy, employer_id)

    connection.commit()
    cursor.close()
    connection.close()
