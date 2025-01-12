from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (BlogModel, 
                     CategoryModel, 
                     TagsModel)




class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['name']

class GetCategorySerializer(ModelSerializer):
    blog_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'blog_count']


class TagsSerializer(ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['name']


class PostBlogSerializer(ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['title', 'content', 'status']


class GetAllBlogSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = BlogModel
        fields = ['id','title', 'status', 'categories', 'created_at']

class GetBlogSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = BlogModel
        fields = ['id','title', 'content', 'status', 'categories', 'tags', 'created_at', 'updated_at']

