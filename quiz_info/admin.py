from django.contrib import admin

from quiz_info.models import *


class MixinAdmin(admin.ModelAdmin):
    actions = ["is_published", "is_draft"]

    @admin.action(description="Опубликовать статьи")
    def is_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Статьи в черновики")
    def is_draft(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Films)
class FilmsAdmin(MixinAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "is_published",
        "film_name",
        "slug",
        "year",
        "country",
        "director",
        "composer",
        "budget",
        "awards",
        "rating",
        "video",
        "image",
        # "description",
    )
    list_filter = ("film_name", "year", "country", "director", "composer")
    search_fields = ("film_name", "actors", "director", "composer")
    ordering = ("film_name", "year")
    filter_horizontal = ("actors",)
    prepopulated_fields = {"slug": ["film_name"]}
    fields = [
        ("film_name", "slug"),
        ("country", "year"),
        ("director", "composer"),
        "actors",
        ("rating", "budget"),
        ("video", "image"),
        "awards",
        "description",
        "is_published",
    ]


@admin.register(Celebrity)
class CelebrityAdmin(MixinAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "slug",
        "birthday",
        "country",
        "awards",
        "is_published",
        "created_at",
        "updated_at",
        "photo",
    )
    list_filter = ("last_name", "birthday", "awards")
    search_fields = ("last_name", "country", "awards")
    ordering = ("first_name",)
    filter_horizontal = ("employment",)
    prepopulated_fields = {"slug": ["last_name", "first_name"]}
    fields = [
        ("first_name", "last_name", "slug"),
        ("birthday", "country"),
        "employment",
        "photo",
        "awards",
        "is_published",
        "title",
    ]


@admin.register(Awards)
class AwardsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_awards",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_filter = ("name_awards",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_family",
        "he",
        "she",
        "created_at",
        "updated_at",
    )
    list_filter = ("name_family", "he", "she")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_country",
        "created_at",
        "updated_at",
    )
    list_filter = ("name_country",)


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employment",
        "created_at",
        "updated_at",
    )
    list_filter = ("employment",)


@admin.register(MediaFileImage)
class MediaFileImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_name",
        "image_easy",
        "image_medium",
        "image_hard",
    )
    list_filter = ("image_name",)


@admin.register(MediaFileVideo)
class MediaFileVideoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "video_name",
        "video_file",
    )
    list_filter = ("video_name",)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "film_carousel",
        "carousel_info",
        "slide_number",
        "image",
        "slogan",
    )
    ordering = ("slide_number",)


@admin.register(RoundMenu)
class RoundMenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "menu_name",
        "image",
        "image_number",
    )
    ordering = ("image_number",)
