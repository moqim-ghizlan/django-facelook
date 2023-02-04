from django.urls import path, include
from . import views

urlpatterns = [
    # path('post/<int:id>/like', views.set_like),
    path('post/<int:id>/<str:action>', views.set_value_post),
    path('user/<int:id>/fowllowing', views.set_value_follow),
    path('user/<int:id>/i-follow', views.get_value_follow),
    path('post/<int:id>/nombers/likes', views.get_nb_likes),



    path('list/users', views.get_users_custom),
    path('topics', views.get_all_topics),
    path('topic/<int:id>', views.get_topic),
    path('post/create', views.create_post),
]
