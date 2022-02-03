"""View module for handling requests about review types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Review
from django.contrib.auth.models import User


class ReviewView(ViewSet):
    """Level up review types view"""

    def list(self, request):
        """Handle GET requests to get all review types

        Returns:
            Response -- JSON serialized list of review types
        """
        reviews = Review.objects.all()

        game = request.query_params.get('game', None)
        if game is not None:
            reviews = reviews.filter(game_id=game)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """
        
        user = User.objects.get(pk=request.auth.user.id)

        review = Review.objects.create(
            review=request.data["review"],
            game_id= request.data["gameId"],
            user=user
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review types
    """
    class Meta:
        model = Review
        depth = 1
        fields = "__all__"
