from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CelebrityForm, FilmForm

from .models import *


class HomePage(ListView):
    model = Films
    template_name = "quiz_info/index.html"
    context_object_name = "films"

    def get_queryset(self):
        return self.model.published.order_by("-created_at")[:3].select_related('image')


class FilmListView(ListView):
    model = Films

    def get_queryset(self):
        return self.model.published.order_by("film_name").select_related('image')


class FilmDetailView(DetailView):

    def get_queryset(self):
        return Films.published.prefetch_related('actors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actors = self.object.actors.all()
        context["actors"] = actors[:3]
        return context


class CelebrityListView(ListView):
    model = Celebrity

    def get_queryset(self):
        return self.model.published.order_by("first_name").select_related('photo')


class CelebrityDetailView(DetailView):
    model = Celebrity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor = self.object
        context["films"] = actor.film_actors.all()[:3]
        return context


class CelebrityFilmDetailView(DetailView):
    model = Celebrity
    template_name = "quiz_info/celebrity_films_detail.html"

    def get(self, request, *args, **kwargs):
        celebrity_slug = kwargs.get("slug")
        celebrity = get_object_or_404(Celebrity, slug=celebrity_slug)
        film = Films.objects.filter(actors=celebrity).select_related('image')
        context = {"celebrity": celebrity, "films": film}
        return self.render_to_response(context)


class FilmActorDetailView(DetailView):
    model = Films
    template_name = "quiz_info/films_actors_detail.html"

    def get(self, request, *args, **kwargs):
        film_slug = kwargs.get("slug")
        film = get_object_or_404(Films, slug=film_slug)
        actors = Celebrity.objects.filter(film_actors=film).select_related('photo')
        context = {"actors": actors, "film": film}
        return self.render_to_response(context)


class CelebrityCreateView(CreateView):
    model = Celebrity
    form_class = CelebrityForm
    template_name = "quiz_info/forms/celebrity_form.html"
    success_url = reverse_lazy("quiz_info:list_celebrity")


class CelebrityUpdateView(UpdateView):
    model = Celebrity
    form_class = CelebrityForm
    template_name = "quiz_info/forms/celebrity_form.html"
    success_url = reverse_lazy("quiz_info:list_celebrity")


class CelebrityDeleteView(DeleteView):
    model = Celebrity
    template_name = "quiz_info/delete/celebrity_confirm_delete.html"
    success_url = reverse_lazy("quiz_info:list_celebrity")


class FilmCreateView(CreateView):
    model = Films
    form_class = FilmForm
    template_name = "quiz_info/forms/film_form.html"
    success_url = reverse_lazy("quiz_info:list_film")


class FilmUpdateView(UpdateView):
    model = Films
    form_class = FilmForm
    template_name = "quiz_info/forms/film_form.html"
    success_url = reverse_lazy("quiz_info:list_film")


class FilmDeleteView(DeleteView):
    model = Films
    template_name = "quiz_info/delete/film_confirm_delete.html"
    success_url = reverse_lazy("quiz_info:list_film")

# def display_video(request, id_vid=None):
#     if id_vid is None:
#         return HttpResponse("No Video")
#     try:
#         video_object = get_object_or_404(Videos, pk=id_vid)
#     except Videos.DoesNotExist:
#         return HttpResponse("Id doesn't exists.")
#     return render(request, "quiz_info/video_template.html", {"vid_dict": video_object})
