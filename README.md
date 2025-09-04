Tender Scraper Project
📌 Overview

This project is a Scrapy-based web scraper designed to extract tender data from the Indian Central Public Procurement Portal
.

It collects:

Tender IDs

Titles

Issuing authorities

Dates

Other metadata

The scraped data is stored in a MongoDB database, making it ready for further analysis or API consumption.

✨ Features

Scrapes tenders with structured data fields.

Supports pagination to capture multiple pages.

Converts dates to ISO 8601 format.

Stores data cleanly in MongoDB.

Easily extensible for other portals or extra tender details.

⚙️ Installation
Prerequisites

Python 3.9+

MongoDB (local or remote)

Git (optional, for cloning the repo)

Setup Steps

Clone the repository:

git clone <repository_url>
cd tender-scraper-project


Create and activate a virtual environment:

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

📂 Project Structure
tender-scraper-project/
├── scrapy.cfg
├── requirements.txt
├── tenderscraper/              # Scrapy project folder
│   ├── __init__.py
│   ├── items.py                 # Data model
│   ├── pipelines.py             # MongoDB pipeline
│   ├── settings.py              # Scrapy & MongoDB config
│   └── spiders/
│       ├── __init__.py
│       └── cppp_spider.py       # Main spider (scraping + pagination)
├── api/                         # (Optional) API backend
│   ├── __init__.py
│   ├── main.py
│   └── models.py
└── run_api.py                   # API launch script

▶️ Usage

From the project root (scrapy.cfg location), run:

scrapy crawl cppp


This will:

Start scraping from the first page.

Follow pagination links.

Stop after scraping 30 tenders (configurable).

Insert data into MongoDB → tenderdb database → tenders collection.

🧩 Code Highlights

cppp_spider.py → Spider with XPath extraction, pagination, and ISO date parsing.

pipelines.py → Handles MongoDB storage.

settings.py → MongoDB config + scraping parameters.

Pagination logic → Automatically increments page queries.

Error handling → Manages missing fields & date parsing issues.

🚀 Improvements & Next Steps

Enhance XPath selectors to capture richer details (eligibility, value, category).

Follow tender detail pages for documents & in-depth info.

Normalize/validate all date & numerical fields.

Implement incremental scraping to avoid duplicates.

Add anti-blocking techniques (user-agent rotation, proxies).

Build a REST API for frontend consumption.

Automate runs via cron jobs / CI pipelines.

Extend to multi-country portals with configurable spiders.
