SELECT
    c.id,
    c.label,
    COUNT(gc.id) game_count
FROM raterapi_category c
LEFT JOIN raterapi_gamecategory gc ON gc.category_id = c.id
GROUP BY c.label
ORDER BY game_count DESC