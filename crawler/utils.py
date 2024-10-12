import logging
import os
from hashlib import sha1
from weakref import WeakKeyDictionary

from scrapy.logformatter import LogFormatter
from scrapy.utils.python import to_bytes


class RequestFingerprinter:
    cache = WeakKeyDictionary()

    def fingerprint(self, request):
        if request not in self.cache:
            fp = sha1()
            fp.update(to_bytes(request.url))
            self.cache[request] = fp.digest()
        return self.cache[request]


class PoliteLogFormatter(LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            "level": logging.WARNING,  # lowering the level from logging.WARNING
            "msg": "Dropped: %(exception)s" + os.linesep + "%(item)s",
            "args": {
                "exception": exception,
                "item": item,
            },
        }
