from rest_framework.exceptions import NotFound


def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = (
            klass.__name__
            if isinstance(klass, type)
            else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        # raise Http404(
        #   'No %s matches the given query.' % queryset.model._meta.object_name
        # )
        raise NotFound(
            detail={
                "message": (
                  f"No {queryset.model._meta.object_name} "
                  f"matches the given query."
                )
            }
        )


def get_list_or_404(klass, *args, **kwargs):
    """
    Use filter() to return a list of objects, or raise an Http404 exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'filter'):
        klass__name = (
            klass.__name__
            if isinstance(klass, type)
            else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_list_or_404() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        # raise Http404(
        #   'No %s matches the given query.' % queryset.model._meta.object_name
        # )
        raise NotFound(
            detail={
                "message": (
                  f"No {queryset.model._meta.object_name} "
                  f"matches the given query."
                )
            }
        )
    return obj_list
