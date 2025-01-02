from rest_framework.serializers import ModelSerializer
from .models import (BlogModel, 
                     CategoryModel, 
                     TagsModel)



class CategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name']


class TagsSerializer(ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['id', 'name']


