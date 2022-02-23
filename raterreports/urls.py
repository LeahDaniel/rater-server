from django.urls import path

from .views import TopGamesByRatingList, BottomGamesByRatingList, CategoryCountList, GamesByPlayersList

urlpatterns = [
    path('reports/topgames', TopGamesByRatingList.as_view()),
    path('reports/bottomgames', BottomGamesByRatingList.as_view()),
    path('reports/categorycount', CategoryCountList.as_view()),
    path('reports/groupgames', GamesByPlayersList.as_view()),
]