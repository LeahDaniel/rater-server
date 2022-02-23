"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class GamesByPlayersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games with their average rating, order them, and limit to 5
            db_cursor.execute("""
            SELECT  
                id,
                title, 
                number_of_players
            FROM raterapi_game
            WHERE number_of_players > 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id",
            #     "title",
            #     "number_of_players"
            #   },
            # ]

            games_by_players = []

            for row in dataset:
                games_by_players.append({
                    "id": row["id"],
                    "title": row["title"],
                    "number_of_players": row["number_of_players"],
                })
                

        # The template string must match the file name of the html template
        template = 'games/list_with_games_by_players.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list_by_players": games_by_players
        }

        return render(request, template, context)