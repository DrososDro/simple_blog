from django.urls import path
from blog_posts import views


urlpatterns = [
    path("", views.home, name="home"),
    path("post/<str:pk>/", views.single_post, name="single_post"),
    path("create-post", views.create_post, name="create_post"),
    path("my-articles/", views.my_articles, name="my_articles"),
    path(
        "delete-article/<str:pk>",
        views.delete_article,
        name="delete_article",
    ),
    path("update-post/<str:pk>/", views.update_post, name="update_post"),
]
