from django_filters.rest_framework import FilterSet, CharFilter

from todos.models import Task


class TaskFilter(FilterSet):
    """
    A filterset class for filtering and ordering Task records
    """

    created_by = CharFilter(method='filter_with_created_by')
    tags = CharFilter(method='filter_with_tags')
    ordering = CharFilter(method='ordering_by_params')

    def filter_with_created_by(self, queryset, name, value):
        print("this method is called", name, value)
        created_by_ids = value.split(',')
        return queryset.filter(
            created_by__id__in=created_by_ids
        )

    def filter_with_tags(self, queryset, name, value):
        print("this method is called", name, value)
        tag_uuids = value.split(',')
        return queryset.filter(
            tags__uuid__in=tag_uuids
        )

    def ordering_by_params(self, queryset, name, value):
        print("this method is called", name, value)
        if value:
            ordering_list = value.split(',')
        else:
            ordering_list = ['id']
        return queryset.order_by(*ordering_list)

    class Meta:
        model = Task
        fields = [
            'created_by',
            'tags',
            "ordering"
        ]
