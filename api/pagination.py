from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'cur_page': self.page.number,
            'next_page': self.page.next_page_number() if self.page.has_next() else None,
            'prev_page': self.page.previous_page_number() if self.page.has_previous() else None,
            'count': self.page.paginator.count,
            'results': data
        })


class UserPagination(CustomPagination):
    page_size = 36


class ReviewPagination(CustomPagination):
    page_size = 10


class TagPagination(CustomPagination):
    page_size = 36
