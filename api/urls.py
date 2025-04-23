from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet, CastViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'cast', CastViewSet)

urlpatterns = [
    path('', include(router.urls)),
]