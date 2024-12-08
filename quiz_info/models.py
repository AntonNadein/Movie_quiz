from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    class Status(models.IntegerChoices):
        PUBLISHED = True, "Опубликовано"
        DRAFT = False, "Черновик"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=PublishedManager.Status.PUBLISHED)


class Films(models.Model):
    """Фильмы"""
    film_name = models.CharField(max_length=255, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание фильма")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL фильма",
        help_text="Уникальное имя формируется из названия фильма",
    )
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1895), MaxValueValidator(datetime.now().year)],
        verbose_name="Год выпуска",
        help_text="Используйте формат года: (YYYY)",
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_DEFAULT,
        default="Страна производства не указана",
        related_name="film_country",
        verbose_name="Страна",
    )
    director = models.ForeignKey(
        "Celebrity", on_delete=models.PROTECT, related_name="director", verbose_name="Режиссер"
    )
    actors = models.ManyToManyField("Celebrity", related_name="film_actors", verbose_name="Актеры")
    composer = models.ForeignKey(
        "Celebrity", on_delete=models.PROTECT, related_name="composer", verbose_name="Композитор"
    )
    budget = models.PositiveIntegerField(verbose_name="Бюджет фильма в миллионах долларов")
    awards = models.ForeignKey(
        "Awards",
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default="Нет наград",
        related_name="film_awards",
        verbose_name="Награды",
    )
    video = models.ForeignKey(
        "MediaFileVideo",
        on_delete=models.SET_DEFAULT,
        default="Нет видеоролика", 
        related_name="video",
        verbose_name="Видеоролик",
    )
    image = models.ForeignKey(
        "MediaFileImage",
        on_delete=models.SET_DEFAULT,
        default="Нет скриншота",
        related_name="image",
        verbose_name="Скриншот",
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Рейтинг"
    )
    is_published = models.BooleanField(
        choices=PublishedManager.Status.choices, default=PublishedManager.Status.PUBLISHED, verbose_name="Публикация"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"{self.film_name} ({self.year} год) Режиссер: {self.director}"

    def get_absolute_url(self):
        return reverse("quiz_info:film_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["year", "film_name", "director", "country", "rating", "is_published"]


class Celebrity(models.Model):
    """Звезды"""
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
        help_text="Уникальное имя формируется из фамилии и имени",
    )
    photo = models.ForeignKey(
        "MediaFileImage",
        on_delete=models.SET_DEFAULT,
        default="Нет фото",
        related_name="photo",
        verbose_name="Фотография",
    )
    birthday = models.DateField(verbose_name="Дата рождения", help_text="Формат даты: (YYYY-MM-DD)")
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_DEFAULT,
        default="Страна рождения не указана",
        related_name="celebrity_country",
        verbose_name="Страна рождения",
    )
    employment = models.ManyToManyField("Employment", related_name="employment_actors", verbose_name="Кем работает")
    awards = models.ForeignKey(
        "Awards",
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default="Нет наград",
        related_name="celebrity_awards",
        verbose_name="Награды",
    )
    title = models.TextField(null=True, blank=True, verbose_name="Статья")
    is_published = models.BooleanField(
        choices=PublishedManager.Status.choices, default=PublishedManager.Status.PUBLISHED, verbose_name="Публикация"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("quiz_info:celebrity_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "известную личность"
        verbose_name_plural = "Известные личности"
        ordering = ["last_name", "birthday"]


class Awards(models.Model):
    """Награды"""
    name_awards = models.CharField(max_length=255, default="Нет наград", verbose_name="Название награды")
    quantity = models.PositiveIntegerField(verbose_name="Количество наград")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.name_awards} {self.quantity} шт."

    class Meta:
        verbose_name = "награду"
        verbose_name_plural = "Награды"
        ordering = [
            "name_awards",
        ]


class Contact(models.Model):
    """Семья"""
    name_family = models.CharField(
        max_length=255, verbose_name="Название семьи", help_text="Название семьи (например: Семья Ивановых)"
    )
    he = models.OneToOneField(
        "Celebrity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="husband",
        verbose_name="Муж",
    )
    she = models.OneToOneField(
        "Celebrity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wife",
        verbose_name="Жена",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Муж: {self.he} - Жена: {self.she}"

    class Meta:
        verbose_name = "отношения"
        verbose_name_plural = "Отношения"


class Country(models.Model):
    """Страны"""
    name_country = models.CharField(max_length=255, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.name_country

    class Meta:
        verbose_name = "страну"
        verbose_name_plural = "Страны"


class Employment(models.Model):
    """Вид деятельности"""
    employment = models.CharField(max_length=255, verbose_name="Род деятельности", help_text="Актер, Режиссер, и др.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.employment

    class Meta:
        verbose_name = "род деятельности"
        verbose_name_plural = "Род деятельности"


class MediaFileImage(models.Model):
    """Изображения"""
    FILM = "film"
    CELEBRITY = "celebrity"

    STATUS = [(FILM, "Фильм"), (CELEBRITY, "Звезда")]

    image_name = models.CharField(
        max_length=255, verbose_name="Название изображения", help_text="Название изображения для вывода"
    )
    relation = models.CharField(
        max_length=255, choices=STATUS, verbose_name="Категория")
    image_easy = models.ImageField(
        upload_to="images/easy",
        verbose_name="Главное фото/ Постер",
        help_text="Загрузите главное фото для знаменитости, или постер для фильма",
    )
    image_medium = models.ImageField(
        upload_to="images/medium",
        null=True,
        blank=True,
        verbose_name="Изображение сложность: средняя",
        help_text="Загрузите изображение для вывода в квизе на уровне сложности: средний",
    )
    image_hard = models.ImageField(
        upload_to="images/hard",
        null=True,
        blank=True,
        verbose_name="Изображение сложность: сложно",
        help_text="Загрузите изображение для вывода в квизе на уровне сложности: сложно",
    )

    def __str__(self):
        return self.image_name

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "Изображения"


class MediaFileVideo(models.Model):
    """Видео"""
    video_name = models.CharField(
        max_length=255, blank=False, verbose_name="Название видео", help_text="Название видео для вывода"
    )
    video_file = models.FileField(upload_to="videos", null=True, blank=True, verbose_name="Видеофайл")

    def __str__(self):
        return self.video_name

    class Meta:
        verbose_name = "видеозапись"
        verbose_name_plural = "Видеозаписи"


class Carousel(models.Model):
    """Меню карусели"""
    film_carousel = models.CharField(
        max_length=255, verbose_name="Название фильма", help_text="Название фильма для вывода"
    )
    slogan = models.CharField(
        max_length=255, verbose_name="Слоган фильма", help_text="Информация для вывода 255 символов"
    )
    carousel_info = models.OneToOneField(
        "Films",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="film",
        verbose_name="Меню карусели",
        help_text="Для создания ссылки на фильм",
    )
    slide_number = models.PositiveIntegerField(
        verbose_name="Номер слайда", help_text="Порядок отоброжения слайдов следите что бы номера не повторялись"
    )
    image = models.ImageField(
        upload_to="images/top_menu",
        verbose_name="Изображение",
        help_text="Загрузите изображение 2600х800 пикселей",
    )

    def __str__(self):
        return self.film_carousel

    class Meta:
        verbose_name = "меню карусели"
        verbose_name_plural = "Меню карусели"


class RoundMenu(models.Model):
    """Круглые меню"""
    menu_name = models.CharField(
        max_length=255, verbose_name="Название категории", help_text="Название категории для вывода"
    )
    image = models.ImageField(
        upload_to="images/round_menu",
        verbose_name="Изображение",
        help_text="Загрузите изображение 2600х800 пикселей",
    )
    image_number = models.PositiveIntegerField(
        verbose_name="Номер картинки", help_text="Определяет положение картинки на странице"
    )

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = "настройки круглого меню"
        verbose_name_plural = "Круглое меню"
