from django.urls import path

from todos.api.v4.views import (
    TagViewset,
    TaskViewset
)

app_name = "todos"

urlpatterns = [

    # |=============================== Tag APIs ===========================| #
    path(
        route="tags/",
        view=TagViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="tag_create_list_v4"
    ),
    path(
        route="tags/<slug:uuid>",
        view=TagViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="tag_retrieve_update_delete_v4"
    ),

    # |============================== Task APIs ===========================| #
    path(
        route="tasks/",
        view=TaskViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="task_list_create_v3"
    ),
    path(
        route="tasks/<slug:uuid>",
        view=TaskViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="task_retrieve_update_delete_v4"
    ),

]
