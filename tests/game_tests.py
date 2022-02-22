from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Game
from raterapi.models.category import Category


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new User, collect the auth Token
        """

        # Define the URL path for registering a User
        url = '/register'

        # Define the User properties
        user = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, user, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED THE DATABASE WITH A GAMETYPE
        # This is necessary because the API does not
        # expose a /gametypes URL path for creating GameTypes

        self.category = Category()
        self.category.label = "Strategy"

        self.category.save()

        # Create a new instance of Game
        self.game = Game()
        self.game.user_id = self.token.user_id
        self.game.title = "Sorry"
        self.game.designer = "Milton Bradley"
        self.game.description = "Is it too late now to say sorry?"
        self.game.year_released = 1942
        self.game.number_of_players = 4
        self.game.hours_playtime = 1
        self.game.min_age_recommended = 8

        # Save the Game to the testing database
        self.game.save()
        self.game.categories.add(self.category.id)

    def test_create_game(self):
        """
        Ensure we can create (POST) a new Game.
        """

        # Define the URL path for creating a new Game
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Sorry",
            "designer": "Milton Bradley",
            "description": "Is it too late now to say sorry?",
            "yearReleased": 1942,
            "numberOfPlayers": 4,
            "hoursPlaytime": 1,
            "minAgeRecommended": 8,
            "categoryId": self.category.id
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, game, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        # self.assertEqual(response.data["user"]['user'], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["designer"], game['designer'])
        self.assertEqual(response.data["description"], game['description'])
        self.assertEqual(response.data["year_released"], game['yearReleased'])
        self.assertEqual(
            response.data["number_of_players"], game['numberOfPlayers'])
        self.assertEqual(
            response.data["hours_playtime"], game['hoursPlaytime'])
        self.assertEqual(
            response.data["min_age_recommended"], game['minAgeRecommended'])
        self.assertIsNotNone(response.data["categories"])

    def test_get_game(self):
        """
        Ensure we can GET an existing game.
        """

        # Define the URL path for getting a single Game
        url = f'/games/{self.game.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url, format='json')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["title"], self.game.title)
        self.assertEqual(response.data["designer"], self.game.designer)
        self.assertEqual(response.data["description"], self.game.description)
        self.assertEqual(
            response.data["year_released"], self.game.year_released)
        self.assertEqual(
            response.data["number_of_players"], self.game.number_of_players)
        self.assertEqual(
            response.data["hours_playtime"], self.game.hours_playtime)
        self.assertEqual(
            response.data["min_age_recommended"], self.game.min_age_recommended)
        self.assertIsNotNone(response.data["categories"])
        
    def test_get_games(self):
        """
        Ensure we can GET all games
        """
        url = f'/games'
        # Initiate GET request and capture the response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1 )

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """

        # Define the URL path for updating an existing Game
        url = f'/games/{self.game.id}'

        # Define NEW Game properties
        new_game = {
            "title": "Sorry",
            "designer": "Milton Bradley",
            "description": "Sorry not sorry",
            "yearReleased": 2023,
            "numberOfPlayers": 4,
            "hoursPlaytime": 1,
            "minAgeRecommended": 27,
            "categoryId": self.category.id
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["title"], new_game["title"])
        self.assertEqual(response.data["designer"], new_game["designer"])
        self.assertEqual(response.data["description"], new_game["description"])

        self.assertEqual(
            response.data["year_released"], new_game["yearReleased"])
        self.assertEqual(
            response.data["number_of_players"], new_game["numberOfPlayers"])
        self.assertEqual(
            response.data["hours_playtime"], new_game["hoursPlaytime"])
        self.assertEqual(
            response.data["min_age_recommended"], new_game["minAgeRecommended"])
        self.assertIsNotNone(response.data["categories"])
