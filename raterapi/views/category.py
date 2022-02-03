"""View module for handling requests about game types"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Category


class CategoryView(ViewSet):
    """Level up game types view"""

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category types
    """
    class Meta:
        model = Category
        fields = "__all__"
