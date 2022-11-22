from math import ceil
# django imports
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q, Count
# rest_framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from todos.models import Tag, Task


# ===================================Tag APIs ============================== #

@csrf_exempt
@api_view(['GET', 'POST'])
def tag_list_create(request):
    """
    This view lists all tags and a create a new tag
    """

    if request.method == "GET":
        # list all the tags present in the database

        # fetch tags from the database
        tags = Tag.objects.all()

        # prepare a list of dicts to be sent in the response
        response_data = []
        for tag in tags:
            response_data.append(
                {
                    "name": tag.name,
                    "uuid": tag.uuid
                }
            )

        # return a Response instance with the data and status code
        return Response(
            data={
                "message": "List of tag records",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )

    if request.method == "POST":
        # create a new tag in the database

        # validate the data coming in the request
        try:
            name = request.data['name']
            print(name, len(name.split(' ')))
            if len(name.split(' ')) > 1:
                return Response(
                    data={
                        "message": "Tag names are not allowed to have spaces"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except KeyError as e:
            return Response(
                data={
                    "message": f"{e.split(' ')[1]} is a requried field"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # create a new record in the database
        tag = Tag.objects.create(
            name=name
        )

        # prepare a dict to be sent in the response
        response_data = {
            "name": tag.name,
            "uuid": tag.uuid
        }

        # return an instance of Response with the data and status code
        return Response(
            data={
                "message": "New tag record created",
                "data": response_data,
            },
            status=status.HTTP_201_CREATED
        )


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def tag_retrieve_update_delete(request, uuid):
    """
    This view returns the details, updates the fields or deletes the
    selected tag record.
    The selected tag record is uniquely identified by the uuid coming in
    as the URI param in the request.
    """

    if request.method == "GET":
        # Returns the details of the selected tag

        # fetch the requested tag from the database
        try:
            tag = Tag.objects.get(uuid=uuid)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": "There is no tag record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

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

        # prepare the dict to be sent in the response
        response_data = {
            "name": tag.name,
            "uuid": tag.uuid,
            "tasks": task_count_grouped_by_completion_status
        }

        # return the instance of Response with the data and status code
        return Response(
            data={
                "message": "Tag record",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )

    if request.method == "PATCH":
        # updates the selected tag record

        # fetch the requested tag from the database
        try:
            tag = Tag.objects.get(uuid=uuid)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": "There is no tag record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # validate the values coming in the request
        try:
            name = request.data['name']
            if len(name.split(' ')) > 1:
                return Response(
                    data={
                        "message": "Tag names are not allowed to have spaces"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except KeyError as e:
            return Response(
                data={
                    "message": f"{e.split(' ')[1]} is a requried field"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # update the tag record
        tag.name = name
        tag.save()

        # prepare a dict to be sent in the response
        response_data = {
            "name": tag.name,
            "uuid": tag.uuid
        }

        # return a Resposne instance
        return Response(
            data={
                "message": "Tag record",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )

    if request.method == "DELETE":
        # deletes the requested tag from the database

        # fetch the requested tag from the database
        try:
            tag = Tag.objects.get(uuid=uuid)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": "There is no tag record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the tag record
        tag.delete()

        # prepare a dict to be sent in the response
        response_data = {
            "name": tag.name,
            "uuid": tag.uuid
        }

        return Response(
            data={
                "message": "Tag record deleted",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )


# ===================================Task APIs ============================== #


@csrf_exempt
@api_view(['GET', 'POST'])
def task_list_create(request):
    """
    This view lists all tags and a create a new tag
    """

    if request.method == "GET":
        # returns a list of all the tags present in the database

        # Filtering based on the query_params sent in the request
        print("query_params", request.query_params)
        query = Q()
        # Filtering based on the created_by field
        created_by_ids = request.query_params.get('created_by')
        if created_by_ids:
            created_by_ids = created_by_ids.split(',')
            print("created_by_ids:", created_by_ids)
            query &= Q(created_by__id__in=created_by_ids)
        # Filtering based on related tags
        tag_uuids = request.query_params.get('tag_uuids')
        if tag_uuids:
            tag_uuids = tag_uuids.split(',')
            print("tag_uuids:", tag_uuids)
            query &= Q(tags__uuid__in=tag_uuids)
        print(query)

        # Pagination through a simple implementation of page number pagination
        page_size = 5
        # fetch the total records after the filteration
        total_tasks = Task.objects.all().filter(query).count()
        total_pages = ceil(total_tasks / page_size)
        current_page = int(request.query_params.get('page', 1))
        # calculated the limits for the query to fetch the records from the db
        start_index = (current_page - 1) * (page_size)
        end_index = start_index + page_size - 1
        print("total_tasks:", total_tasks)
        print("total_pages:", total_pages)
        print("current_page:", current_page)
        print("start_index:", start_index)
        print("end_index:", end_index)

        # Ordering
        ordering_list = request.query_params.getlist('ordering')
        if not ordering_list:
            ordering_list = ['id']

        # Fetch the task records from the database
        tasks = (
            Task.objects
            .order_by(*ordering_list)
            .filter(query)
            [start_index:end_index]
        )

        # preparing a list of dicts that need to be sent in the response
        response_data = []
        for task in tasks:
            response_data.append(
                {
                    "title": task.title,
                    "uuid": task.uuid,
                    "created_by": {
                        "email": task.created_by.email,
                        "id": task.created_by.id
                    },
                    "tags": [
                        {
                            "name": tag.name,
                            "uuid": tag.uuid
                        } for tag in task.tags.all()
                    ],
                }
            )

        # return the Response instance
        return Response(
            data={
                "message": "List of task records",
                "data": response_data,
                "page_info": {
                    "result_count": total_tasks,
                    "page_size": page_size,
                    "page_count": total_pages,
                    "page": current_page,
                }
            },
            status=status.HTTP_200_OK
        )

    if request.method == "POST":
        # creates a new tag in the database

        # validate the data coming in the request
        try:
            title = request.data['title']
            text = request.data['text']
            tag_uuid_list = request.data.get('tags')
            if tag_uuid_list:
                tags = Tag.objects.filter(uuid__in=tag_uuid_list)
            created_by_id = request.data['created_by']
            try:
                created_by = User.objects.get(id=created_by_id)
            except User.DoesNotExist:
                return Response(
                    data={
                        "message": (
                            "User id provided in the created_by is not valid"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except KeyError as e:
            return Response(
                data={
                    "message": f"{e.split(' ')[1]} is a requried field"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new task record in the database
        task = Task.objects.create(
            title=title,
            text=text,
            created_by=created_by
        )
        # set the tags associated with the task
        task.tags.set(tags)

        # prepare dict for response
        response_data = {
            "uuid": task.uuid,
            "title": task.title,
            "text": task.text,
            "created_date": task.created_date.strftime("%m/%d/%Y"),
            "modified_date": task.modified_date.strftime("%m/%d/%Y"),
            "created_by": {
                        "email": task.created_by.email,
                        "id": task.created_by.id
            },
            "completion_status": task.get_completion_status_display(),
            "tags": [
                {
                    "name": tag.name,
                    "uuid": tag.uuid,
                } for tag in tags
            ]

        }

        # return the Response instance with the data and status code
        return Response(
            data={
                "message": "New task record created",
                "data": response_data,
            },
            status=status.HTTP_201_CREATED
        )


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def task_retrieve_update_delete(request, uuid):
    """
    This view lists all tags and a create a new tag
    """

    if request.method == "GET":
        # fetch the requested tag from the database
        try:
            task = Task.objects.get(uuid=uuid)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": "There is no task record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        response_data = {
            "uuid": task.uuid,
            "title": task.title,
            "text": task.text,
            "created_date": task.created_date.strftime("%d %B %Y"),
            "modified_date": task.modified_date.strftime("%d %B %Y"),
            "created_by": {
                        "email": task.created_by.email,
                        "id": task.created_by.id
            },
            "completion_status": task.get_completion_status_display(),
            "tags": [
                {
                    "name": tag.name,
                    "uuid": tag.uuid,
                } for tag in task.tags.all()
            ]

        }

        return Response(
            data={
                "message": "Task record",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )

    if request.method == "PATCH":
        # fetch the requested tag from the database
        try:
            task = Task.objects.get(uuid=uuid)
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "There is no tag record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Extract and validate data in the request
        title = request.data.get('title', task.title)
        if len(title) > 200:
            raise ValidationError(
                detail="The maximum length allowed for the title is 200"
            )
        text = request.data.get('text', task.text)
        completion_status = request.data.get(
            'completion_status', task.completion_status
        )
        if completion_status not in Task.CompletionStatus.names:
            raise ValidationError(
                detail="completion_status can be either COMPLETE or INCOMPLETE"
            )
        tag_uuids = request.data.get('tags', task.tags.all())
        tags = (
            Tag.objects.filter(uuid__in=tag_uuids) if tag_uuids
            else task.tags.all()
        )

        # Update the Task record in the database
        task.title = title
        task.text = text
        task.completion_status = completion_status
        task.save()
        task.tags.set(tags)

        # Prepare the dictionary for the response
        response_data = {
            "uuid": task.uuid,
            "title": task.title,
            "text": task.text,
            "created_date": task.created_date.strftime("%d %B %Y"),
            "modified_date": task.modified_date.strftime("%d %B %Y"),
            "created_by": {
                        "email": task.created_by.email,
                        "id": task.created_by.id
            },
            "completion_status": task.get_completion_status_display(),
            "tags": [
                {
                    "name": tag.name,
                    "uuid": tag.uuid,
                } for tag in tags
            ]
        }

        # return the Response instance
        return Response(
            data={
                "message": "Requsted Tag record updated.",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )

    if request.method == "DELETE":
        # fetch the requested tag from the database
        try:
            task = Task.objects.get(uuid=uuid)
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "There is no tag record with the given uuid"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()

        return Response(
            data={
                "message": "Task record deleted",
            },
            status=status.HTTP_200_OK
        )
