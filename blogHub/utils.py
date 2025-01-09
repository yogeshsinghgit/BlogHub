from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

def get_paginated_response(request, page_size, queryset, serializer_class, page_number=1):
    """
    Utility function to paginate a queryset and return a paginated response.

    Args:
        request: The current HTTP request object.
        page_size: The number of items per page.
        queryset: The queryset to paginate.
        serializer_class: The serializer class for serializing the data.
        page_number (int, optional): The page number to retrieve. Defaults to 1.

    Returns:
        Response: A DRF Response object containing paginated data and metadata.
    """
    paginator = PageNumberPagination()
    paginator.page_size = page_size

    # Set the current page number in the request
    request.query_params._mutable = True  # Allow modification of query_params
    request.query_params['page'] = page_number
    request.query_params._mutable = False  # Make it immutable again

    # Paginate the queryset
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    # Serialize the paginated data
    serializer = serializer_class(paginated_queryset, many=True)

    # Return the paginated response
    return paginator.get_paginated_response(serializer.data)
