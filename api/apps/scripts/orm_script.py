from pprint import pprint

from django.db import connection
from django.db.models import Q
from django.utils import timezone

from api.apps.models import Comic, Chapter


def run():
    # tit_or_slu = Q(title__icontains="I Am the Fated Villain") & Q(
    #     slug__icontains="1908287720-i-am-the-fated-villain"
    # )

    # monthly_created = ~Q(created_at__gt=timezone.now() - timezone.timedelta(days=31))
    # not_monthly_created = ~Q(
    #     created_at__gt=timezone.now() - timezone.timedelta(days=31)
    # ) & Q(rating__gte=10.0)
    # yearly_created = ~Q(
    #     created_at__gt=timezone.now() - timezone.timedelta(days=186)
    # ) & Q(rating__gte=10.0)
    recently = Q(updated_at__gte=timezone.now() - timezone.timedelta(days=7))
    top = Q(updated_at__gte=timezone.now() - timezone.timedelta(days=2)) & Q(
        rating__gte=9.9
    )
    # top = Q(status=Comic.ComicStatus.ONGOING) | Q(rating__gte=10.0)
    # topcomics = Comic.objects.filter(top).order_by("-updated_at")[0:6]
    # todaycomics = Comic.objects.filter(recently).order_by("-updated_at")[0:4]
    # comic = Comic.objects.get(title="I Am the Fated Villain")
    # genres = [gen.id for gen in comic.genres.all()]
    # cat = comic.category.id
    # genresquery = Q(genres=genres[0])
    # catquery = Q(category=cat)
    # newcomics = (
    #     Comic.objects.select_related("category")
    #     .prefetch_related("genres")
    #     .filter(catquery & genresquery & not_monthly_created)
    # )
    # rating_has_number = Q(rating__regex=r"[9:10]+")
    # upcomics = Comic.objects.filter(not_monthly_created).values_list("slug", flat=True)
    # # chapters = comic.chapter_set.all()
    # chapters = Chapter.objects.select_related("comic").filter(comic__slug=comic.slug)
    # chapter = chapters[0]
    # panels = Panel.objects.select_related("chapter").filter(chapter__slug=chapter.slug)
    # print({"count": upcomics.count(), "data": upcomics})
    # pprint(connection.queries)
    # comics = Comic.objects.all()

    # chapters = Chapter.objects.all()
    # comic = comics.first()
    # chapter = comic.chapter_comic.all()
    # comic = comics.first()
    # type = comic.type.pk
    # typequery = Q(type__exact=type)
    # monthly_updated = Q(
    #     updated_at__gte=timezone.now() - timezone.timedelta(days=365),
    # ) & Q(rating__gte=10.0)
    # relatedcomics = (
    #     Comic.objects.select_related("type")
    #     .filter(typequery & monthly_updated)
    #     .order_by("updated_at")
    # )
    # for com in comics:
    #     images = com.comic_images.all()
    #     fimg = images.first().image.url
    #     context = {"fimg": fimg}
    #     if images.count() > 1:
    #         img = images[1].image.url
    #         context["simg"] = img
    #         pprint(com.pk)
    # pprint(context)
    # comic = Comic.objects.get(pk="111")
    # chapter = Chapter.objects.get(slug="demon-king-chapter-11")
    # comic = chapter.comic
    # chapter = chapters.first()
    # chapter_chapters = chapter.comic.chapter_comic.all()
    # rcomics = (
    #     Comic.objects.select_related("type").filter(
    #         Q(status=Comic.ComicStatus.ONGOING)
    #         & Q(type=chapter.comic.type)
    #         & Q(rating__gte=9.8)
    #     )
    # )[0:6]
    # genres = [gen.id for gen in comic.genres.all()[0:2]]
    # rcomics = (
    #     Comic.objects.prefetch_related("genres")
    #     .select_related("type")
    #     .filter(Q(genres__in=genres) & Q(type=comic.type))
    # )
    rcomics = Comic.objects.filter(recently)
    tcomics = Comic.objects.filter(top)
    chapters = Chapter.objects.all()

    pprint(
        {
            # "con": connection.queries,
            "tcomics": tcomics,
            "tcomicscount": tcomics.count(),
            # "comic_url": comic.url,
            # "genres": genres,
            "rcomics": rcomics,
            "rcomicscount": rcomics.count(),
            # "chapters": chapters,
            # "todaycomicscount": todaycomics.count(),
            # "todaycomics": todaycomics,
            # "topcomicscount": topcomics.count(),
            # "topcomics": topcomics,
            # "chapterscount": chapters.count(),
            # "chapters-count": chapter_chapters.count(),
            # "rcomics-count": rcomics.count(),
        }
    )
