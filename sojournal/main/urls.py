from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name="home"),

    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),

    path('addpost/', AddPost.as_view(), name="add_post"),
    path('post/<int:pk>/', PostPage.as_view(), name="post"),
    path('profile/<slug:username>/', ProfilePage.as_view(), name="profile"),
]