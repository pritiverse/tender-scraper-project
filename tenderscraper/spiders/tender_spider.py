import scrapy
from tenderscraper.items import TenderItem
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

class CPPPTenderSpider(scrapy.Spider):
    name = "cppp"
    start_urls = [
        "https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata"
    ]

    def __init__(self):
        self.items_scraped = 0
        self.limit = 30  # Number of records to scrape

    def parse(self, response):
        rows = response.xpath('//table[contains(@class, "table")]/tbody/tr')
        for row in rows:
            if self.items_scraped >= self.limit:
                return

            item = TenderItem()
            item['tenderId'] = row.xpath('.//td[5]/text()').get(default='').strip()
            item['sourceUrl'] = response.url
            item['scrapedTimestamp'] = datetime.utcnow().isoformat() + "Z"
            item['country'] = "IN"
            item['state'] = ""
            item['region'] = ""
            item['referenceNumber'] = item['tenderId']

            title = row.xpath('.//td[5]/a/text()').get() or row.xpath('.//td[1]/text()').get(default='').strip()
            item['title'] = title.strip() if title else ''
            item['issuingAuthority'] = row.xpath('.//td[6]/text()').get(default='').strip()
            item['procurementSummary'] = item['title']
            item['category'] = []
            item['tenderValue'] = None
            item['currency'] = "INR"
            item['publishedDate'] = self.parse_date(row.xpath('.//td[4]/text()').get())
            item['clarificationEndDate'] = None
            item['closingDate'] = self.parse_date(row.xpath('.//td[7]/text()').get())
            item['openingDate'] = self.parse_date(row.xpath('.//td[7]/text()').get())

            item['eligibilityRequirements'] = []
            item['proposalFormat'] = []
            item['unstructuredData'] = {}
            item['vectorEmbedding'] = None

            self.items_scraped += 1
            yield item

        # Handle pagination by incrementing page number via URL param
        if self.items_scraped < self.limit:
            current_url = response.url
            parsed = urlparse(current_url)
            query_params = parse_qs(parsed.query)
            current_page = int(query_params.get('page', ['1'])[0])
            next_page_num = current_page + 1
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            next_page_url = f"{base_url}?page={next_page_num}"

            # Request next page URL
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_date(self, date_str):
        if not date_str or date_str.strip() in ['', '--']:
            return None
        try:
            dt = datetime.strptime(date_str.strip(), "%d-%b-%Y %I:%M %p")
            return dt.isoformat()
        except Exception:
            return None
