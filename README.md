
# Tender Scraper Project
This project is a web scraper built using **Scrapy** to extract tender information from t
---
## Features
- Scrapes tender ID, title, issuing authority, dates, and other metadata.
- Supports pagination to scrape multiple tender pages (e.g., 30 tenders).
- Stores results in a MongoDB collection (`tenders`).
- Easily extensible to scrape additional tender portals.
---
## Tech Stack
- **Python 3.11+**
- **Scrapy 2.13.3** (web scraping framework)
- **MongoDB** (NoSQL database for storing scraped tenders)
- Other libraries: `pymongo` for MongoDB integration
---
## Installation & Setup
1. **Clone the repository:**
git clone <repo-url>
cd tender-scraper-project
2. **Create and activate Python virtual environment:**
write report oh what ton install, code ,file
structure, etc from coder pov- for git hub readme
python -m venv venv
source venv/bin/activate # On Linux/macOS
venv\Scripts\activate # On Windows
3. **Install required Python packages:**
pip install -r requirements.txt
4. **Install and start MongoDB server:**
- [Download MongoDB Community Edition](https://www.mongodb.com/try/download/community) an
- Start MongoDB service or run from terminal:
```
mongod
```
---
## Project Structure
tender-scraper-project/
├── scrapy.cfg # Scrapy project config file
├── requirements.txt # Python dependencies
├── tenderscraper/ # Scrapy project folder
│ ├── init.py
│ ├── items.py # Scrapy item definitions
│ ├── pipelines.py # MongoDB pipeline
│ ├── settings.py # Project settings
│ └── spiders/
│ ├── init.py
│ └── cppp_spider.py # Tender spider with pagination support
├── api/ # (Optional) API backend folder
│ ├── init.py
│ ├── main.py
│ └── models.py
└── run_api.py # (Optional) API run script
---
## Running the Spider
Run the scraper from the project root (where `scrapy.cfg` is located):
scrapy crawl cppp
This will scrape up to 30 tender records across multiple pages and save them into the Mon
---
## Sample Output
Scraped data sample (stored in MongoDB as JSON):
{
"tenderId": "/04/TZCD/2025-26/Tezpur/125823",
"title": "Road Construction Works at Tezpur",
"issuingAuthority": "Central Public Works Department (CPWD)",
"publishedDate": "2025-09-12T15:30:00Z",
"closingDate": "2025-09-15T17:00:00Z",
"currency": "INR",
"sourceUrl": "https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata?page=1",
"scrapedTimestamp": "2025-09-04T16:59:39Z"
}
---
