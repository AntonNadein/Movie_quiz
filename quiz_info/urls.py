from django.urls import path

from quiz_info.apps import QuizInfoConfig

from . import views

app_name = QuizInfoConfig.name

urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("film_list/", views.FilmListView.as_view(), name="list_film"),
    path("film_detail/<slug:slug>/", views.FilmDetailView.as_view(), name="film_detail"),
    path("celebrity_list/", views.CelebrityListView.as_view(), name="list_celebrity"),
    path("celebrity_detail/<slug:slug>/", views.CelebrityDetailView.as_view(), name="celebrity_detail"),
    path("celebrity_film/<slug:slug>/", views.CelebrityFilmDetailView.as_view(), name="celebrity_film"),
    path("film_actors/<slug:slug>/", views.FilmActorDetailView.as_view(), name="film_actors"),
    # path("base/", views.CarouselListView.as_view(), name="top_menu"),
    # path("base/", views.carousel_list, name="top_menu"),
    # path('video/<int:id_vid>', views.display_video),
]
