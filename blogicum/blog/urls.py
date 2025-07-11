from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path(
        'posts/<int:post_id>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<post_id>/edit_comment/<int:pk>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<post_id>/delete_comment/<int:pk>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.create_edit_post,
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'edit_profile/',
        views.EditProfileView.as_view(),
        name='edit_profile'
    ),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/create/', views.create_edit_post, name='create_post'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'profile/<str:username>/', views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path('', views.index, name='index'),
]
