import os
import django
import asyncio
import subprocess
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_finder.scrapper_settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from main.models import Internships

Internships.objects.all().delete()

scrap_site = {
    "internepal": {
        "main_link": "https://internepal.com.np/vacancy-list?type=internship",
        "query_selector": "div.category_box div.view_more_apply_btn a",
        "dismiss_btn": "button[aria-label='Dismiss']",
        "title": "div.main_information_des_badge h6",
        "company": "div.company_name_badge",
        "location": "div.location",
        "application_deadline": "div.duration_stippned_application",
    },
    "internsathi": {
        "main_link": "https://internsathi.com/internships?sort=NEWEST",
        "query_selector": "a",
        "title": "p.font-medium",
        "company": "a.text-brand-red",
        "location": "p.text-t-xs",
        "application_deadline": "div.sm\\:w-auto.w-full p.mt-4 + p.font-medium",
    },
}

async def run(playwright):

    flag = False
    browser = await playwright.chromium.launch(headless=True)
    try:
        for site in scrap_site:
            page = await browser.new_page()
            await page.goto(scrap_site[site]["main_link"])

            try:
                await page.wait_for_load_state("networkidle")
                page_links = await page.query_selector_all(scrap_site[site]["query_selector"])
            except PlaywrightTimeoutError as e:
                print("Error: ", e)
                continue

            if page_links:
                for link in page_links:
                    href = await link.get_attribute("href")
                    if not href:
                        continue

                    if site == "internsathi" and href.startswith("/internships/"):
                        href = "https://internsathi.com" + href
                    elif site == "internsathi":
                        continue

                    try:
                        details_page = await browser.new_page()
                        await details_page.goto(href)
                        await details_page.wait_for_load_state("networkidle")
                    except PlaywrightTimeoutError as e:
                        print("Timeout Error: ", e)
                        continue

                    try:
                        title_el = await details_page.query_selector(scrap_site[site]["title"])
                        company_el = await details_page.query_selector(scrap_site[site]["company"])
                        location_el = await details_page.query_selector(scrap_site[site]["location"])

                        title = await title_el.inner_text() if title_el else "N/A"
                        company = await company_el.inner_text() if company_el else "N/A"
                        location = await location_el.inner_text() if location_el else "N/A"
                        location = location.split("\n")[0].strip()

                        if site == "internepal":
                            deadline = await page.evaluate("""() => {
                                const icons = document.querySelectorAll('.duration_icons');
                                if (icons.length < 3) return null;
                                const durationsDiv = icons[2].querySelector('.durations');
                                if (!durationsDiv) return null;
                                const match = durationsDiv.textContent.match(/\\d{4}-\\d{2}-\\d{2}/);
                                return match ? match[0] : null;
                            }""")
                        else:
                            deadline_el = await details_page.query_selector(scrap_site[site]["application_deadline"])
                            raw_deadline = await deadline_el.inner_text() if deadline_el else None
                            try:
                                deadline = datetime.strptime(raw_deadline.strip(), "%B %d, %Y").date() if raw_deadline else None
                            except ValueError:
                                deadline = None

                        # Check for duplicate and save
                        if not Internships.objects.filter(apply=href).exists():
                            Internships.objects.create(
                                title=title,
                                company=company,
                                location=location,
                                deadline=deadline,
                                apply=href
                            )
                            flag = True

                    except Exception as e:
                        print("Error while processing job:", e)
                        continue
            else:
                print("No links found!")

    except Exception as e:
        print("Global Error:", e)

    finally:
        await browser.close()

    return flag

async def main():
    async with async_playwright() as playwright:
        return await run(playwright)

# Entry point
if __name__ == "__main__":
    flag = asyncio.run(main())
    print(f"Flag is: {flag}")

    if flag:
        try:
            commit_msg = f"Database updated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'add', '.'])
            subprocess.run(['git', 'commit', '-m', commit_msg])
            subprocess.run(['git', 'push', '-u', 'origin', 'main'])

        except Exception as e:
            print(f"Error while git push: {e}")
