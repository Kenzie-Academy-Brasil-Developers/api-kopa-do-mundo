import ipdb
from django.forms.models import model_to_dict
from rest_framework.views import APIView, Request, Response, status

from .models import Team
from .utils import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
    data_processing,
)


class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        team_list = []
        for team in teams:
            team_dict = model_to_dict(team)
            team_list.append(team_dict)

        return Response(team_list, 200)

    def post(self, request: Request) -> Response:
        try:
            valid_data = data_processing(request.data)
        except NegativeTitlesError:
            return Response({"error": "titles cannot be negative"}, 400)
        except InvalidYearCupError:
            return Response({"error": "there was no world cup this year"}, 400)
        except ImpossibleTitlesError:
            return Response(
                {"error": "impossible to have more titles than disputed cups"}, 400
            )

        teams = Team.objects.create(**request.data)
        team_dict = model_to_dict(teams)
        return Response(team_dict, 201)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: str) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        # ipdb.set_trace()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)
        return Response(team_dict, 200)

    def delete(self, request: Request, team_id: str) -> Response:
        try:
            team = Team.objects.get(id=team_id)
            team.delete()
        # ipdb.set_trace()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, team_id: str) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        # ipdb.set_trace()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)
        return Response(team_dict, 200)


# Create your views here.
