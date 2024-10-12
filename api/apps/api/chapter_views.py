from api.apps.serializers.chapter import ChaptersSerializer, ChapterSerializer
from api.apps.models import Chapter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def chapter_list(request):
    chapters = Chapter.objects.all()
    serializer = ChaptersSerializer(chapters, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    serializer = ChapterSerializer(chapter)

    return Response(serializer.data)
