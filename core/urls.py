from django.urls import path
from .views import CategoryAPI, BlogAPI, BlogViewAPI

urlpatterns = [
    path('blogs/category/', CategoryAPI.as_view(), name='category_api'),

    # GET request for getting all blogs
    path('blogs/', BlogAPI.as_view(), name='get_all_blogs'),
    
    # GET request for getting a single blog
    path('blog/<slug:slug>/', BlogViewAPI.as_view(), name='get_single_blog'),

    # POST request for creating a blog
    path('blogs/create/', BlogAPI.as_view(), name='create_blog'),

    # DELETE request for deleting a blog
    path('blogs/delete/', BlogAPI.as_view(), name='delete_blog'),

    # PATCH request for changing the status of a blog
    path('blogs/change_status/', BlogAPI.as_view(), name='change_blog_status'),

]
