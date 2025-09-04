BOT_NAME = 'tenderscraper'

SPIDER_MODULES = ['tenderscraper.spiders']
NEWSPIDER_MODULE = 'tenderscraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'tenderscraper.pipelines.MongoPipeline': 300,
}

# MongoDB connection URI and DB name
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'tenderdb'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

LOG_LEVEL = 'INFO'
