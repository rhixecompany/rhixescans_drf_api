# import hashlib

from contextlib import suppress

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.images import ImagesPipeline


class CrawlerImagesPipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        # s3store = cls.STORE_SCHEMES["s3"]
        # s3store.AWS_ACCESS_KEY_ID = settings["AWS_ACCESS_KEY_ID"]
        # s3store.AWS_SECRET_ACCESS_KEY = settings["AWS_SECRET_ACCESS_KEY"]
        # s3store.AWS_SESSION_TOKEN = settings["AWS_SESSION_TOKEN"]
        # s3store.AWS_ENDPOINT_URL = settings["AWS_ENDPOINT_URL"]
        # s3store.AWS_REGION_NAME = settings["AWS_REGION_NAME"]
        # s3store.AWS_USE_SSL = settings["AWS_USE_SSL"]
        # s3store.AWS_VERIFY = settings["AWS_VERIFY"]
        # s3store.POLICY = settings["IMAGES_STORE_S3_ACL"]
        store_uri = settings["IMAGES_STORE"]
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)

        if adapter.get("image_urls"):
            if adapter.get("image_urls") and adapter.get("title"):
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [
                    Request(
                        u,
                        meta={"comicfoldertitle": item.get("slug")},
                        callback=NO_CALLBACK,
                    )
                    for u in urls
                ]
            if (
                adapter.get("image_urls")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [
                    Request(
                        u,
                        meta={
                            "comicfoldertitle": item.get("comicslug"),
                            "chapterfoldername": item.get("chapterslug"),
                        },
                        callback=NO_CALLBACK,
                    )
                    for u in urls
                ]
        else:
            raise DropItem(f"Missing field in get_media_requests: {item!r}")

    def item_completed(self, results, item, info):
        with suppress(KeyError):
            item["images"] = ItemAdapter(item)[self.images_result_field] = [
                x for ok, x in results if ok
            ]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        if adapter.get("image_urls"):
            if adapter.get("image_urls") and adapter.get("title"):
                file = "{}/{}".format(
                    request.meta["comicfoldertitle"], request.url.split("/")[-1]
                )
                return file
            if (
                adapter.get("image_urls")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                file = "{}/{}/{}".format(
                    request.meta["comicfoldertitle"],
                    request.meta["chapterfoldername"],
                    request.url.split("/")[-1],
                )
                return file
        else:
            raise DropItem(f"Missing field in file_path: {item!r}")
