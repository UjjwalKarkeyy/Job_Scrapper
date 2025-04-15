from playwright.sync_api import sync_playwright, Playwright

''' Getting all the paths set '''

linkedin_path = "https://www.linkedin.com/jobs/search?keywords=&location=Kathmandu&geoId=100665265&distance=25&f_JT=I&f_TPR=&f_E=1&position=1&pageNum=0"

internsathi_path = "https://internsathi.com/internships?sort=NEWEST"

''' Fetching the content in the form of html from the paths '''

def run(playwright: Playwright):

    brave = playwright.chromium
    browser = brave.launch()

    try:
        # For internsathi
        internsathi_page = browser.new_page()
        internsathi_page.goto(internsathi_path)
        internsathi_page.wait_for_load_state("networkidle") # Waits till all the JS is loaded and there are no request for 500ms
        internsathi_links = internsathi_page.query_selector_all("a")

        # For linkedin
        linkedin_page = browser.new_page()
        linkedin_page.goto(linkedin_path)
        linkedin_close_button = linkedin_page.query_selector("button[aria-label='Dismiss']") # For closing the pop up sign in message in linkedin

        if linkedin_close_button:
            linkedin_close_button.click()
            # linkedin_page.wait_for_timeout()

        linkedin_page.wait_for_load_state("networkidle") # Waits till all the JS is loaded and there are no request for 500ms
        linkedin_links = linkedin_page.query_selector_all(".base-card__full-link")

        if internsathi_links and linkedin_links:

            internsathi_details_page = browser.new_page()
            linkedin_details_page = browser.new_page()

            print("Opportunities at LinkedIn:\n")

            for link in linkedin_links:
                linkedin_href = link.get_attribute("href")

                if linkedin_href:
                    
                    try:
                        
                        linkedin_details_page.goto(linkedin_href)
                        linkedin_details_page.wait_for_load_state("networkidle")

                        linkedin_close_button = linkedin_details_page.query_selector("button[aria-label='Dismiss']")
                        if linkedin_close_button:
                            linkedin_close_button.click(force=True)
                            linkedin_details_page.wait_for_timeout(100)

                    except Exception as e:
                        pass
                    
                    try:
                        linkedin_title = linkedin_details_page.query_selector(".top-card-layout__title").inner_text()
                        linkedin_company = linkedin_details_page.query_selector(".topcard__org-name-link").inner_text()
                        location_el = linkedin_details_page.query_selector(".topcard__flavor.topcard__flavor--bullet")
                        linkedin_location = location_el.inner_text().strip() if location_el else "N/A"
                   
                        print(f"Title: {linkedin_title}\nCompany: {linkedin_company}\nLocation: {linkedin_location}\nApply: {linkedin_href}\n")

                    except AttributeError as e:
                        pass

            print("Opportunities at Internsathi:\n")

            for link in internsathi_links:
                internsathi_href = link.get_attribute("href") 

                if internsathi_href and internsathi_href.startswith("/internships/"):
                    internsathi_full_url = "https://internsathi.com/" + internsathi_href
                    internsathi_details_page.goto(internsathi_full_url)
                    internsathi_details_page.wait_for_load_state("networkidle")

                    internsathi_title = internsathi_details_page.query_selector("p.font-medium").inner_text()
                    internsathi_company = internsathi_details_page.query_selector("a.text-brand-red").inner_text()
                    internsathi_location = internsathi_details_page.query_selector("p.text-t-xs").inner_text().split("\n")[0].strip()

                    print(f"Title: {internsathi_title}\nCompany: {internsathi_company}\nLocation: {internsathi_location}\nApply: {internsathi_full_url}\n")

            internsathi_details_page.close()
            linkedin_details_page.close()

        else:
            print("No <a> tag found!")

    finally:
        browser.close()


# links = [linkedin_path, internsathi_path, internship_in_nepal_path, intern_nepal_path]

with sync_playwright() as playwright:
    run(playwright)
