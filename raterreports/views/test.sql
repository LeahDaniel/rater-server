-- What is the most-reviewed game?

SELECT title, MAX(review_total) highest_review_total FROM(
    SELECT g.title, COUNT(r.id) review_total
    FROM raterapi_game g 
    JOIN raterapi_review r ON g.id = r.game_id
    GROUP BY g.id
)

-- Who is the player with the most games added to the collection?

SELECT user_name, MAX(game_total) highest_game_total FROM(
    SELECT u.first_name || " " || u.last_name user_name, COUNT(g.id) game_total
    FROM auth_user u
    JOIN raterapi_game g ON g.user_id = u.id
    GROUP BY u.id
)

-- What are the games of any category suitable for children under 8?

SELECT c.label, g.title, g.min_age_recommended
FROM raterapi_game g 
JOIN raterapi_gamecategory gc ON gc.game_id = g.id
JOIN raterapi_category c ON c.id = gc.category_id
WHERE g.min_age_recommended < 8


-- How many games don't have pictures?

SELECT * FROM (
    SELECT g.title, COUNT(p.id) total_pictures
    FROM raterapi_game g 
    LEFT JOIN raterapi_picture p ON p.game_id = g.id
    GROUP BY g.id
) WHERE total_pictures = 0

-- By count, who are the top three game reviewers?

SELECT u.first_name || " " || u.last_name user_name, COUNT(r.id) total_reviews_written 
FROM raterapi_review r 
JOIN auth_user u ON u.id = r.user_id
GROUP BY u.id
ORDER BY total_reviews_written DESC
LIMIT 3