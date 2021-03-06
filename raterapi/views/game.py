"""View module for handling requests about game types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Game, Category
from django.contrib.auth.models import User
from django.db.models import Q


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        
        search_text = self.request.query_params.get('q', None)
        order_text = self.request.query_params.get('orderby', None)

        if search_text is not None:
            games = Game.objects.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
            )
        if order_text is not None:
            games = Game.objects.order_by(order_text)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        user = User.objects.get(pk=request.auth.user.id)
        
        game = Game.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            designer=request.data["designer"],
            year_released=request.data["yearReleased"],
            number_of_players=request.data["numberOfPlayers"],
            hours_playtime=request.data["hoursPlaytime"],
            min_age_recommended=request.data["minAgeRecommended"],
            user=user
        )

        game.categories.add(request.data["categoryId"])

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.hours_playtime = request.data["hoursPlaytime"]
        game.min_age_recommended = request.data["minAgeRecommended"]

        category = Category.objects.get(pk=request.data["categoryId"])
        game.categories.add(category)

        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        depth = 1
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'number_of_players',
                  'hours_playtime', 'min_age_recommended', 'categories', 'average_rating', 'user')
