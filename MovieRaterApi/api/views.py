from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Movie,Rating
from .serializers import MovieSerializers,RatingSerializers,UserSerializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    @action(detail=True,methods=['POST'])#It defines to what URL will the browser POST or GET (depending on the method) the filled form.
    def rate_movie(self,request,pk=None):
        if 'stars' in request.data:
            movie=Movie.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user #token is connected to this user
            print('User:  ',user)
            try:
                rating=Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars=stars
                rating.save()
                serializer=RatingSerializers(rating,many=False)
                response = {'massege': 'Rating updated','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user, movie=movie,stars=stars)
                serializer = RatingSerializers(rating, many=False)
                response = {'massege': 'Rating created','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'massege': 'you need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'massege': 'You cant update rating like that '}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'massege': 'You cant create rating like that '}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


