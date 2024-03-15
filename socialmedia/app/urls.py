from django.urls import path
from app import views

urlpatterns = [
    path('user/list',views.ListUser.as_view()),
    path('user/create/',views.CreateUser.as_view()),
    path('user/login/',views.LoginUserView.as_view()),
    path('user/<int:pk>/',views.RetrieveUser.as_view()),
    path('user/update/<int:pk>',views.UpdateUser.as_view()),
    path('user/delete/<int:pk>',views.DeleteUser.as_view()),


    path('post/list/',views.ListPost.as_view()),
    path('post/posts/',views.RetrieweUserPosts.as_view()),
    path('post/create/',views.CreatePost.as_view()),
    path('post/<int:pk>/',views.RetrievePost.as_view()),
    path('post/update/<int:pk>/',views.UpdatePost.as_view()),
    path('post/delete/<int:pk>/',views.DestroyPost.as_view()),
    path('post/like/<int:pk>/',views.LikePost.as_view()),
    path('post/likes/<int:pk>/',views.LikePost.as_view()),


    path('post/comment/<int:pk>/',views.CommentPost.as_view()),
    path('post/comments/<int:pk>/',views.CommentPost.as_view()),

    path('post/follow/<int:pk>/',views.FollowUser.as_view())
]
