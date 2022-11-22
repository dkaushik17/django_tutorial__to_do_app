from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from core.db_utils import get_object_or_404
from todos.models import Tag, Task
from todos.serializers import (
    TagSerializer,
    TagRetrieveSerializer,
    TaskCreateUpdateSerializer,
    TaskSerializer
)
from todos.pagination import TaskPagination
from todos.api.v2.filters import TaskFilter


# |================================= Tag APIs =============================| #
class TagListCreateView(GenericAPIView):
    serializer_class = TagSerializer
    list_message = "List of tag records"
    post_message = "New tag recrod created"

    def get_queryset(self, request, *args, **kwargs):
        queryset = Tag.objects.all()
        return queryset

    # |------------------------ Tag List API ----------------------------| #
    def get(self, request, *args, **kwargs):
        # list all the tags present in the database

        # fetch records from the database
        queryset = self.get_queryset(request, *args, **kwargs)

        # Creating Serializer instance for serialization from
        # Model instanaces to a list of dicts which will be sent in
        # the response
        serialized_data = self.serializer_class(
            instance=queryset,
            many=True,
            context={
                "request": request
            }
        ).data

        # return a Response instance with the data and status code
        return Response(
            data={
                "message": self.list_message,
                "tags": serialized_data
            }
        )

    # |------------------------ Tag Create API ----------------------------| #
    def post(self, request, *args, **kwargs):
        # creates a new tag in the database

        # Creating Serializer instance for de-serialization from
        # data extracted from the request to a python dict
        # representing the validated_data
        serializer_instance = self.serializer_class(
            data=request.data,
            context={
                "request": request
            }
        )

        # Validate the data coming in the request
        serializer_instance.is_valid(raise_exception=True)

        # Create the new model record in the database
        model_instance = serializer_instance.create(
            validated_data=serializer_instance.validated_data
        )

        # Creating Serializer instance for serialization from
        # Model instanace to a dict which will be sent in the response
        serialized_data = self.serializer_class(
            instance=model_instance,
            context={
                "request": request
            }
        ).data

        # Return the Response instance
        return Response(
            data={
                "message": self.post_message,
                "tag": serialized_data
            },
            status=status.HTTP_201_CREATED
        )


class TagUpdateRetrieveDeleteView(GenericAPIView):
    retrieve_message = "Details of tag records"
    update_message = "New tag recrod created"
    delete_message = "Tag recrod deleted"

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagRetrieveSerializer
        else:
            return TagSerializer

    def get_object(self, *args, **kwargs):
        tag = get_object_or_404(
            klass=Tag,
            uuid=kwargs.get("uuid")
        )
        return tag

    # |----------------------- Tag Retrieve API ---------------------------| #
    def get(self, request, *args, **kwargs):
        model_instance = self.get_object(*args, **kwargs)

        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(
            instance=model_instance
        ).data

        return Response(
            data={
                "message": self.retrieve_message,
                "data": serialized_data
            },
        )

    # |------------------------ Tag Update API ----------------------------| #
    def patch(self, request, *args, **kwargs):
        model_instance = self.get_object(*args, **kwargs)

        serializer_class = self.get_serializer_class()
        serializer_instance = serializer_class(
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        serializer_instance.is_valid(raise_exception=True)
        model_instance = serializer_instance.update(
            validated_data=serializer_instance.validated_data,
            instance=model_instance
        )

        serialized_data = serializer_class(model_instance).data

        return Response(
            data={
                "message": self.update_message,
                "data": serialized_data
            },
        )

    # |------------------------ Tag Delete API ----------------------------| #
    def delete(self, request, *args, **kwargs):
        model_instance = self.get_object(*args, **kwargs)

        model_instance.delete()

        return Response(
            data={
                "message": self.delete_message
            },
            status=status.HTTP_204_NO_CONTENT
        )


# |================================= Task APIs ============================| #
class TaskViewset(GenericViewSet):
    filterset_class = TaskFilter
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    paginator = None

    create_message = "New task created"
    update_message = "Task record updated"
    list_message = "List of task records"
    retrieve_message = "Details of task record"
    delete_message = "Task record deleted"

    def get_object(self, *args, **kwargs):
        task = get_object_or_404(
            klass=Task,
            uuid=kwargs.get("uuid")
        )
        return task

    def get_queryset(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        return queryset

    def filter_queryset(self, request, queryset):
        filterset = self.filterset_class(
            data=request.GET,
            queryset=queryset
        )
        filtered_qs = filterset.qs
        return filtered_qs

    def paginate_queryset(self, request, queryset):
        self.paginator = self.pagination_class()
        paginated_qs = self.paginator.paginate_queryset(
            queryset=queryset,
            request=request
        )
        return paginated_qs

    def get_paginated_response(self, data, message):
        return self.paginator.get_paginated_response(data, message)

    def get_serializer_class(self):
        if self.action in ["create_task", "update_task"]:
            return TaskCreateUpdateSerializer
        if self.action in ["list_tasks", "retrieve_task", "delete_task"]:
            return TaskSerializer

    # |------------------------- Task List API ----------------------------| #
    def list_tasks(self, request, *args, ** kwargs):

        model_instances = self.get_queryset(request, *args, ** kwargs)
        filtered_queryset = self.filter_queryset(request, model_instances)
        paginated_queryset = self.paginate_queryset(request, filtered_queryset)

        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(
            instance=paginated_queryset,
            many=True
        ).data

        paginated_response = self.get_paginated_response(
            message=self.list_message,
            data=serialized_data,
        )

        # return the Response instance
        return paginated_response

    # |------------------------- Task Create API --------------------------| #
    def create_task(self, request, *args, ** kwargs):

        serializer_class = self.get_serializer_class()

        serializer_instance = serializer_class(
            data=request.data,
            context={'request': request}
        )

        serializer_instance.is_valid(raise_exception=True)

        model_instance = serializer_instance.create(
            validated_data=serializer_instance.validated_data
        )

        serialized_data = self.serializer_class(instance=model_instance).data

        return Response(
            data={
                "message": self.create_message,
                "data": serialized_data
            },
            status=status.HTTP_201_CREATED
        )

    # |----------------------- Task Update API ---------------------------| #
    def update_task(self, request, *args, ** kwargs):

        model_instance = self.get_object(*args, ** kwargs)

        serializer_class = self.get_serializer_class()

        serializer_instance = serializer_class(
            data=request.data,
            partial=True
        )

        serializer_instance.is_valid(raise_exception=True)

        model_instance = serializer_instance.update(
            validated_data=serializer_instance.validated_data,
            instance=model_instance
        )

        serialized_data = self.serializer_class(
            model_instance
        ).data

        return Response(
            data={
                "message": self.update_message,
                "data": serialized_data
            },
        )

    # |----------------------- Task Retrieve API --------------------------| #
    def retrieve_task(self, request, *args, ** kwargs):

        model_instance = self.get_object(*args, ** kwargs)

        serializer_class = self.get_serializer_class()

        serialized_data = serializer_class(instance=model_instance).data

        return Response(
            data={
                "message": self.retrieve_message,
                "data": serialized_data
            },
        )

    # |----------------------- Task Delete API ---------------------------| #
    def delete_task(self, request, *args, ** kwargs):

        model_instance = self.get_object(*args, ** kwargs)

        model_instance.delete()

        return Response(
            data={
                "message": self.delete_message
            },
            status=status.HTTP_202_ACCEPTED
        )
