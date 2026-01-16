from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Movie, Review, Favorite
from .serializers import MovieSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["get", "post"], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        movie = self.get_object()

        if request.method == "GET":
            qs = movie.reviews.select_related("user")
            return Response(ReviewSerializer(qs, many=True).data)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        movie = self.get_object()

        if request.method == "POST":
            Favorite.objects.get_or_create(
                user=request.user,
                movie=movie,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)

        Favorite.objects.filter(user=request.user, movie=movie).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        qs = Movie.objects.filter(favorites__user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
