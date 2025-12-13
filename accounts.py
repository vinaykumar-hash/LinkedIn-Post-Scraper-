import csv
from playwright.sync_api import sync_playwright
import time
import os


def scrape_linkedin_people(query):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./linkedin_session",
            headless=False
        )
        page = browser.new_page()

        base_url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
        page.goto(base_url)

        all_rows = []
        page_number = 1

        while page_number<2:

            print(f"\n============================")
            print(f" SCRAPING PAGE {page_number}")
            print(f"============================")

            for _ in range(6):
                page.mouse.wheel(0, 4000)
                time.sleep(1.2)

            cards = page.query_selector_all('a[href*="/in/"]')

            rows = extract_people_from_cards(cards)
            all_rows.extend(rows)

            print(f"Extracted {len(rows)} profiles on page {page_number}")

            next_btn = page.query_selector(
                'button[data-testid="pagination-controls-next-button-visible"]'
            )

            if not next_btn:
                print("\nNo NEXT button found — scraping complete.")
                break

            disabled = next_btn.get_attribute("disabled")
            if disabled is not None:
                print("\nNext button disabled — end reached.")
                break

            print("\nClicking NEXT page...")
            next_btn.click()
            time.sleep(2.5)

            page_number += 1

        save_to_csv(all_rows)
        print("\nCSV saved as linkedin_people.csv")

        input("\nPress Enter to close...")
        browser.close()


def extract_people_from_cards(cards):
    rows = []
    seen = set()

    for card in cards:

        name_el = card.query_selector('a[data-view-name="search-result-lockup-title"]')
        if not name_el:
            continue

        name = name_el.inner_text().strip()

        p_tags = card.query_selector_all("p")

        headline = p_tags[1].inner_text().strip() if len(p_tags) > 1 else "No headline"
        location = p_tags[2].inner_text().strip() if len(p_tags) > 2 else "No location"

        profile_url = card.get_attribute("href")

        if profile_url in seen:
            continue
        seen.add(profile_url)

        img_el = card.query_selector("img[alt]")
        image_url = img_el.get_attribute("src") if img_el else "No image"

        rows.append([name, headline, location, profile_url, image_url])

    return rows


def save_to_csv(rows, filename="linkedin_people.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name", "Headline", "Location", "Profile URL", "Image URL"])

        writer.writerows(rows)


scrape_linkedin_people('''"react native developer" OR "SEO Specialist"''')
