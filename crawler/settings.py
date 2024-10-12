import os
import sys
from pathlib import Path

import django
from django.conf import settings
from scrapy.utils.reactor import install_reactor

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(os.path.join(BASE_DIR, "config"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
django.setup()

BOT_NAME = "crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = False

# HTTPCACHE_ENABLED = False
# REDIRECT_ENABLED = True
# COOKIES_ENABLED = False
DOWNLOAD_DELAY = 0

CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 10

# LOGSTATS_INTERVAL = 10
CONCURRENT_REQUESTS_PER_IP = 10

SPIDER_MIDDLEWARES = {
    "crawler.middlewares.default.CrawlerSpiderMiddleware": 543,
}

DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.retry.TooManyRequestsRetryMiddleware": 541,
    "crawler.middlewares.default.CrawlerDownloaderMiddleware": 543,
}

ITEM_PIPELINES = {
    "crawler.pipelines.images.CrawlerImagesPipeline": 100,
    "crawler.pipelines.time.CrawlerTimePipeline": 200,
    "crawler.pipelines.db.CrawlerDbPipeline": 300,
    # "crawler.pipelines.redis.red.CrawlerRedisPipeline": 400,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
REQUEST_FINGERPRINTER_CLASS = "crawler.utils.RequestFingerprinter"
# REQUEST_FINGERPRINTER_CLASS = "scrapy.utils.request.fingerprint()"
TWISTED_REACTOR = install_reactor(
    "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
)
FEED_EXPORT_ENCODING = "utf-8"

RETRY_TIMES = 3
RETRY_ENABLED = True
RETRY_HTTP_CODES = [i for i in range(300, 601)]

IMAGES_STORE = settings.MEDIA_ROOT

MEDIA_ALLOW_REDIRECTS = True
REACTOR_THREADPOOL_MAXSIZE = 32
# DNS_TIMEOUT = 180
DOWNLOAD_FAIL_ON_DATALOSS = True
LOG_LEVEL = "WARNING"
# LOG_LEVEL = "INFO"
# LOG_LEVEL = "DEBUG"
LOG_FORMATTER = "crawler.utils.PoliteLogFormatter"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = False
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
# REDIS_URL = settings.CELERY_BROKER_URL
# SCHEDULER_FLUSH_ON_START = True
ADDONS = {
    "crawler.addon.MyAddon": 1,
}
EXTENSIONS = {"crawler.extensions.SpiderOpenCloseLogging": 500}

# FEEDS = {
#     "comics.json": {
#         "format": "json",
#         "encoding": "utf8",
#         "store_empty": False,
#         "item_classes": ["crawler.items.ComicItem"],
#         "fields": None,
#         "indent": 4,
#     },
#     "chapters.json": {
#         "format": "json",
#         "encoding": "utf8",
#         "store_empty": False,
#         "item_classes": ["crawler.items.ChapterItem"],
#         "fields": None,
#         "indent": 4,
#     },
# }
IMAGES_EXPIRES = 730
HTTPERROR_ALLOW_ALL = True
