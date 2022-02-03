"""View module for handling requests about rating types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Rating
from django.contrib.auth.models import User


class RatingView(ViewSet):
    """Level up rating types view"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """
        
        user = User.objects.get(pk=request.auth.user.id)

        rating = Rating.objects.create(
            rating= request.data["rating"],
            game_id= request.data["gameId"],
            user=user
        )

        serializer = RatingSerializer(rating)
        return Response(serializer.data)


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for rating types
    """
    class Meta:
        model = Rating
        fields = "__all__"
