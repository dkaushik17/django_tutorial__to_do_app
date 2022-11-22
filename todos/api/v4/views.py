
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from core.db_utils import get_object_or_404
from core.renderers import CustomRenderer
from todos.api.v2.filters import TaskFilter
from todos.models import Tag, Task
from todos.pagination import TaskPagination
from todos.serializers import (
    TagRetrieveSerializer, TagSerializer,
    TaskCreateUpdateSerializer, TaskSerializer
)
from rest_framework.permissions import IsAuthenticated


# |================================= Tag APIs ============================| #
class TagViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    # Authentication
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    renderer_classes = [CustomRenderer]

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of tag records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested tag record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested tag record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested tag record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New Tag record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        tag = get_object_or_404(
            klass=Tag,
            uuid=self.kwargs.get("uuid")
        )
        return tag

    def get_queryset(self, *args, **kwargs):
        queryset = Tag.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TagRetrieveSerializer
        else:
            return TagSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if self.action in self.response_data:
            context["message"] = (
                self.response_data.get(self.action).get("message")
            )
            context["status_code"] = (
                self.response_data.get(self.action).get("status_code")
            )
        return context


# |================================= Task APIs ============================| #
class TaskViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    pagination_class = TaskPagination
    renderer_classes = [CustomRenderer]

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of task records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested task record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested task record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested task record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New Task record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        task = get_object_or_404(
            klass=Task,
            uuid=self.kwargs.get("uuid")
        )
        return task

    def get_queryset(self, *args, **kwargs):
        queryset = Task.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TaskCreateUpdateSerializer
        else:
            return TaskSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if self.action in self.response_data:
            context["message"] = (
                self.response_data.get(self.action).get("message")
            )
            context["status_code"] = (
                self.response_data.get(self.action).get("status_code")
            )
        return context
