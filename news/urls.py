from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.feed, name='feed'),
    path('article/<int:article_id>', views.get_article, name='get_article'),
    # path('feed/', views.feed, name='feed'),
    path('action', views.set_action, name='action'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]