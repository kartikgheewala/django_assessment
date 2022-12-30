from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movie_cast.serializers import *


# Create your views here.
class MovieCreateView(APIView):
    """
    :param: title, runtime, language, tagline
    :return: movie object
    function : create the movie
    """
    def post(self, request):
        serializer = MovieCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            qry_message = {
                "status": True,
                "message": "Movie created successfully.",
                "data": serializer.data
            }
            return Response(qry_message, status=status.HTTP_200_OK)

        else:
            if 'title' in serializer.errors:
                message = "title field is required!"
            elif 'runtime' in serializer.errors:
                message = "runtime field is required!"
            elif 'language' in serializer.errors:
                message = "language field is required!"
            elif 'tagline' in serializer.errors:
                message = "tagline field is required!"
            else:
                message = "Some unknown error is occur!"

            qry_message = {
                "status": False,
                "message": message,
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(APIView):
    """
    :param: id, title, runtime, language, tagline, created_at, updated_at
    :return: object
    function : all movies objects in list.
    """

    def get(self, request, format=None):
        qry_region = Movie.objects.all()
        serializer = MovieListSerializer(qry_region, many=True)

        qry_message = {
            "status": True,
            "message": "Movies found!",
            "data": serializer.data
        }
        return Response(qry_message, status=status.HTTP_200_OK)


class MovieDetailsView(APIView):
    """
    :param: id
    :return: object
    function : get particular movies with their cast list of objects
    """

    def get(self, request, id, format=None):
        try:
            qry_movie = Movie.objects.get(id=id)

        except Movie.DoesNotExist:
            qry_message = {
                "status": False,
                "message": "Movies doesn't exist.",
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_404_NOT_FOUND)

        qry_cast = Cast.objects.filter(
            movie=qry_movie.id
        ).values(
            "id", "name", "gender", "publish_date"
        )

        qry_message = {
            "status": True,
            "message": "Movies details found!",
            "data": {
                "id": qry_movie.id,
                "title": qry_movie.title,
                "runtime": qry_movie.runtime,
                "language": qry_movie.language,
                "tagline": qry_movie.tagline,
                "cast": qry_cast,
                "created_at": qry_movie.created_at,
                "updated_at": qry_movie.updated_at,
            }
        }
        return Response(qry_message, status=status.HTTP_200_OK)


class CastCreateView(APIView):
    """
    :param: title, runtime, language, tagline
    :return: movie object
    function : create the cast based in movie object
    """
    def post(self, request):
        serializer = CastCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            qry_message = {
                "status": True,
                "message": "Cast created successfully.",
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_200_OK)

        else:
            if 'title' in serializer.errors:
                message = "title field is required."
            elif 'gender' in serializer.errors:
                message = "gender is not a valid choice."
            elif 'publish_date' in serializer.errors:
                message = "Use one of these formats instead: YYYY-MM-DD."
            elif 'movie' in serializer.errors:
                if serializer.errors['movie'] == ["This field may not be null."]:
                    message = "movie field is required."
                else:
                    message = "movie object not found."
            else:
                message = "Some unknown error is occur!"

            qry_message = {
                "status": False,
                "message": message,
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_400_BAD_REQUEST)
