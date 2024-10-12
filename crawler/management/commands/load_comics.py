import json
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q

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

User = get_user_model()


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        def save_comic():
            user = User.objects.filter(
                Q(email__iexact="admin@rhixe.company") | Q(username__iexact="adminbot"),
            ).first()
            if not user:
                user = User.objects.create_superuser(
                    email="admin@rhixe.company",
                    username="adminbot",
                    password="R4I7gcJHX",
                )
            base = settings.BASE_DIR
            comics_file = str(base / "comics.json")
            with open(comics_file) as f:
                comics_data = json.load(f)
                for c in comics_data:
                    ty = Type.objects.filter(
                        Q(name__iexact=c["type"]),
                    ).get_or_create(
                        name=c["type"]
                    )[0]
                    au = Author.objects.filter(
                        Q(name__iexact=c["author"]),
                    ).get_or_create(name=c["author"])[0]
                    ar = Artist.objects.filter(
                        Q(name__iexact=c["artist"]),
                    ).get_or_create(name=c["artist"])[0]

                    comic = Comic.objects.filter(Q(slug__iexact=c["slug"])).first()

                    if not comic:
                        co = Comic.objects.filter(
                            Q(slug__iexact=c["slug"]),
                        ).get_or_create(
                            user=user,
                            type=ty,
                            artist=ar,
                            author=au,
                            title=c["title"],
                            slug=c["slug"],
                            description=c["description"],
                            rating=c["rating"],
                            status=c["status"],
                            url=c["url"],
                            spider=c["spider"],
                            updated_at=c["updated_at"],
                            # downloaded_at=c["downloaded_at"],
                            numChapters=0,
                            serialization=c["serialization"],
                        )[
                            0
                        ]
                        genres = c["genres"]
                        if genres:
                            for gen in genres:
                                ge = Genre.objects.filter(
                                    Q(name__iexact=gen),
                                ).get_or_create(name=gen)[0]
                                co.genres.add(ge)
                                co.save()
                        images = c["images"]
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
                                    ).get_or_create(url=img_url,)[0]
                                    lmm = ComicImagesItem.objects.filter(
                                        pannquery
                                    ).first()
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
                                    title = ComicImage.objects.get(panquery).image
                                    pprint(
                                        f"{title} Couldnt be saved because it already exists"
                                    )
                                    pass

                    else:
                        numchap = comic.chapter_comic.all().count()
                        co = Comic.objects.update(
                            user=user,
                            type=ty,
                            artist=ar,
                            author=au,
                            # title=c["title"],
                            # slug=c["slug"],
                            description=c["description"],
                            rating=c["rating"],
                            status=c["status"],
                            url=c["url"],
                            spider=c["spider"],
                            updated_at=c["updated_at"],
                            # downloaded_at=c["downloaded_at"],
                            numChapters=numchap,
                            serialization=c["serialization"],
                        )

                        pprint(
                            f"{c["title"]} Couldnt be saved because it already exists"
                        )
                        pass
            pprint(
                {
                    "Comics": Comic.objects.all().values(),
                    "ComicsImage": ComicImage.objects.all().values(),
                    "ComicsImagesItem": ComicImagesItem.objects.all().values(),
                },
            )
            return

        def save_chapter():
            base = settings.BASE_DIR

            chapters_file = str(base / "chapters.json")
            with open(chapters_file) as f:
                chapters_data = json.load(f)
                for ch in chapters_data:
                    co = Comic.objects.filter(
                        Q(slug__iexact=ch["comicslug"])
                        | Q(title__iexact=ch["comictitle"])
                    ).first()
                    imgs = ch["images"]
                    if co:
                        numchap = co.chapter_comic.all().count() + 1
                        chapterss = Chapter.objects.filter(
                            Q(slug__iexact=ch["chapterslug"]),
                        ).first()
                        if chapterss:
                            cha = Chapter.objects.update(
                                comic=co,
                                name=ch["chaptername"],
                                # downloaded_at=ch["downloaded_at"],
                                updated_at=ch["updated_at"],
                                # slug=ch["chapterslug"],
                                url=ch["url"],
                                spider=ch["spider"],
                                numPages=len(imgs),
                            )
                            co.numChapters = numchap
                            co.save()
                            pprint(
                                f"{ch["chaptername"]} Couldnt be saved because it already exists"
                            )
                            pass
                        else:

                            cha = Chapter.objects.filter(
                                Q(slug__iexact=ch["chapterslug"]),
                            ).get_or_create(
                                comic=co,
                                name=ch["chaptername"],
                                # downloaded_at=ch["downloaded_at"],
                                updated_at=ch["updated_at"],
                                slug=ch["chapterslug"],
                                url=ch["url"],
                                spider=ch["spider"],
                                numPages=len(imgs),
                            )[
                                0
                            ]

                            if imgs:
                                for img in imgs:
                                    panelll = ChapterImage.objects.filter(
                                        Q(url__iexact=img["url"]),
                                    ).first()
                                    if panelll:
                                        pass
                                    else:

                                        pa = ChapterImage.objects.filter(
                                            Q(url__iexact=img["url"]),
                                        ).get_or_create(url=img["url"],)[0]
                                        paas = ChapterImagesItem.objects.filter(
                                            Q(image__iexact=img["path"]),
                                        ).first()
                                        if not paas:
                                            paa = ChapterImagesItem.objects.filter(
                                                Q(image__iexact=img["path"]),
                                            ).get_or_create(
                                                chapter=cha,
                                                comic=co,
                                                link=pa,
                                                image=img["path"],
                                            )[
                                                0
                                            ]
                    else:
                        print("Comic not Found!!")
                        pass
            pprint(
                {
                    "Chapters": Chapter.objects.all().values(),
                    "ChaptersImage": ChapterImage.objects.all().values(),
                    "ChaptersImagesItem": ChapterImagesItem.objects.all().values(),
                },
            )
            return

        save_comic()
        save_chapter()
        pprint(
            {
                "ComicsCount": Comic.objects.all().count(),
                "ComicsImageCount": ComicImage.objects.all().count(),
                "ComicsImagesItemCount": ComicImagesItem.objects.all().count(),
                "ChaptersCount": Chapter.objects.all().count(),
                "ChaptersImageCount": ChapterImage.objects.all().count(),
                "ChaptersImagesItemCount": ChapterImagesItem.objects.all().count(),
            },
        )
