# from django.utils import timezone
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CrawlerTimePipeline:

    # def __init__(self):
    #     self.slug_seen = set()
    #     self.chapterslug_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("images"):
            if adapter.get("images") and adapter.get("title"):
                # if adapter["slug"] in self.slug_seen:
                #     raise DropItem(f"ComicItem Already Exists In The Database:{item!r}")
                # self.slug_seen.add(adapter["slug"])
                # item["downloaded_at"] = timezone.now()
                item["spider"] = spider.name
                return item
            if (
                adapter.get("images")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                # if adapter["chapterslug"] in self.chapterslug_seen:
                #     raise DropItem(
                #         f"ChapterItem Already Exists In The Database:{item!r}"
                #     )

                # self.chapterslug_seen.add(adapter["chapterslug"])
                # item["downloaded_at"] = timezone.now()
                item["spider"] = spider.name
                return item
        else:
            raise DropItem(
                f"CrawlerTimePipeline Item has a Missing field:{item!r}",
            )
