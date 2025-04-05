import requests
from bs4 import BeautifulSoup

page = requests.get("https://realpython.github.io/fake-jobs/")

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id = "ResultsContainer")

# print(results.prettify())

job_cards = results.find_all("div", class_="card-content")

# for job_card in job_cards:

#     print(job_card, end = "\n" * 2)

# for job_card in job_cards:

#     title_ele = job_card.find("h2", class_ = "title")
#     company_ele = job_card.find("h3", class_ = "company")
#     location_ele = job_card.find("p", class_ = "location")

#     print(title_ele.text.strip())
#     print(company_ele.text.strip())
#     print(location_ele.text.strip())

python_jobs = results.find_all("h2", string = lambda text: 'python' in text.lower())

python_job_cards = [h2_element.parent.parent.parent for h2_element in python_jobs]

for job_card in python_job_cards:

    title = job_card.find("h2", class_ = "title")
    company = job_card.find("h3", class_ = "company")
    location = job_card.find("p", class_ = "location")
    link_url = job_card.find_all("a")[1]["href"]

    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print(link_url)
    print()