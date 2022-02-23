from django.urls import path

from .views import TopGamesByRatingList, BottomGamesByRatingList, CategoryCountList

urlpatterns = [
    path('reports/topgames', TopGamesByRatingList.as_view()),
    path('reports/bottomgames', BottomGamesByRatingList.as_view()),
    path('reports/categorycount', CategoryCountList.as_view()),
]