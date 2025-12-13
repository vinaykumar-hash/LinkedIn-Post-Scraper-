# LinkedIn Scraper

Automatically scrape freelancing and job opportunity posts from LinkedIn and add them to Google Tasks using Google Gemini AI.

Additionally, this project supports scraping LinkedIn profiles based on a specific headline or skill and exporting the results to a CSV file.

==================================================

FEATURES

- Scrapes freelancing / hiring posts from LinkedIn
- Uses Gemini AI to summarize and extract key details
- Automatically creates Google Tasks with apply instructions
- Runs in Chromium via Playwright
- Secure authentication using OAuth tokens

NEW FEATURE
- Scrape LinkedIn profiles by headline / skill
- Export profile data to CSV using accounts.py

==================================================

PROFILE HEADLINE SCRAPER (accounts.py)

The accounts.py script allows you to extract LinkedIn profiles based on a specific headline or skill.

Examples:
- React Developer
- UI/UX Designer
- Machine Learning Engineer
- Python | Django | AWS

What it extracts:
- Name
- Headline
- Profile URL

The data is saved into a CSV file for easy filtering and outreach.

Run the script:
python accounts.py

Modify the search query inside accounts.py:
query = "React Native Developer"

Output file:
linkedin_profiles.csv

CSV Example:
Name,Headline,Profile URL
John Doe,React Native Developer | Expo | Firebase,https://linkedin.com/in/johndoe

==================================================

SETUP

1. Clone the repository
```
git clone https://github.com/vinaykumar-hash/LinkedIn-Post-Scraper-.git
cd LinkedIn_Posttool
```
2. Install dependencies using uv
```
uv sync
uv add google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
3. Set up Google credentials
- Create a Google Cloud project
- Enable Google Tasks API
- Create OAuth 2.0 credentials
- Place credentials.json in the project root

4. Authenticate with Google Cloud
```
gcloud auth application-default login
```
5. Environment variables (.env)
```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```
6. Run the program
```
python main.py
```
==================================================
```
FOLDER STRUCTURE

LinkedIn_Posttool/
│
├── main.py
├── accounts.py
├── agent.py
├── schema.py
├── Prompt.py
├── Googletask.py
├── credentials.json
├── token.json
├── .env
└── .gitignore
```
==================================================

NOTES

- Do not commit credentials.json or token.json
- Use LinkedIn scraping responsibly
- CSV output is suitable for recruiters, sourcing, and lead generation

==================================================

Made with ❤️ by Vinay Kumar
Powered by Gemini AI, Playwright, and Google Tasks API
