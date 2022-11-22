from django.contrib.auth.models import User
from django.db import models

from core.behaviours import UUIDMixin


class Tag(UUIDMixin):
    """
    This model represents a tag.
    Multiple tags can be associated with a task.
    """
    # The name of the tag
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "tags"
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class Task(UUIDMixin):
    """
    This model represents a task.
    """
    # The title of the task
    title = models.CharField(max_length=200)
    # The text of the task which specifies the details of the task
    text = models.TextField()
    # Created date of the task
    created_date = models.DateTimeField(
        verbose_name="Task creation datetime",
        auto_now_add=True
    )
    # Modified date of the task
    modified_date = models.DateTimeField(
        verbose_name="Task last modification datetime",
        auto_now=True
    )
    # The user who created the task
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )

    # Compeletion Status
    class CompletionStatus(models.TextChoices):
        COMPLETED = 'COMPLETED', "Completed"
        INCOMPLETE = 'INCOMPLETE', "Incomplete"

    completion_status = models.CharField(
        max_length=50,
        choices=CompletionStatus.choices,
        default=CompletionStatus.INCOMPLETE
    )

    # Tag
    tags = models.ManyToManyField(
        to=Tag,
        related_name="tasks",
        related_query_name="task"
    )

    class Meta:
        db_table = "task"
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __repr__(self) -> str:
        return self.title

    def __str__(self) -> str:
        return self.title
