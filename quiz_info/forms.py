from django import forms
from transliterate import translit
from django.core.exceptions import ValidationError

from .models import Films, Celebrity


class MixinQuiz:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CelebrityForm(MixinQuiz, forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = [
            "first_name",
            "last_name",
            "slug",
            "birthday",
            "country",
            "awards",
            "is_published",
            "photo",
            "title",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'slug' not in self.initial:
            self.fields['slug'].initial = 'default-slug'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        birthday = cleaned_data.get('birthday')
        slug = cleaned_data.get('slug')

        if first_name and last_name and birthday and 'default-slug' in slug:
            generated_slug = f"{first_name}-{last_name}-{birthday}"
            cleaned_data['slug'] = translit(generated_slug.lower(), 'ru', reversed=True)

        return cleaned_data


class FilmForm(MixinQuiz, forms.ModelForm):
    class Meta:
        model = Films
        fields = [
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
            "actors",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'slug' not in self.initial:
            self.fields['slug'].initial = 'default-slug'

    def clean(self):
        cleaned_data = super().clean()
        film_name = cleaned_data.get('film_name')
        year = cleaned_data.get('year')
        slug = cleaned_data.get('slug')

        if film_name and year and 'default-slug' in slug:

            new_name = ''
            for letter in translit(film_name, 'ru', reversed=True):
                spase = [' ']
                sym = ['"', ',', '.', '?', '!', '#', '@', "'"]
                if letter in sym:
                    continue
                elif letter in spase:
                    new_name += '-'
                else:
                    new_name += letter

            generated_slug = f"{new_name}-{year}"
            cleaned_data['slug'] = generated_slug

        return cleaned_data
