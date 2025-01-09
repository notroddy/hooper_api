# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.TeamListView.as_view(), name='team-list-view'),
    path('teams/<str:abbreviation>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('teams/<str:abbreviation>/<int:year>/roster/', views.TeamRosterView.as_view(), name='team-roster-view'),
    path('players/<str:player_abbreviation>/', views.PlayerView.as_view(), name='player-view'),
    path('players/search/<str:first_name>/<str:last_name>/', views.PlayerSearchView.as_view(), name='player-search-view'),
]
