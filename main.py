from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from schema import *
from agent import LLMagent as agent
from Prompt import ExtractTaskLlm
from Googletask import createTask

def scrape_linkedin_posts(query):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./linkedin_session", headless=False
        )
        page = browser.new_page()

        url = f"https://www.linkedin.com/search/results/content/?keywords={query.replace(' ', '%20')}"
        # url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
        page.goto(url)

        page.wait_for_selector("div.occludable-update", timeout=20000)
        for i in range(6):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        for post in soup.find_all("div", class_="feed-shared-update-v2"):
            # Extract data-urn
            data_urn = post.get("data-urn")
            post_url = f"https://www.linkedin.com/feed/update/{data_urn}" if data_urn else "URL not found"

            # Extract text
            text_div = post.find("div", class_="update-components-text")
            text = text_div.get_text(separator="\n", strip=True) if text_div else "No text found"

            # Extract author
            author_tag = post.find("span", class_="update-components-actor__title")
            author_name = author_tag.get_text(strip=True) if author_tag else "Author not found"
            agentFeedback = agent(ExtractTaskLlm(url=post_url, text=text))
            createTask({
                "title" : f"LinkedIn Application -> {agentFeedback["job_title"]}",
                "notes" : f"{agentFeedback["hiring_task"]} - {agentFeedback["post_url"]}"   

            })
        input("Press Enter to close the browser...")
        browser.close()
# def scrape_linkedin_people(query):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./linkedin_session",
            headless=False

        )
        page = browser.new_page()

        url = f"https://www.linkedin.com/search/results/people/?keywords={query.replace(' ', '%20')}"
        page.goto(url)

        # Wait for ANY person card
        page.wait_for_selector('a[href*="/in/"]', timeout=20000)

        # Scroll to load more
        for _ in range(6):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        soup = BeautifulSoup(page.content(), "html.parser")

        # Find all person cards
        # cards = soup.select('a[href*="/in/"]')
        cards = [
            c for c in soup.select('a[href*="/in/"]')
            if c.select_one('a[data-view-name="search-result-lockup-title"]')
        ]


        for card in cards:
            profile_url = card.get("href")

            # Name (first title link)
            name_tag = card.select_one('a[data-view-name="search-result-lockup-title"]')
            name = name_tag.get_text(strip=True) if name_tag else "No name"

            # Headline (first p.bcbad6fa.b47b8486...)
            headline_tag = card.select_one("p.bcbad6fa.b47b8486")
            headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

            # Location (second occurrence)
            location_tag = card.select("p.bcbad6fa.b47b8486")
            location = location_tag[1].get_text(strip=True) if len(location_tag) > 1 else "No location"

            # Image
            img_tag = card.select_one("img[alt]")
            img = img_tag.get("src") if img_tag else "No image"

            print("\n----- PERSON -----")
            print("Name:", name)
            print("Headline:", headline)
            print("Location:", location)
            print("Profile URL:", profile_url)
            print("Image URL:", img)


        input("Press Enter to close...")
        browser.close()
scrape_linkedin_posts('''"freelance project" OR "looking for freelancer" OR "need a freelancer" OR "hiring freelancer" OR "freelance work"''')
# scrape_linkedin_people('''"flutter developer" OR "react native"''')