from django.core.management.base import BaseCommand

from redis import from_url
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer
from twisted.internet import reactor
from django.conf import settings as set
from crawler.spiders.asuracomic import AsuracomicSpider


class Command(BaseCommand):
    help = "A  Custom command to  run my spiders"

    def handle(self, *args, **options):
        # redisClient = from_url(set.CELERY_BROKER_URL)

        # redisClient.rpush(
        #     "asuracomic_queue:start_urls",
        #     "https://asuracomic.net/series",
        # )

        settings = get_project_settings()
        configure_logging(settings)
        runner = CrawlerRunner(settings=settings)

        @defer.inlineCallbacks
        def run():
            yield runner.crawl(AsuracomicSpider)
            reactor.stop()

        run()
        results = reactor.run()
        return results
