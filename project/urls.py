"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dcard.views import homepage, logout_view, post_detail, register, update_comment, user_login, add_comment, delete_comment, user_profile
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/0/", permanent=False)),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('add_comment/<str:post_no>/', add_comment, name='add_comment'),
    path('update_comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('logout/', logout_view, name='logout'),
    path('<slug:slug>/', homepage),
]