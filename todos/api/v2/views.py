# django imports
from django.views.decorators.csrf import csrf_exempt

# rest_framework imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# local imports
from core.db_utils import get_object_or_404
from todos.api.v2.filters import TaskFilter
from todos.serializers import (
    TagRetrieveSerializer,
    TagSerializer,
    TaskCreateUpdateSerializer,
    TaskSerializer
)
from todos.models import Tag, Task
from todos.pagination import TaskPagination


# ===================================Tag APIs ============================== #

@csrf_exempt
@api_view(['GET', 'POST'])
def tag_list_create(request):
    """
    This view lists all tags and a create a new tag
    """

    # |------------------------- Tag List API ----------------------------| #
    if request.method == "GET":
        # list all the tags present in the database

        # fetch tags from the database
        tags = Tag.objects.all()

        # Creating Serializer instance for serialization from
        # Model instanaces to a list of dicts which will be sent in
        # the response
        serialized_data = TagSerializer(
            instance=tags,
            many=True,
            context={
                "request": request
            }
        ).data

        # return a Response instance with the data and status code
        return Response(
            data={
                "message": "List of tag records",
                "data": serialized_data
            }
        )

    # |------------------------- Tag Create API ----------------------------| #
    if request.method == "POST":
        # creates a new tag in the database

        # Creating Serializer instance for de-serialization from
        # data extracted from the request to a python dict
        # representing the validated_data
        tag_serializer = TagSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        # Validate the data coming in the request
        tag_serializer.is_valid(raise_exception=True)

        # Create the new tag record in the database
        tag = tag_serializer.create(
            validated_data=tag_serializer.validated_data
        )

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = TagSerializer(
            instance=tag,
            context={
                "request": request
            }
        ).data

        # Return the Response instance
        return Response(
            data={
                "message": "New tag record created",
                "data": serialized_data
            },
            status=status.HTTP_201_CREATED
        )


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def tag_retrieve_update_delete(request, uuid):
    """
    This view returns the details, updates the fields or deletes the
    selected tag record.
    The selected tag record is uniquely identified by the uuid coming in
    as the URI param in the request.
    """

    # |----------------------- Tag Retrieve API --------------------------| #
    if request.method == "GET":
        # Returns the details of the selected tag

        # fetch the requested tag from the database
        tag = get_object_or_404(
            klass=Tag,
            uuid=uuid
        )

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = TagRetrieveSerializer(
            instance=tag,
            context={
                "request": request
            }
        ).data

        # Return the Response instance
        return Response(
            data={
                "message": "Tag details",
                "data": serialized_data
            },
        )

    # |------------------------ Tag Update API ---------------------------| #
    if request.method == "PATCH":
        # updates the selected tag record

        # fetch the requested tag from the database
        tag = get_object_or_404(
            klass=Tag,
            uuid=uuid
        )

        # Creating Serializer instance for de-serialization from
        # data extracted from the request to a python dict
        # representing the validated_data
        tag_serializer = TagSerializer(
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        # Validate the data coming in the request
        tag_serializer.is_valid(raise_exception=True)

        tag = tag_serializer.update(
            validated_data=tag_serializer.validated_data,
            instance=tag
        )

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = TagSerializer(
            instance=tag,
            context={
                "request": request
            }
        ).data

        # Return the Response instance
        return Response(
            data={
                "message": "Selected tag is updated",
                "data": serialized_data
            },
        )

    # |------------------------- Tag Delete API ----------------------------| #
    if request.method == "DELETE":
        # deletes the requested tag from the database

        # fetch the requested tag from the database
        tag = get_object_or_404(
            klass=Tag,
            uuid=uuid
        )

        # Delete the tag record
        tag.delete()

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = TagSerializer(
            instance=tag,
            context={
                "request": request
            }
        ).data

        return Response(
            data={
                "message": "Tag record deleted",
                "data": serialized_data
            },
            status=status.HTTP_200_OK
        )


# ===================================Task APIs ============================= #


@csrf_exempt
@api_view(['GET', 'POST'])
def task_list_create(request):
    """
    This view lists all tags and a create a new tag
    """

    # |------------------------- Task List API ----------------------------| #
    if request.method == "GET":
        # returns a list of all the tags present in the database

        # Filtering based on the query_params sent in the request
        filterset = TaskFilter(
            data=request.GET,
            queryset=Task.objects.all()
        )
        filtered_qs = filterset.qs

        # Pagination through a simple implementation of page number pagination
        paginator = TaskPagination()
        paginated_qs = paginator.paginate_queryset(
            queryset=filtered_qs,
            request=request
        )

        # # Ordering
        # ordering_list = request.query_params.getlist('ordering')
        # if not ordering_list:
        #     ordering_list = ['id']

        # preparing a list of dicts that need to be sent in the response
        serialized_data = TaskSerializer(
            instance=paginated_qs,
            many=True
        ).data

        # Prepare a dict to be sent in the response
        paginated_response = paginator.get_paginated_response(
            message="List of task records.",
            data=serialized_data,
        )

        # return the Response instance
        return paginated_response

    # |------------------------- Task Create API --------------------------| #
    if request.method == "POST":
        # creates a new tag in the database

        # validate the data coming in the request
        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        task_serializer = TaskCreateUpdateSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        # Create a new task record in the database
        task = task_serializer.create(
            validated_data=task_serializer.validated_data,
        )

        # prepare dict for response
        serialized_data = TaskSerializer(
            instance=task
        ).data

        return Response(
            data={
                "message": "New task record created",
                "data": serialized_data
            },
        )


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def task_retrieve_update_delete(request, uuid):
    """
    This view lists all tags and a create a new tag
    """
    # |----------------------- Task Retrieve API --------------------------| #
    if request.method == "GET":
        # fetch the requested tag from the database
        task = get_object_or_404(
            klass=Task,
            uuid=uuid
        )

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = TaskSerializer(
            instance=task,
            context={
                "request": request
            }
        ).data

        # return the Response instace
        return Response(
            data={
                "message": "Task details",
                "data": serialized_data
            },
            status=status.HTTP_200_OK
        )

    # |----------------------- Task Retrieve API --------------------------| #
    if request.method == "PATCH":
        # fetch the requested tag from the database
        task = get_object_or_404(
            klass=Task,
            uuid=uuid
        )

        task_serializer = TaskCreateUpdateSerializer(
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        task_serializer.is_valid(raise_exception=True)

        task = task_serializer.update(
            validated_data=task_serializer.validated_data,
            instance=task
        )

        serialized_data = TaskSerializer(
            instance=task
        ).data

        return Response(
            data={
                "message": "Selected task is updated",
                "data": serialized_data
            },
        )

    # |----------------------- Task Delete API ---------------------------| #
    if request.method == "DELETE":
        # fetch the requested tag from the database
        task = get_object_or_404(
            klass=Task,
            uuid=uuid
        )

        task.delete()

        return Response(
            data={
                "message": "Selected task record is deleted",
            },
            status=status.HTTP_202_ACCEPTED
        )
