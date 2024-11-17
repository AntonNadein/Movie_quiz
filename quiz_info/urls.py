from django.urls import path
from quiz_info.apps import QuizInfoConfig

from . import views

app_name = QuizInfoConfig.name

urlpatterns = [
    path("", views.home_page, name="home_page"),
    # path('video/<int:id_vid>', views.display_video),
]
