```markdown
# Tender Scraper Project

📌 **Overview**  
This project is a Scrapy-based web scraper designed to extract tender data from the [Indian Central Public Procurement Portal](https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata?utm_source=chatgpt.com).  
It collects:  
- Tender IDs  
- Titles  
- Issuing authorities  
- Dates  
- Other metadata  

The scraped data is stored in a MongoDB database, making it ready for further analysis or API consumption.

---

✨ **Features**  
- Scrapes tenders with structured data fields.  
- Supports pagination to capture multiple pages.  
- Converts dates to ISO 8601 format.  
- Stores data cleanly in MongoDB.  
- Easily extensible for other portals or extra tender details.

---

⚙️ **Installation**

**Prerequisites:**  
- Python 3.9+  
- MongoDB (local or remote)  
- Git (optional, for cloning the repo)

**Setup Steps:**  
```
git clone <repository_url>
cd tender-scraper-project

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

📂 **Project Structure**

```
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
```

---

▶️ **Usage**

From the project root (where `scrapy.cfg` is), run:  
```
scrapy crawl cppp
```

This will:  
- Start scraping from the first page.  
- Follow pagination links automatically.  
- Stop after scraping 30 tenders (configurable in spider).  
- Insert data into MongoDB → `tenderdb` database → `tenders` collection.

---

🧩 **Code Highlights**

- `cppp_spider.py` → Spider with XPath extraction, pagination, and ISO date parsing.  
- `pipelines.py` → Handles MongoDB storage and upserts to avoid duplicates.  
- `settings.py` → MongoDB connection config and Scrapy parameters.  
- Pagination logic → Automatically increments page query parameters on portal.  
- Error handling → Manages missing fields & date parsing issues gracefully.

---

🚀 **Improvements & Next Steps**

🔹 **Technology Stack & Anti-Scraping Mitigation**  
- Python (Scrapy) for scraping orchestration; fallback to Selenium/Playwright for dynamic content.  
- BeautifulSoup/lxml for advanced parsing as needed.  
- Proxy rotation and user-agent spoofing for stealth and robustness.  
- CAPTCHA solving if required for protected portals.

🔹 **Vector Embedding Pipeline**  
- Scrape & Store → Insert MongoDB document, `vectorEmbedding = null`.  
- Event Trigger → Use RabbitMQ / Kafka or MongoDB Change Streams.  
- Embedding Worker → Generate semantic text embeddings (Sentence-BERT / OpenAI API).  
- Update Record → Patch `vectorEmbedding` field with float vector array.

🔹 **Output Formatting & Consistency**  
- Maintain API and database document compatibility with shared specs.  
- Map unstructured data sections as raw text or HTML for full fidelity.  
- Test with synthetic data aligned with output schema.

---
