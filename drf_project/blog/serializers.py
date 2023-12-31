from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'average_rating', 'rating_count', 'user_rating']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.value for rating in ratings) / len(ratings)
        return 0

    def get_rating_count(self, obj):
        return obj.ratings.count()

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_rating = obj.ratings.get(user=user)
                return user_rating.value
            except Rating.DoesNotExist:
                return None
        return None

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'post', 'value']
