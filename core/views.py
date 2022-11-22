from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pprint import pprint
# Views are the part of the cdoe we write which are responsible for doing the
# work required on the API

# These are function based views


# csrf_exempt decorator for managing the policy for the check for the cross
# site request forgery
@csrf_exempt
# The api_view decorator manages the allowed HTTP methods for the API
@api_view(['GET', 'POST'])
def hello_world(request, *args, **kwargs):
    # The request details are sent in the request instance
    print('\n', '-'*40, "request", '-'*40)
    print("Request :", request)
    print("type:", type(request))
    pprint(request.__dict__)

    # The request headers are sent in the request.headers instance
    print('\n', '-'*40, "request", '-'*40)
    print("Headers :", request.headers)
    print("type:", type(request.headers))
    # pprint(request.__dict__)

    if request.method == "GET":
        # Returning the response on the GET call
        return Response(
            data={
                "hello": "world"
            },
            status=status.HTTP_200_OK
        )

    if request.method == "POST":
        name = request.data.get('form_field_name')
        # Returning the response on the POST call
        return Response(
            data={
                "hello": name
            },
            status=status.HTTP_201_CREATED
        )


@csrf_exempt
@api_view(['GET', 'PATCH'])
def hello_user(request, user, num, *args, **kwargs):
    """
    URI params can also be passed in the view in this way
    This view requires a URI param named user that the API request will have.
    The API path registered in the urls.py file determines the name of the
    parameter that is passed here.
    """
    print('='*75)
    # The request details are sent in the request instance
    print('\n', '-'*40, "request", '-'*40)
    print("Request :", request)
    print("type:", type(request))
    pprint(request.__dict__)

    print('\n', '-'*40, "uri_params", '-'*40)
    # The URI params passed in the API are passed with the keyword args
    uri_params = kwargs
    print("URI Params:", uri_params)
    print("type:", type(uri_params))

    print('\n', '-'*40, "query_params", '-'*40)
    # The query params passed in the API are stored in request.query_params
    query_params = request.query_params
    print("Query Params:", query_params)
    print("type:", type(query_params))

    print('\n', '-'*40, "form/JSON data", '-'*40)
    # The form/JSON data passed in the API are stored in request.data
    data = request.data
    print("Query Params:", data)
    print("type:", type(data), '\n')

    print('='*75)

    if request.method == "GET":
        form_field1 = request.data.get('form_field_name')
        return Response(
            data={
                "user": user,
                "form-data": form_field1,
                "num": num
            }
        )
