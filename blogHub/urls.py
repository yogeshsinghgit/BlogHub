
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user.urls')),
    # social authentication
    # Include DJ-Rest-Auth URLs for login, logout, etc.
    path('auth/', include('dj_rest_auth.urls')),  
    # Include Allauth's URLs for social login, signup, etc.
    path('auth/social/', include('allauth.socialaccount.urls')), 
]

