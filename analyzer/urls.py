from django.urls import path
from . import views
from .views import MatchScoreAndCulturalFitAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate_match/', MatchScoreAndCulturalFitAPIView.as_view(), name='match_score_api'),
]