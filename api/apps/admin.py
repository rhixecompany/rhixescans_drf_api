from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from import_export.admin import ImportExportModelAdmin
from import_export.forms import ExportForm
from import_export.forms import ImportForm
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.forms.widgets import ArrayWidget
from unfold.contrib.forms.widgets import WysiwygWidget

from api.apps.models import Artist
from api.apps.models import Author
from api.apps.models import Chapter
from api.apps.models import ChapterImagesItem
from api.apps.models import ChapterImage
from api.apps.models import Comic
from api.apps.models import ComicImage
from api.apps.models import ComicImagesItem
from api.apps.models import Comment
from api.apps.models import Genre
from api.apps.models import Type
from api.apps.models import UsersItem


class CommentInline(TabularInline):
    model = Comment
    # extra = 2
    tab = True


class ComicInline(TabularInline):
    model = Comic
    # extra = 2
    tab = True


class ChapterInline(TabularInline):
    model = Chapter
    # extra = 2
    tab = True


@admin.register(Comic)
class ComicAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Comic
    search_fields = (
        "title",
        "slug",
    )
    # Display submit button in filters
    list_filter_submit = True

    list_filter = (
        "status",
        ("updated_at", RangeDateTimeFilter),  # Date filter
        ("created_at", RangeDateTimeFilter),  # Datetime filter
    )

    list_display = ("title",)
    # prepopulated_fields = {"slug": ("title",)}
    inlines = [ChapterInline]

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = [
        "comic_completed_action",
        "comic_ongoing_action",
        "comic_hiatus_action",
        "comic_dropped_action",
        "comic_season_end_action",
        "comic_coming_soon_action",
    ]
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }

    @admin.action(description="Mark selected Comic as completed")
    def comic_completed_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.COMPLETED)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.COMPLETED)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been completed",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been completed.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as completed and users have been notified.",
        )

    @admin.action(description="Mark selected Comic as ongoing")
    def comic_ongoing_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.ONGOING)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.ONGOING)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been ongoing",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been ongoing.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as ongoing and users have been notified.",
        )

    @admin.action(description="Mark selected Comic as hiatus")
    def comic_hiatus_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.HIATUS)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.HIATUS)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been hiatus",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been hiatus.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as hiatus and users have been notified.",
        )

    @admin.action(description="Mark selected Comic as dropped")
    def comic_dropped_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.DROPPED)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.DROPPED)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been dropped",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been dropped.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as dropped and users have been notified.",
        )

    @admin.action(description="Mark selected Comic as Season End")
    def comic_season_end_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.SEASON_END)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.SEASON_END)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been season_end",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been Season End.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as Season End and users have been notified.",
        )

    @admin.action(description="Mark selected Comic as Coming Soon")
    def comic_coming_soon_action(self, request, queryset):
        comics_to_comp = queryset.exclude(status=Comic.ComicStatus.COMING_SOON)
        comics = list(comics_to_comp)

        comics_to_comp.update(status=Comic.ComicStatus.COMING_SOON)

        for comic in comics:
            user = comic.user
            user.email_user(
                "Your comic has been coming_soon",
                f"Dear {user.username}, \n\nYour comic with Title {comic.title} has been Coming Soon.",
                f"{user.email}",
                fail_silently=False,
            )
        self.message_user(
            request,
            "Selected comics have been marked as Coming Soon and users have been notified.",
        )


@admin.register(Chapter)
class ChapterAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Chapter
    search_fields = ("name",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = (
        "name",
        ("updated_at", RangeDateTimeFilter),  # Date filter
        ("created_at", RangeDateTimeFilter),  # Datetime filter
    )

    list_display = ("name",)
    inlines = [CommentInline]

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(ComicImagesItem)
class ComicImagesItemAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = ComicImagesItem
    search_fields = (
        "link__url",
        "image",
    )
    # Display submit button in filters
    list_filter_submit = True

    list_filter = (
        "link__url",
        "image",
    )

    list_display = (
        "link__url",
        "image",
    )
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(ChapterImagesItem)
class ChapterImagesItemAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = ChapterImagesItem
    search_fields = (
        "link__url",
        "image",
    )
    # Display submit button in filters
    list_filter_submit = True

    list_filter = (
        "link__url",
        "image",
    )

    list_display = (
        "link__url",
        "image",
    )
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Genre)
class GenreAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Genre
    search_fields = ("name",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = ("name",)

    list_display = ("name",)
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Type)
class TypeAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Type
    search_fields = ("name",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = ("name",)

    list_display = ("name",)
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Author)
class AuthorAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Author
    search_fields = ("name",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = ("name",)

    list_display = ("name",)
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Artist)
class ArtistAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Artist
    search_fields = ("name",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = ("name",)

    list_display = ("name",)
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Comment)
class CommentAdminClass(ModelAdmin, ImportExportModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    model = Comment
    search_fields = ("body",)
    # Display submit button in filters
    list_filter_submit = True

    list_filter = (
        "body",
        ("created_at", RangeDateTimeFilter),
    )

    list_display = ("body",)
    inlines = []

    # Display changelist in fullwidth
    list_fullwidth = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail
    actions = []
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


admin.site.register(UsersItem)
admin.site.register(ComicImage)
admin.site.register(ChapterImage)
