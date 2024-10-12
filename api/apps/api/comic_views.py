from api.apps.serializers.comic import ComicsSerializer, ComicSerializer
from api.apps.models import Comic
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def comic_list(request):
    comics = Comic.objects.all()[0:44]
    serializer = ComicsSerializer(comics, many=True, context={"request": request})

    return Response(serializer.data)


@api_view(["GET"])
def comic_detail(request, pk):

    comic = get_object_or_404(Comic, pk=pk)
    serializer = ComicSerializer(comic)

    return Response(serializer.data)
