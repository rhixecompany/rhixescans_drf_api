import logging

from scrapy import Spider
from scrapy.loader import ItemLoader

from crawler.items import ChapterItem, ComicItem

logger = logging.getLogger(__name__)


class AsuraSpider(Spider):
    name = "asura"
    allowed_domains = ["asuracomic.net"]
    start_urls = [
        "https://asuracomic.net/series/maxed-out-leveling-057f45c9",
    ]
    # redis_key = "asuracomic_queue:start_urls"

    # redis_batch_size = 1

    # max_idle_time = 7

    custom_feed = {}

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.setdefault("FEEDS", {}).update(cls.custom_feed)

    def parse(self, response):
        logger.warning("A New Comic was found at %s", response.url)
        loader = ItemLoader(item=ComicItem(), selector=response)
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
        loader.add_xpath(
            "updated_at",
            '//div[contains(@class, "grid grid-cols-1 md:grid-cols-2 gap-5 mt-8")]/div[5]/h3[2]/text()',
        )

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
        image = response.xpath("//img[@class='rounded mx-auto md:mx-0 ']/@src").get()
        image2 = response.xpath(
            '//div[contains(@class, "bigcover")]/img[contains(@data-nimg, "1")]/@src'
        ).get()
        chapters = response.xpath(
            '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3/a/@href'
        ).getall()[0:2]
        chapters_time = response.xpath(
            '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3[2]/text()'
        ).getall()[0:2]
        loader.add_value("url", response.url)
        cimages = []
        cimages.append(response.urljoin(image))
        if image2:
            cimages.append(response.urljoin(image2))
        loader.add_value("image_urls", cimages)
        loader.add_value(
            "numChapters",
            len(chapters),
        )
        genres = response.xpath(
            "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
        ).getall()
        if not genres:
            loader.add_value(
                "genres",
                "-",
            )
        else:
            loader.add_xpath(
                "genres",
                "//div[@class='flex flex-row flex-wrap gap-3']/button/text()",
            )
        des = response.xpath(
            '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/text()',
        ).getall()
        desem = response.xpath(
            '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong/em/text()',
        ).getall()
        if not des:
            newdes = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/text()',
            ).getall()

            newdesem = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/strong/em/text()',
            ).getall()
            newdesem1 = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[1]/text()',
            ).getall()
            newdesem2 = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[2]/em/text()',
            ).getall()
            newdesem3 = response.xpath(
                '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/p/strong[2]/em/text()',
            ).getall()
            newdesemdiv = f"{newdesem}{newdesem1}{newdesem2}{newdesem3}"
            if not newdes:
                olddes = response.xpath(
                    '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/div/div/div[1]/text()',
                ).getall()
                oldesem = response.xpath(
                    '//div[contains(@class, "col-span-12 sm:col-span-9")]/span/div/div/div[1]/strong/em/text()',
                ).getall()
                if not olddes:
                    pass
                if not oldesem:
                    myolddes = f"{olddes}"
                    loader.add_value("description", myolddes)
                oldmydesem = f"{oldesem}{olddes}"
                loader.add_value("description", oldmydesem)
            if not newdesem:
                mynewdes = f"{newdes}"
                loader.add_value("description", mynewdes)
            newmydesem = f"{newdesem}{newdes}"
            loader.add_value("description", newmydesem)

        if not desem:
            mydes = f"{des}"
            loader.add_value("description", mydes)
        mydesem = f"{desem} {des}"
        loader.add_value("description", mydesem)

        item = loader.load_item()
        yield item

        if chapters:
            yield from response.follow_all(
                chapters,
                callback=self.parsechapter,
                cb_kwargs=dict(chapters_time=chapters_time),
            )
        # chapters = response.xpath(
        #     '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3/a/@href',
        # ).getall()[:1]
        # chapters_time = response.xpath(
        #     '//div[contains(@class, "pl-4 py-2 border rounded-md group w-full hover:bg-[#343434] cursor-pointer border-[#A2A2A2]/20 relative")]/h3[2]/text()'
        # ).getall()[:1]
        # if chapters:
        #     yield from response.follow_all(
        #         chapters,
        #         callback=self.parsechapter,
        #         cb_kwargs=dict(chapters_time=chapters_time),
        #     )

    def parsechapter(self, response, chapters_time):
        logger.warning("A New Chapter was found at %s", response.url)
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

        chaptername = response.xpath(
            '//div[contains(@class, "dropdown md:w-[13em] max-[350px]:w-[10rem] ")]/button[contains(@class, "px-3 py-2 dropdown-btn")]/h2[contains(@class, "text-[#9B9B9B] text-[13px] whitespace-nowrap max-[350px]:truncate")]/text()',
        ).get()

        slug = f"{title} {chaptername}"

        loader.add_value("url", response.url)
        loader.add_value("chapterslug", slug)
        loader.add_value("chaptername", chaptername)
        loader.add_value("image_urls", images)
        # loader.add_value("numPages", len(image_urls))
        loader.add_value("updated_at", chapters_time)

        loader.add_value("comictitle", title)
        loader.add_xpath(
            "comicslug",
            "//div[@class='flex flex-col items-center space-y-2 pt-6 px-5 text-center']/p/a/span/text()",
        )
        item = loader.load_item()
        yield item
