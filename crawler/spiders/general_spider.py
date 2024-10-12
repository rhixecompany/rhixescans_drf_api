import logging

from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

from crawler.items import ChapterItem, ComicItem

logger = logging.getLogger(__name__)


class GeneralSpider(Spider):
    name = "general"
    start_urls = ["https://asuracomic.net/series"]

    def parse(self, response):
        # urls = [f"https://asuracomic.net/series?page={i}" for i in range(2, 17)]
        urls = [f"https://asuracomic.net/series?page={i}" for i in range(2, 3)]

        links = response.xpath(
            "//div[@class='grid grid-cols-2 sm:grid-cols-2 md:grid-cols-5 gap-3 p-4']/a/@href",
        ).getall()
        if links:
            yield from response.follow_all(links, callback=self.parse_item)

        if urls:
            yield from response.follow_all(urls, callback=self.parse)
        logger.info("Current Page: %s", response.url)

    def parse_item(self, response):
        loader = ItemLoader(item=ComicItem(), selector=response)
        image = response.urljoin(
            response.xpath("//img[@class='rounded mx-auto md:mx-0 ']/@src").get(),
        )
        loader.add_value("url", response.url)

        loader.add_value("image_urls", image)

        loader.add_value(
            "numChapters",
            len(
                response.xpath(
                    "//div[@class='pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20']/h3/a/@href",
                ).getall(),
            ),
        )

        genres = response.xpath(
            "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
        ).getall()
        if genres:
            loader.add_xpath(
                "genres",
                "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
            )
        elif not genres:
            loader.add_value(
                "genres",
                "-",
            )
        des = response.xpath(
            "//div[@class='col-span-12 sm:col-span-9 ']/span/text()",
        ).getall()
        ddes = response.xpath(
            "//div[@class='col-span-12 sm:col-span-9 ']/span/p/text()",
        ).getall()
        dddes = response.xpath(
            "//span[@class='font-medium text-sm text-[#A2A2A2]']/text()",
        ).getall()
        ddddes = response.xpath(
            "//span[@class='font-medium text-sm text-[#A2A2A2]']/p/text()",
        ).getall()
        if des:
            loader.add_xpath(
                "description",
                "//div[@class='col-span-12 sm:col-span-9 ']/span/text()",
            )

        elif ddes and not des:
            loader.add_xpath(
                "description",
                "//div[@class='col-span-12 sm:col-span-9 ']/span/p/text()",
            )
        elif dddes and not ddes:
            loader.add_xpath(
                "description",
                "//span[@class='font-medium text-sm text-[#A2A2A2]']/text()",
            )
        elif ddddes and not ddes and not dddes:
            loader.add_xpath(
                "description",
                "//span[@class='font-medium text-sm text-[#A2A2A2]']/p/text()",
            )
        elif not des and not ddddes and not ddes and not dddes:
            loader.add_value("description", "-")

        loader.add_xpath(
            "title",
            "//div[@class='text-center sm:text-left']/span/text()",
        )
        loader.add_xpath(
            "slug",
            "//div[@class='text-center sm:text-left']/span/text()",
        )

        loader.add_xpath(
            "serialization",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[1]/h3[2]/text()",
        )
        loader.add_xpath(
            "author",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[2]/h3[2]/text()",
        )
        loader.add_xpath(
            "artist",
            "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[3]/h3[2]/text()",
        )
        # loader.add_xpath(
        #     "updated_at",
        #     "//div[@class='grid grid-cols-1 md:grid-cols-2 gap-5 mt-8']/div[5]/h3[2]/text()",
        # )
        loader.add_xpath(
            "rating",
            "//div[@class='bg-[#343434] px-2 py-1 flex items-center justify-between rounded-[3px]']/p/text()",
        )
        loader.add_xpath(
            "status",
            "//div[@class='bg-[#343434] px-2 py-2 flex items-center justify-between rounded-[3px] w-full']/h3[2]/text()",
        )
        loader.add_xpath(
            "type",
            "//div[@class='bg-[#343434] px-2 py-2 flex items-center justify-between rounded-[3px] w-full'][2]/h3[2]/text()",
        )
        item = loader.load_item()
        yield item

        chapters = response.xpath(
            "//div[@class='pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20']/h3/a/@href",
        ).getall()[0:1]
        if chapters:
            yield from response.follow_all(chapters, callback=self.parsechapter)

        logger.info("A New Comic was found at %s", response.url)

    def parsechapter(self, response):
        loader = ItemLoader(item=ChapterItem(), selector=response)
        images = []
        image_urls = response.xpath(
            "//div[@class='w-full mx-auto center']/img[@class='object-cover mx-auto']/@src",
        ).getall()
        for image in image_urls:
            images.append(response.urljoin(image))
        title = response.xpath(
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        ).get()
        name = response.xpath(
            "//div[@class='dropdown md:w-[13em]']/button/h2/text()",
        ).get()
        slug = f"{title} {name}"
        loader.add_value("url", response.url)
        loader.add_value("chapterslug", slug)
        loader.add_value("image_urls", images)
        loader.add_value("numPages", len(image_urls))
        loader.add_xpath(
            "chaptername",
            "//div[@class='dropdown md:w-[13em]']/button/h2/text()",
        )
        loader.add_xpath(
            "comictitle",
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        )
        loader.add_xpath(
            "comicslug",
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        )
        # loader.add_xpath(
        #     "comicslug",
        #     "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/@href",
        # )
        item = loader.load_item()
        yield item

        logger.info("A New Chapter was found at %s", response.url)
