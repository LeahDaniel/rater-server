"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class TopGamesByRatingList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games with their average rating, order them, and limit to 5
            db_cursor.execute("""
            SELECT
                g.id, 
                g.title, 
                AVG(r.rating) average_rating
            FROM raterapi_game g
            JOIN raterapi_rating r ON r.game_id = g.id
            GROUP BY g.title
            ORDER BY average_rating DESC
            LIMIT 5
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
            #     "average_rating"
            #   },
            # ]

            top_games_by_rating = []

            for row in dataset:
                top_games_by_rating.append({
                    "id": row["id"],
                    "title": row["title"],
                    "average_rating": row["average_rating"],
                })
                

        # The template string must match the file name of the html template
        template = 'games/list_with_top_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "topgame_list": top_games_by_rating
        }

        return render(request, template, context)
