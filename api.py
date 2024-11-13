import requests


# Fetch vacancies multiple companies
def get_vacancies(company_ids):
    all_vacancies = {}
    for company_id in company_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={company_id}'
        response = requests.get(url)
        if response.status_code == 200:
            all_vacancies[company_id] = response.json()
        else:
            print(f"Error fetching data for company {company_id}: {response.status_code}")
    return all_vacancies


# Fetch details for a single employer
def get_employer(employer_id):
    url = f'https://api.hh.ru/employers/{employer_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching employer data for {employer_id}: {response.status_code}")
        return None
