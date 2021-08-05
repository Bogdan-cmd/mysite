from django.urls import path
from blog import views

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'), #HOME PAGE
    path('about/',views.AboutView.as_view(),name='about'), #ABOUT PAGE
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',views.CreatePostView.as_view(),name='post_new'), #PT CREATE
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name='post_edit'), #PT UPDATE
    path('post/<int:pk>/remove/',views.PostDeleteView.as_view(),name='post_remove'), #PT STERGEREA UNUI POST
    path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove',views.comment_remove,name='comment_remove'),
    path('post/<int:pk>/publish',views.post_publish,name='post_publish'),
]
