from rest_framework import generics
from data.models import Team
from .serializers import TeamSerializer
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from services.logic import (
    PlayerStatsFetcher,
    fetch_team_page_data,
    fetch_team_current_season_data,
    fetch_team_roster,
    search_players,
)
import csv
import io


class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(View):
    def get(self, request, abbreviation):
        team = get_object_or_404(Team, abbreviation=abbreviation)

        try:
            team_page_data = fetch_team_page_data(team)
            team_season_data = fetch_team_current_season_data(team)

            data = {
                "message": "Successfully fetched team page data",
                "team_url": team.url,
                "team_name": team.name,
                "abbreviation": team.abbreviation,
                "team_location": team_page_data["location"],
                "playoff_appearances": team_page_data["playoff_appearances"],
                "championships": team_page_data["championships"],
                "team_record": team_season_data["record"],
                "standings": team_season_data["standings_position"],
                "conference": team_season_data["conference"],
                "coach": team_season_data["coach"],
            }

            if request.GET.get('format') == 'csv':
                return self.to_csv(data, 'team_detail.csv')
            else:
                return JsonResponse(data)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)

    def to_csv(self, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        for key, value in data.items():
            writer.writerow([key, value])

        return response


class TeamRosterView(View):
    def get(self, request, abbreviation, year):
        team = get_object_or_404(Team, abbreviation=abbreviation)

        try:
            roster = fetch_team_roster(team, year)

            data = {
                "message": "Successfully fetched team roster",
                "team_url": team.url,
                "team_name": team.name,
                "abbreviation": team.abbreviation,
                "year": year,
                "roster": roster,
            }

            if request.GET.get('format') == 'csv':
                return self.to_csv(data, 'team_roster.csv')
            else:
                return JsonResponse(data)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)

    def to_csv(self, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key])
                for item in value:
                    writer.writerow(item.values())
            else:
                writer.writerow([key, value])

        return response


class PlayerView(View):
    def get(self, request, player_abbreviation):
        try:
            stats_fetcher = PlayerStatsFetcher(player_abbreviation)

            stats_fetcher.fetch_page()

            player_name, position = stats_fetcher.parse_player_info()

            stats = stats_fetcher.parse_player_stats()

            all_star_content = stats_fetcher.parse_all_star_appearances()

            payload = {
                "message": "Successfully fetched player data",
                "player_name": player_name,
                "player_abbreviation": player_abbreviation,
                "position": position,
                **stats, 
            }

            if all_star_content:
                payload["all_star_appearances"] = all_star_content

            if request.GET.get('format') == 'csv':
                return self.to_csv(payload, 'player_detail.csv')
            else:
                return JsonResponse(payload)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def to_csv(self, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        for key, value in data.items():
            writer.writerow([key, value])

        return response


class PlayerSearchView(View):
    def get(self, request, first_name, last_name):
        try:
            players = search_players(first_name, last_name)
            data = {
                "message": "Successfully fetched player search results",
                "players": players,
            }

            if request.GET.get('format') == 'csv':
                return self.to_csv(data, 'player_search.csv')
            else:
                return JsonResponse(data)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)

    def to_csv(self, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key])
                for item in value:
                    writer.writerow(item.values())
            else:
                writer.writerow([key, value])

        return response
