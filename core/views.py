from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4

from user.permissions import IsAdmin, IsReader, IsAuthor
from .models import CategoryModel, BlogModel, TagsModel

