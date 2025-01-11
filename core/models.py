from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

# Category Model
class CategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self) -> str:
        return self.name 
    
    def save(self, *args, **kwargs):
        # If slug is not provided, generate it from the name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  


# Tags Model
class TagsModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


# BlogModel
class BlogModel(models.Model):

    STATUS = (
        (0, 'draft'),
        (1, 'published')
    )

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    categories = models.ManyToManyField(CategoryModel, related_name='categories')
    tags = models.ManyToManyField(TagsModel, related_name='tags')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = 'Blog'

    def save(self, *args, **kwargs):
        # If slug is not provided, generate it from the title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  

    def __str__(self) -> str:
        return self.title


# # Comment Model
# class CommentModel(models.Model):
#     content = models.CharField(max_length= 255)
#     blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenter')
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         ordering = ['created_at']

#     def __str__(self) -> str:
#         return self.content
       

# # Follow Model
class FollowModel(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

# # Like Model
class LikeModel(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likedBy')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='likedBlog')
    created_at = models.DateTimeField(auto_now_add=True)


# class NotificationModel(models.Model):
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=None)
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipients')
#     blog_post = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True, default=None)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Notification for {self.recipient.username}"