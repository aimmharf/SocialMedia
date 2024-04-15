from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name='register'),
    path("login", views.login_user, name='login' ),
    path("logout", views.logout_user, name='logout'),
    path("newpost", views.new_posts, name='newposts'),
    path("profile/<str:username>", views.user_profile, name='profile'),
    path("newuser", views.new_user, name='newuser'),
    
    # Api requests
    path("post_api", views.post_api, name='post_api'),
    path("get_api", views.get_api, name='getapi'),
    path("current_user", views.current_user, name='current_user'),
    path("follow_user", views.follow, name='add_follower'),
    #path("remove_follower", views.remove_follower, name='remove_follower'),
    path("like_post", views.like_post, name='postLike'),
    path("like_count/<int:id>", views.like_count, name='like_count'),
    path("get_user", views.get_user, name='getuser'),
    path("comment/<int:id>", views.comment, name='commentUser'),
    path("post/<int:id>", views.get_id, name='id'),
    path("delete_post/<int:id>", views.delete_post, name='delete_post'),
    path("edit_post/<int:id>", views.edit_post, name='edit_post')
    
    
]