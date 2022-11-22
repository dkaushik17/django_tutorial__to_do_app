from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.serializers import (
    ValidationError,
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    PrimaryKeyRelatedField,
    SlugRelatedField,
)
from todos.models import Tag, Task


class TagSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization &
    de-serialization for Tag model recrods.
    """

    def validate_name(self, name):
        print("validate_name method of TagSerializer is called!")
        print(self.context)
        if len(name.split(' ')) > 1:
            print("spaces found")
            raise ValidationError(
                detail="The name should not contain any spaces",
            )
        return name

    class Meta:
        model = Tag
        exclude = ['id']


class TagRetrieveSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization &
    de-serialization for Tag model recrods.
    """

    tasks = SerializerMethodField()

    def get_tasks(self, tag):
        """
        This field in the response represent the task counts grouped by
        completion_status for this tag
        """
        task_count_grouped_by_completion_status = (
            tag
            .tasks
            .values('completion_status')
            .annotate(
                task_count=Count('completion_status'),
            )
            .values(
                'task_count',
                'completion_status'
            )
        )
        return task_count_grouped_by_completion_status

    class Meta:
        model = Tag
        exclude = ['id']


class TaskCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the Task model records.
    """
    created_by = PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    tags = SlugRelatedField(
        slug_field="uuid",
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Task
        exclude = ['id', 'created_date', 'modified_date']


class TaskSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the Task model records.
    """
    tags = TagSerializer(many=True)
    completion_status = SerializerMethodField()
    created_date = DateTimeField(format="%-d %B %Y, %A, %-I:%-M %p")
    modified_date = DateTimeField(format="%m/%d/%Y-%H:%M:%S")
    created_by = SerializerMethodField()

    def get_completion_status(self, object):
        return Task.CompletionStatus[object.completion_status].label

    def get_created_by(self, object):
        return {
            "id": object.created_by.id,
            "name": (
                f"{object.created_by.first_name} {object.created_by.last_name}"
            )
        }

    class Meta:
        model = Task
        # exclude = ['id']
        # If we want to determine the order of the fields in the response
        # we have to set the fields attribute instead of using exclude
        fields = (
            "title",
            "text",
            "uuid",
            "completion_status",
            "created_by",
            "created_date",
            "modified_date",
            "tags"
        )
