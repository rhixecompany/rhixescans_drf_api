from django.contrib.auth import get_user_model
from django.db.models import Q
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from api.apps.models import Artist
from api.apps.models import Author
from api.apps.models import Chapter
from api.apps.models import ChapterImage
from api.apps.models import ChapterImagesItem
from api.apps.models import Comic
from api.apps.models import ComicImage
from api.apps.models import ComicImagesItem
from api.apps.models import Genre
from api.apps.models import Type


class CrawlerDbPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("images"):
            if adapter.get("images") and adapter.get("title"):
                title = item["title"]
                slug = item["slug"]
                description = item["description"]
                rating = item["rating"]
                status = item["status"]
                url = item["url"]
                spider = item["spider"]
                # downloaded_at = item["downloaded_at"]
                updated_at = item["updated_at"]
                numChapters = item["numChapters"]
                serialization = item["serialization"]
                type = item["type"]
                author = item["author"]
                artist = item["artist"]
                images = item["images"]
                genres = item.get("genres")
                User = get_user_model()
                user = User.objects.filter(
                    Q(email__iexact="admin@rhixe.company")
                    | Q(username__iexact="adminbot")
                ).first()
                if not user:
                    user = User.objects.create_superuser(
                        email="admin@rhixe.company",
                        username="adminbot",
                        password="R4I7gcJHX",
                    )
                ty = Type.objects.filter(Q(name__iexact=type)).get_or_create(name=type)[
                    0
                ]
                au = Author.objects.filter(Q(name__iexact=author)).get_or_create(
                    name=author
                )[0]
                ar = Artist.objects.filter(Q(name__iexact=artist)).get_or_create(
                    name=artist
                )[0]
                comquery = Q(slug__iexact=slug)
                comic = Comic.objects.filter(comquery).first()
                if not comic:
                    co = Comic.objects.filter(comquery).get_or_create(
                        user=user,
                        type=ty,
                        artist=ar,
                        author=au,
                        title=title,
                        slug=slug,
                        description=description,
                        rating=rating,
                        status=status,
                        url=url,
                        spider=spider,
                        # downloaded_at=downloaded_at,
                        updated_at=updated_at,
                        numChapters=numChapters,
                        serialization=serialization,
                    )[0]
                    for genre in genres:
                        ge = Genre.objects.filter(Q(name__iexact=genre)).get_or_create(
                            name=genre,
                        )[0]
                        co.genres.add(ge)
                        co.save()
                    if images:
                        for image in images:
                            img_file = image["path"]
                            img_url = image["url"]
                            panquery = Q(url__iexact=img_url)
                            pannquery = Q(image__iexact=img_file)
                            imm = ComicImage.objects.filter(panquery).first()
                            if not imm:
                                lin = ComicImage.objects.filter(
                                    panquery
                                ).update_or_create(url=img_url)[0]
                                lmm = ComicImagesItem.objects.filter(pannquery).first()
                                if not lmm:
                                    im = ComicImagesItem.objects.filter(
                                        pannquery
                                    ).get_or_create(
                                        image=img_file,
                                        link=lin,
                                        comic=co,
                                    )[
                                        0
                                    ]
                            else:
                                raise DropItem(
                                    f"ComicImageItem Already Exists In The Database: {item!r}"
                                )
                    else:
                        raise DropItem(f"ComicImageItem has not images: {item!r}")
                    return item
                else:

                    raise DropItem(
                        f"ComicItem Already Exists In The Database: {item!r}"
                    )

            if (
                adapter.get("images")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                name = item["chaptername"]
                slug = item["chapterslug"]
                url = item["url"]
                spider = item["spider"]
                # downloaded_at = item["downloaded_at"]
                updated_at = item["updated_at"]

                chapterimages = item.get("images")
                numPages = len(chapterimages)
                comicslug = item["comicslug"]
                comictitle = item["comictitle"]
                comicquery = Q(slug__iexact=comicslug) | Q(title__iexact=comictitle)
                chapterquery = Q(slug__iexact=slug)
                comic = Comic.objects.filter(comicquery).first()
                if comic:

                    chapter = Chapter.objects.filter(chapterquery).first()
                    if not chapter:
                        c = Comic.objects.filter(comicquery).first()
                        ch = Chapter.objects.filter(chapterquery).get_or_create(
                            comic=c,
                            name=name,
                            # downloaded_at=downloaded_at,
                            updated_at=updated_at,
                            slug=slug,
                            url=url,
                            spider=spider,
                            numPages=numPages,
                        )[0]

                        if chapterimages:
                            for img in chapterimages:
                                cimg_file = img["path"]
                                cimg_url = img["url"]
                                panelquery = Q(url__iexact=cimg_url)
                                panellquery = Q(image__iexact=cimg_file)
                                panel = ChapterImage.objects.filter(panelquery).first()
                                if not panel:
                                    pa = ChapterImage.objects.filter(
                                        panelquery
                                    ).get_or_create(url=cimg_url,)[0]
                                    paas = ChapterImagesItem.objects.filter(
                                        panellquery
                                    ).first()
                                    if not paas:
                                        paa = ChapterImagesItem.objects.filter(
                                            panellquery
                                        ).get_or_create(
                                            link=pa,
                                            chapter=ch,
                                            comic=c,
                                            image=cimg_file,
                                        )[
                                            0
                                        ]
                                else:
                                    raise DropItem(
                                        f"ChapterImageItem Already Exists In The Database: {item!r}"
                                    )

                        else:
                            raise DropItem(f"ChapterImageItem has not images: {item!r}")
                        return item
                    else:

                        raise DropItem(
                            f"ChapterItem Already Exists In The Database: {item!r}"
                        )

                else:
                    raise DropItem(
                        f"ComicItem Does Not Exists In The Database: {item!r}"
                    )

        else:
            raise DropItem(f"CrawlerDbPipeline Item has a Missing field in: {item!r}")
