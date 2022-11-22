from django.urls import path

from todos.api.v2.views import (
    tag_list_create,
    tag_retrieve_update_delete,
    task_list_create,
    task_retrieve_update_delete,
)

app_name = "todos"

urlpatterns = [

    # |=============================== Tag APIs ===========================| #
    path(
        route="tags/",
        view=tag_list_create,
        name="tag_create_list_v2"
    ),
    path(
        route="tags/<slug:uuid>",
        view=tag_retrieve_update_delete,
        name="tag_retrieve_update_delete_v2"
    ),

    # |============================== Task APIs ===========================| #
    path(
        route="tasks/",
        view=task_list_create,
        name="tags_create_list_v2"
    ),
    path(
        route="tasks/<slug:uuid>",
        view=task_retrieve_update_delete,
        name="task_retrieve_update_delete_v2"
    ),

]
