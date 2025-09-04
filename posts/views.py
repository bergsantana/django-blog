"""API controllers - translate HTTP requests to use-cases and DTOs."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreatePostSerializer, UpdatePostSerializer
from . import services
from .repositories.external import ExternalAPIError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PostListCreateView(APIView):
    """GET -> list posts (proxy to external GET)
       POST -> create a post (proxy to external POST)
    I used APIView to be explicit and add clear comments; for larger projects ViewSets can be used.
    """
    @swagger_auto_schema(
        operation_description="List all blog posts (proxy to external API).",
        responses={
            200: openapi.Response(
                description="Successful list",
                examples={
                    "application/json": {
                        "count": 1,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "username": "john",
                                "title": "Hello World",
                                "content": "This is my first post",
                                "created_datetime": "2025-09-03T12:00:00Z",
                            }
                        ],
                    }
                },
            )
        },
    )
    def get(self, request):
        # forward query params to external API for listing and return the response as-is.
        try:
            data = services.list_posts(params=request.query_params)
        except ExternalAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(data)

    @swagger_auto_schema(
        request_body=CreatePostSerializer,
        responses={
            201: openapi.Response(
                description="Post successfully created",
                examples={
                    "application/json": {
                        "id": 2,
                        "username": "alice",
                        "title": "My Post",
                        "content": "Post content",
                        "created_datetime": "2025-09-03T12:05:00Z",
                    }
                },
            )
        },
    )
    def post(self, request):
        # Validate input using serializer (DTO). This ensures we only send expected fields to external API.
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            created = services.create_post(serializer.validated_data)
        except ExternalAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(created, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    """Handles retrieve/update/delete for a single post identified by id."""
    @swagger_auto_schema(
        request_body=UpdatePostSerializer,
        responses={
            200: openapi.Response(
                description="Post successfully updated",
                examples={
                    "application/json": {
                        "id": 5,
                        "username": "bob",
                        "title": "Updated Title",
                        "content": "Updated Content",
                        "created_datetime": "2025-09-03T12:10:00Z",
                    }
                },
            )
        },
    )
    def patch(self, request, pk):
        serializer = UpdatePostSerializer(data=request.data, partial=True)
        print(f"{serializer} - {serializer.get_fields()} -{ request}")
        serializer.is_valid(raise_exception=True)
        try:
            updated = services.update_post(pk, serializer.validated_data)
        except ExternalAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(updated, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                description="Post successfully deleted",
                examples={"application/json": {}},
            )
        }
    )
    def delete(self, request, pk):
        try:
            result = services.delete_post(pk)
        except ExternalAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(result, status=status.HTTP_204_NO_CONTENT)