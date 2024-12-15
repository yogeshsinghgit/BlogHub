from django.urls import path
from .views import SignupView, LoginView, LogoutView, CustomTokenRefreshView, GetUserInfoView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', GetUserInfoView.as_view(), name='userinfo'),
]
