from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view, name='index'),
    path('contact/', views.ListContactView.as_view(), name='contact'),
    path('search/', views.SearchPostView.as_view(), name='search_post'),
    path('blog/', views.ListBlogView.as_view(), name='list_blog'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), # 追加　(例) /blog/detail/1　※特定のレコードに対して処理を行うので pk で識別
    #path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), # 追加　(例) /blog/update/1　※同上
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'), # 追加
    path('blog/create/', views.CreateBlogView.as_view(), name='create-blog'),
    path('item/<int:pk>', views.ListItemView.as_view(), name='item'),
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('article/<int:pk>/comment-delete/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
]