from django.contrib import admin
from todos.models import Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'task_count')
    search_fields = ("name__startswith", )

    class Meta:
        ordering = ('name')
 
    def task_count(self, obj):
        return obj.tasks.count()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'tag_names')
    search_fields = ("title__startswith", )

    def tag_names(self, obj):
        return ", ".join(
            [tag.name for tag in obj.tags.all()]
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags')

    class Meta:
        ordering = ('title')
