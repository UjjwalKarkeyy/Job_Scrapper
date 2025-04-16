from playwright.sync_api import sync_playwright, Playwright

''' Getting all the paths set '''

linkedin_path = "https://www.linkedin.com/jobs/search?keywords=&location=Kathmandu&geoId=100665265&distance=25&f_JT=I&f_TPR=&f_E=1&position=1&pageNum=0"

internsathi_path = "https://internsathi.com/internships?sort=NEWEST"

scrap_site = {

    "internsathi" : {

        "main_link" : "https://internsathi.com/internships?sort=NEWEST",
        "query_selector": "a",
        "title": "p.font-medium",
        "company": "a.text-brand-red",
        "location": "p.text-t-xs",
    },

    "linkedin" : {

        "main_link" :  "https://www.linkedin.com/jobs/search?keywords=&location=Kathmandu&geoId=100665265&distance=25&f_JT=I&f_TPR=&f_E=1&position=1&pageNum=0",
        "query_selector": ".base-card__full-link",
        "dismiss_btn": "button[aria-label='Dismiss']",
        "title": ".top-card-layout__title",
        "company": ".topcard__org-name-link",
        "location": ".topcard__flavor.topcard__flavor--bullet",
    },
}

def run(playwright: Playwright):

    chrome = playwright.chromium
    browser = chrome.launch()
    try:
        for site in scrap_site:

                page = browser.new_page()
                page.goto(scrap_site[site]["main_link"])

                if page.is_visible('div#base-contextual-sign-in-modal section[aria-modal="true"]'):

                    linkedin_close_button = page.query_selector(scrap_site[site]["dismiss_btn"]) # For closing the pop up sign in message in linkedin

                    if linkedin_close_button:
                        linkedin_close_button.click()
                try:
                    page.wait_for_load_state("networkidle")
                    page_links = page.query_selector_all(scrap_site[site]["query_selector"])

                except TimeoutError as e:
                    continue

                if page_links:
                    details_page = browser.new_page()

                    print(f"Opportunities in {site} site:\n")

                    for link in page_links:
                        href = link.get_attribute("href")

                        if site == "internsathi" and href.startswith("/internships/"):
                            href = "https://internsathi.com" + href

                        elif site == "internsathi":
                            continue
                        
                        try:
                            details_page.goto(href) 
                            details_page.wait_for_load_state("networkidle")   
                        
                        except TimeoutError as e:
                            continue

                        if page.is_visible('div#base-contextual-sign-in-modal section[aria-modal="true"]'):

                            linkedin_close_button = page.query_selector(scrap_site[site]["dismiss_btn"]) # For closing the pop up sign in message in linkedin

                            if linkedin_close_button:
                                linkedin_close_button.click(force=True)
                                details_page.wait_for_timeout(1000)  

                        if site == "linkedin":    
                            location_el = details_page.query_selector(scrap_site[site]["location"])
                            location = location_el.inner_text().strip() if location_el else "N/A"

                        else:
                            location_el = details_page.query_selector(scrap_site[site]["location"])
                            location = location_el.inner_text().split("\n")[0].strip() if location_el else "N/A"
                        
                        try:

                            title_el = details_page.query_selector(scrap_site[site]["title"]).inner_text() 
                            company_el = details_page.query_selector(scrap_site[site]["company"]).inner_text() 

                            title = title_el if title_el else "N/A"
                            company = company_el if company_el else "N/A"

                            print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nApply: {href}\n")

                        except AttributeError as e:
                            continue

                else:
                    print("Link not Found!")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
