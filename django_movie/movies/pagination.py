from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class OptimizedLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_info': {
                'current_page': (self.offset // self.limit) + 1 if self.limit else 1,
                'total_pages': (self.count + self.limit - 1) // self.limit if self.limit else 1,
                'has_next': self.get_next_link() is not None,
                'has_previous': self.get_previous_link() is not None,
            }
        })


class SmallResultsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class LargeResultsPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 200