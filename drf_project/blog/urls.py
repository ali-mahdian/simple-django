from django.urls import path
from .views import PostListCreateView, RatingCreateUpdateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('rate/<int:post_id>/', RatingCreateUpdateView.as_view(), name='rating-create-update'),
]
