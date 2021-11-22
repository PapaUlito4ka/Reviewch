from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Review, Comment, Tag, User


class UserSerializer(serializers.ModelSerializer):

    reviews = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    date_joined = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'is_staff', 'reviews', 'last_login', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_likes(self, obj):
        return obj.get_likes()

    def get_author_username(self, obj):
        return obj.author.username

    images = serializers.ListField(child=serializers.CharField(), required=False)
    author_id = serializers.IntegerField(required=True)
    author_username = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'group', 'images', 'rating', 'author_id',
                  'author_username', 'average_rating', 'likes', 'created_at')


class CommentSerializer(serializers.ModelSerializer):

    def get_likes(self, obj):
        return obj.get_likes()

    def get_author(self, obj):
        return obj.author.username

    def get_review_id(self, obj):
        return obj.review.pk

    likes = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    author = serializers.SerializerMethodField()
    review_id = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'likes', 'author_id', 'author',
                  'review_id', 'created_at')


class TagSerializer(serializers.ModelSerializer):
    reviews = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'reviews', 'created_at')