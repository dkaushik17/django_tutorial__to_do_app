from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'

    def get_paginated_response(self, data, message=None):
        response_dict = {
            "page_info": {
                "result_count": self.page.paginator.count,
                "page_size": self.page_size,
                "page_count": self.page.paginator.num_pages,
                "page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "data": data
        }
        if message:
            response_dict['message'] = message
        return Response(response_dict)
