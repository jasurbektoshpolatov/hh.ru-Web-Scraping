import json
import requests
from bs4 import BeautifulSoup as soup

def get_url_data_science_page(URL):
    return URL

def extract_job_title(item):
    return item.select_one("a.serp-item__title").get_text()


def extract_company_name(item):
    return item.select_one("a.bloko-link.bloko-link_kind-tertiary").get_text()


def extract_job_link(item):
    return item.select_one("a.serp-item__title")['href']


def extract_location(job_clean):
    location = job_clean.select_one("span[data-qa='vacancy-view-raw-address']")
    return location.get_text() if location else "Not indicated"


def extract_required_experience(job_clean):
    job_experience = job_clean.find("p", "vacancy-description-list-item")
    return job_experience.get_text() if job_experience else "No required"


def extract_description(job_clean):
    find_description = job_clean.find("div", "g-user-content")
    return find_description.get_text(strip=True) if find_description else "Description not exists"


def extract_required_skills(job_clean):
    skills = job_clean.find("div", "bloko-tag-list")
    return skills.get_text(strip=True) if skills else "There is no required skills"


def short_informations_about_job(headers_to_get_allows, params):
    informations = []

    session = requests.Session()
    session.headers.update(headers_to_get_allows)

    for page in range(1, 6):  # let's try scrape first 5 pages
        params['page'] = str(page)
        r = session.get(url, params=params)
        clean = soup(r.content, "html.parser")

        for item in clean.findAll("div", "serp-item"):
            job_title = extract_job_title(item)
            name_of_company = extract_company_name(item)
            job_link = extract_job_link(item)

            job_r = session.get(job_link)
            job_clean = soup(job_r.content, "html.parser")

            location = extract_location(job_clean)
            job_experience = extract_required_experience(job_clean)
            description = extract_description(job_clean)
            required_skills = extract_required_skills(job_clean)

            informations.append({"job_title": job_title,
                                 "company_name": name_of_company,
                                 "job_link": job_link,
                                 "location": location,
                                 "required_experience": job_experience,
                                 "description": description,
                                 "required_skills": required_skills})
    with open("hh_ru_scraping.json", "w") as f:
        json.dump(informations, f, indent=4)
    return informations


if __name__ == "__main__":

    # let's output url for the next function
    url = 'https://hh.ru/search/vacancy?text=Data+Scientist&salary=&ored_clusters=true'
    data_science_url = get_url_data_science_page(url)

    # Let's output job title to dump json file
    headers_to_get_allows = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    params = {
        'text': 'Data Scientist',
        'ored_clusters': 'true'}

    informations = short_informations_about_job(headers_to_get_allows, params)