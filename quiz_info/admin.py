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
    """Фильмы"""
    list_display = (
        "slug",
        "is_published",
        "film_name",
        "year",
        "country",
        "director",
        "composer",
        "get_actors",
        "awards",
        "rating",
        "video",
        "image",
        "budget",
    )
    list_editable = ("film_name",)
    list_display_links = ("slug", "is_published",)
    list_filter = ("is_published", "year", "country", "awards",)
    list_per_page = 20
    search_fields = ("film_name",)
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

    @admin.action(description='Список актеров')
    def get_actors(self, obj):
        """Добавление списка актеров в list_display"""
        actors = obj.actors.all()
        return ", ".join([str(actor) for actor in actors])

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Переопределение foreignkey для сортировки 'Режиссера' и 'Композитора'"""
        if db_field.name == "director":
            kwargs["queryset"] = Celebrity.objects.filter(employment__employment="Режиссер").order_by('last_name',
                                                                                                      'first_name')
        elif db_field.name == "composer":
            kwargs["queryset"] = Celebrity.objects.filter(employment__employment="Композитор").order_by('last_name',
                                                                                                        'first_name')
        elif db_field.name == "image":
            kwargs["queryset"] = MediaFileImage.objects.filter(relation="film").order_by('image_name',)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Переопределение manytomany для сортировки 'Актеров'"""
        if db_field.name == "actors":
            kwargs["queryset"] = Celebrity.objects.filter(employment__employment="Актер").order_by('last_name',
                                                                                                   'first_name')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Celebrity)
class CelebrityAdmin(MixinAdmin, admin.ModelAdmin):
    """Звезды"""
    list_display = (
        "slug",
        "is_published",
        "first_name",
        "last_name",
        "birthday",
        "country",
        "awards",
        # "get_film", Добавление списка фильмов для актеров
        "created_at",
        "updated_at",
        "photo",
    )
    list_editable = ("first_name", "last_name",)
    list_display_links = ("slug", "is_published",)
    list_filter = ("is_published", "awards", "employment", "country",)
    list_per_page = 20
    search_fields = ("last_name", "first_name",)
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

    # раскоментируйте для добавления
    # @admin.action(description='Список фильмов')
    # def get_film(self, obj):
    #     """Добавление списка фильмов для актеров в list_display"""
    #     films = obj.film_actors.all()
    #     return ", ".join([film.film_name for film in films])

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Переопределение foreignkey для сортировки 'Режиссера' и 'Композитора'"""

        if db_field.name == "photo":
            kwargs["queryset"] = MediaFileImage.objects.filter(relation="celebrity").order_by('image_name', )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Awards)
class AwardsAdmin(admin.ModelAdmin):
    """Награды"""
    list_display = (
        "id",
        "name_awards",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name_awards",)
    list_filter = ("name_awards",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Семья"""
    list_display = (
        "id",
        "name_family",
        "he",
        "she",
        "created_at",
        "updated_at",
    )
    list_filter = ("name_family",)
    list_display_links = ("id", "name_family",)
    list_per_page = 20


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Страна"""
    list_display = (
        "id",
        "name_country",
        "created_at",
        "updated_at",
    )
    list_filter = ("name_country",)
    list_display_links = ("id", "name_country",)
    list_per_page = 20


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    """Вид деятельности"""
    list_display = (
        "id",
        "employment",
        "created_at",
        "updated_at",
    )
    list_filter = ("employment",)
    list_display_links = ("id", "employment",)


@admin.register(MediaFileImage)
class MediaFileImageAdmin(admin.ModelAdmin):
    """Изображения"""
    list_display = (
        "id",
        "relation",
        "image_name",
        "image_easy",
        "image_medium",
        "image_hard",
    )
    list_filter = ("relation",)
    list_display_links = ("id", "image_name",)
    list_editable = ('relation', )
    list_per_page = 20


@admin.register(MediaFileVideo)
class MediaFileVideoAdmin(admin.ModelAdmin):
    """Видеофайлы"""
    list_display = (
        "id",
        "video_name",
        "video_file",
    )
    list_filter = ("video_name",)
    list_display_links = ("id", "video_name",)
    list_per_page = 20


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """Меню карусели"""
    list_display = (
        "id",
        "film_carousel",
        "carousel_info",
        "slide_number",
        "image",
        "slogan",
    )
    ordering = ("slide_number",)
    list_display_links = ("id", "film_carousel",)
    list_per_page = 20


@admin.register(RoundMenu)
class RoundMenuAdmin(admin.ModelAdmin):
    """Круглое меню"""
    list_display = (
        "id",
        "menu_name",
        "image",
        "image_number",
    )
    ordering = ("image_number",)
    list_display_links = ("id", "menu_name",)
    list_per_page = 20
