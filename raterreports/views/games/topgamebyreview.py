"""Module for genereview games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class TopGameByReviewList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            SELECT id, title, MAX(review_total) highest_review_total FROM(
                SELECT g.id, g.title, COUNT(r.id) review_total
                FROM raterapi_game g 
                JOIN raterapi_review r ON g.id = r.game_id
                GROUP BY g.id
            )
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
            #     "highest_review_total"
            #   },
            # ]

            top_game_by_reviews = []

            for row in dataset:
                top_game_by_reviews.append({
                    "id": row["id"],
                    "title": row["title"],
                    "highest_review_total": row["highest_review_total"],
                })
                

        # The template string must match the file name of the html template
        template = 'games/most_reviewed_game.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "most_reviewed": top_game_by_reviews
        }

        return render(request, template, context)
