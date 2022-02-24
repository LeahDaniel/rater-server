"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterreports.views.helpers import dict_fetch_all


class CategoryKidGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT c.id, g.id game_id, c.label, g.title, g.min_age_recommended
            FROM raterapi_game g 
            JOIN raterapi_gamecategory gc ON gc.game_id = g.id
            JOIN raterapi_category c ON c.id = gc.category_id
            WHERE g.min_age_recommended < 8
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_category list:
            #
            # [
            #   {
            #     "id": 1,
            #     "label": "",
            #     "games": [
            #       {
            #         "game_id":
            #         "title": "Foo",
            #         "min_age_recommended":
            #       },
            #       {
            #         "game_id":
            #         "title": "Foo",
            #         "min_age_recommended":
            #       }
            #     ]
            #   },
            # ]

            games_by_category = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                game = {
                    "game_id": row["game_id"],
                    "title": row["title"],
                    "min_age_recommended": row["min_age_recommended"]
                }
                
                # This is using a generator comprehension to find the user_dict in the games_by_category list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_category:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                
                user_dict = next(
                    (
                        user_game for user_game in games_by_category
                        if user_game['id'] == row['id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_category list, append the game to the games list
                    user_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_category list, create and add the user to the list
                    games_by_category.append({
                        "id": row['id'],
                        "label": row['label'],
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'categories/list_with_kid_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "kidgame_list": games_by_category
        }

        return render(request, template, context)
