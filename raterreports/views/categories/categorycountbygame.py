"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class CategoryCountList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get the count of games in each category
            db_cursor.execute("""
            SELECT
                c.id,
                c.label,
                COUNT(gc.id) game_count
            FROM raterapi_category c
            LEFT JOIN raterapi_gamecategory gc ON gc.category_id = c.id
            GROUP BY c.label
            ORDER BY game_count DESC
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
            #     "label",
            #     "game_count"
            #   },
            # ]

            category_count_by_game = []

            for row in dataset:
                category_count_by_game.append({
                    "id": row["id"],
                    "label": row["label"],
                    "game_count": row["game_count"],
                })
                

        # The template string must match the file name of the html template
        template = 'categories/list_with_category_count_by_game.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "categorycount_list": category_count_by_game
        }

        return render(request, template, context)