from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RatingCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user, post=post)

    def perform_update(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        if serializer.instance.user != self.request.user or serializer.instance.post != post:
            raise PermissionDenied("You don't have permission to update this rating.")
        serializer.save(user=self.request.user)

    def get_object(self, post_id):
        try:
            return Rating.objects.get(post=post_id, user=self.request.user)
        except Rating.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        existing_rating = self.get_object(post_id)

        if existing_rating:
            return self.update(request, *args, **kwargs)
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        existing_rating = self.get_object(post_id)

        if existing_rating:
            serializer = self.get_serializer(existing_rating, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            raise ValidationError("Cannot update. Rating does not exist for the specified post.")

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user, post=post)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
