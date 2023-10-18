from rest_framework import pagination


class EducationPaginator(pagination.PageNumberPagination):
    page_size = 10

