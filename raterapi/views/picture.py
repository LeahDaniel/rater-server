import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Picture, Game


class PictureView(ViewSet):
    """Level up picture types view"""

    def list(self, request):
        """Handle GET requests to get all picture types

        Returns:
            Response -- JSON serialized list of picture types
        """
        pictures = Picture.objects.all()

        game = request.query_params.get('game', None)
        if game is not None:
            pictures = pictures.filter(game_id=game)

        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """

        game = Game.objects.get(pk=request.data['gameId'])
        # Create a new instance of the game picture model you defined
        # Example: game_picture = GamePicture()
        picture = Picture()
        picture.base64 = request.data['file']

        format, imgstr = request.data["file"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(
            imgstr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')

        picture.file = data
        picture.game = game

        # Save the data to the database with the save() method
        picture.save()

        serializer = PictureSerializer(picture)
        return Response(serializer.data)


class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer for picture types
    """
    class Meta:
        model = Picture
        depth = 1
        fields = "__all__"
