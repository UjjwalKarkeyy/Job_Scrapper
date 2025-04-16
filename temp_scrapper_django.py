from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

scrap_site = {

    "internepal" : {

        "main_link" : "https://internepal.com.np/vacancy-list?type=internship",
        "query_selector": "div.category_box div.view_more_apply_btn a",
        "dismiss_btn": "button[aria-label='Dismiss']",
        "title": "div.main_information_des_badge h6",
        "company": "div.company_name_badge",
        "location": "div.location",
    },

    "internsathi" : {

        "main_link" : "https://internsathi.com/internships?sort=NEWEST",
        "query_selector": "a",
        "title": "p.font-medium",
        "company": "a.text-brand-red",
        "location": "p.text-t-xs",
        "application_deadline": "div.sm\\:w-auto.w-full p.mt-4 + p.font-medium",
    },
}

def run(playwright: Playwright):

    chrome = playwright.chromium
    browser = chrome.launch()
    try:
        for site in scrap_site:

                page = browser.new_page()
                page.goto(scrap_site[site]["main_link"])

                try:
                    page.wait_for_load_state("networkidle")
                    page_links = page.query_selector_all(scrap_site[site]["query_selector"])

                except PlaywrightTimeoutError as e:
                    print("Error: ", e)
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
                        
                        except PlaywrightTimeoutError as e:
                            print("Error: ", e)
                            continue

                        try:

                            title_el = details_page.query_selector(scrap_site[site]["title"]).inner_text() 
                            company_el = details_page.query_selector(scrap_site[site]["company"]).inner_text()
                            location_el = details_page.query_selector(scrap_site[site]["location"])

                            if site == "internepal":
                                
                                deadline_el = details_page.eval_on_selector_all( 
                                                ".duration_icons",
                                                "elements => elements[2][1]")

                            else:
                                deadline_el = details_page.query_selector(scrap_site[site]["application_deadline"])
                            
                            print(deadline_el.inner_text())


                            title = title_el if title_el else "N/A"
                            company = company_el if company_el else "N/A"
                            location = location_el.inner_text().split("\n")[0].strip() if location_el else "N/A" 
                            deadline = deadline_el.inner_text() if deadline_el else "N/A" 
                            print(deadline)
                            # print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nApply: {href}\nDeadline: {deadline}\n")

                        except AttributeError as e:
                            print("Error: ", e)
                            continue

                else:
                    print("Link not Found!")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
