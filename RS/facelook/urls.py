from django.urls import path
from . import views


#      route, location, name
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('registe', views.registe, name='registe'),
    path('signup', views.registe, name='registe'),
    path("logout", views.logout_user, name= "logout"),
    path('user/<int:id>/profile', views.profile, name='profile'),
    path('users/list', views.users_list, name='users_list'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/password/edit', views.password_edit, name='password_edit'),

    path('topic/<int:id>', views.topic, name='topic'),
    path('topics/', views.topics, name='topics'),
    path('posts/<int:id>', views.posts, name='posts'),
    path('posts/add', views.add_post, name='add_post'),
    path('posts/<int:id>/edit', views.edit_post, name='edit_post'),
    path('topic/<int:id>/edit', views.edit_topic, name='edit_topic'),
    path('topic/add', views.add_topic, name='add_topic'),
    path('user/<int:id>/posts', views.posts_for_user, name='posts_for_user'),
    path('user/<int:id>/topics', views.topics_for_user, name='topics_for_user'),
    path('user/<int:id>/follow-or-unfollow', views.follow_or_unfollow, name='follow_or_unfollow'),
    
 
    path('delete/<int:id>/<str:type_of_object>', views.delete, name='delete'),


    path('404', views.page_404, name='page_404'),
]
