from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from uuid import uuid4
from blogHub.utils import get_paginated_response

from django.db.models import Count

from user.permissions import IsAdmin, IsReader, IsAuthor
from user.models import CustomUser
from .serializers import CategorySerializer, GetCategorySerializer, GetBlogSerializer,TagsSerializer, PostBlogSerializer, GetAllBlogSerializer
from .models import CategoryModel, BlogModel, TagsModel
from .throttling import BlogAccessThrottle



class CategoryAPI(APIView):
    """API for Create, Read, and Delete Blog Categories"""
    # permission_classes = [IsAuthenticated, IsAdmin]
    def get_permissions(self):
        if self.request.method == 'GET':
            # Allow Admin, Author, and Reader to access the GET method
            return [IsAuthenticated()]  # Adjust to include your custom IsAuthor/IsReader if needed
        # For other methods (POST, PUT, DELETE), restrict to Admins
        return [IsAdmin()]

    def post(self, request):
        """Allow the Admin to CRUD Category for blogs"""
        request_data = request.data
        request_data['name'] = request_data.get('name').lower()

        serializer = CategorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "message": "Category created successfully",
                "data": serializer.data,
            }
            return Response(response_data, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Allow the Admin/Author/Reader to get all categories"""
        try:
            categories = CategoryModel.objects.annotate(blog_count = Count('categories'))
            return get_paginated_response(request, queryset=categories, page_size=10, serializer_class=GetCategorySerializer)
        except Exception as e:
            return Response({"Error": str(e)}, status= status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        """Allow the Admin to delete a category"""
        try:
            category_id = request.query_params.get('category_id')
            category = CategoryModel.objects.filter(id=category_id).first()
            if category:
                category.delete()
                return Response({"Message": f"Category {category.name} is deleted"}, status= status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Message':"No such category exists"},
                                 status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status= status.HTTP_400_BAD_REQUEST)



class BlogAPI(APIView):
    """API to Create, Delete, Update, Get List and change status of blogs by admin and blog user"""
    permission_classes = [IsAuthenticated, IsAuthor]


    def get(self, request):
        """Allow the Author to get all blogs"""
        session_user = request.user
        blogs = BlogModel.objects.filter(author=session_user)
        page_size = 10
        return get_paginated_response(request, page_size, 
                                      queryset = blogs, 
                                      serializer_class=GetAllBlogSerializer)
        
    def post(self, request):
        data = request.data

        categories = data.pop('category', []) 
        tags = data.pop('tags', []) 
        author_id = data.pop('author', {}).get('author_id') 
        blogdata = data.get('blog_data')

        try: 
            author = CustomUser.objects.get(id=author_id) 
        except CustomUser.DoesNotExist: 
            return Response({"error": "Author not found"},status= status.HTTP_404_NOT_FOUND)

        # Fetch categories and tags 
        blog_categories = CategoryModel.objects.filter(name__in=[cat.lower() for cat in categories]) 
        blog_tags = [TagsModel.objects.get_or_create(name=tag.lower())[0] for tag in tags]

        blog_serializer = PostBlogSerializer(data = blogdata)
        if blog_serializer.is_valid():
            blog_instance = blog_serializer.save(author = author)
            # Add many-to-many fields for catoegores and tags.
            blog_instance.categories.set(blog_categories)
            blog_instance.tags.set(blog_tags)

            return Response({
                'success': True,
                'message': 'Blog created successfully',
                'data': {"id": blog_instance.id, "title": blog_instance.title,"slug": blog_instance.slug,"status": blog_instance.status}
            }, status= status.HTTP_201_CREATED)
        
        return Response({"error": blog_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        """Delete a blog by id"""
        blog_id = request.data.get('blog_id')
        session_user = request.user
        blog = BlogModel.objects.filter(id = blog_id).first()
        if blog.author == session_user or session_user.user_type == "admin":
            blog.delete()
            return Response({"Message": f"Blog with id {blog_id} deleted successfully"}, status=status.HTTP_200_OK)

        return Response({"Message":"No Such Blog Exists"}, status=status.HTTP_404_NOT_FOUND)
    

    def patch(self, request):
        """Change the status of a blog by id"""
        blog_id = request.data.get('blog_id')
        blog_status = request.data.get('status')
        blog = BlogModel.objects.filter(id = blog_id).first()
        if blog:
            blog.status = blog_status
            blog.save()
            blog_status = "Published" if blog_status == 1 else "Draft"
            return Response({"Message": f"Blog with id {blog_id} status changed to {blog_status}"})
    


class BlogViewAPI(APIView):
    permission_classes = [AllowAny]  # Allow any user (authenticated or not)
    throttle_classes = [BlogAccessThrottle]

    def get(self, request, slug = None):
        # Fetch and return the blogs
        if slug:
            try:
                blog = BlogModel.objects.filter(slug = slug).first()
                blog_serializer = GetBlogSerializer(blog)
                return Response({"blogs": blog_serializer.data}, status=status.HTTP_200_OK)
            
            except BlogModel.DoesNotExist:
                return Response({"Message": "No such blog exists"}, status=status.HTTP_404_NOT_FOUND)
        
        blogs = BlogModel.objects.all().order_by('-created_at')
        blog_serializer = GetAllBlogSerializer(blogs, many=True)
        return Response({"blogs": blog_serializer.data}, status=status.HTTP_200_OK)