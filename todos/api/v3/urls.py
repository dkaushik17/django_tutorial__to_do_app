from django.urls import path

from todos.api.v3.views import (
    TagListCreateView,
    TagUpdateRetrieveDeleteView,
    TaskViewset
)

app_name = "todos"

urlpatterns = [

    # |=============================== Tag APIs ===========================| #
    path(
        route="tags/",
        view=TagListCreateView.as_view(),
        name="tag_create_list_v3"
    ),
    path(
        route="tags/<slug:uuid>",
        view=TagUpdateRetrieveDeleteView.as_view(),
        name="tag_retrieve_update_delete_v3"
    ),

    # |============================== Task APIs ===========================| #
    path(
        route="tasks/",
        view=TaskViewset.as_view({
            "get": "list_tasks",
            "post": "create_task"
        }),
        name="task_list_create_v3"
    ),
    path(
        route="tasks/<slug:uuid>",
        view=TaskViewset.as_view({
            "get": "retrieve_task",
            "patch": "update_task",
            "delete": "delete_task"
        }),
        name="task_retrieve_update_delete_v3"
    ),

]
