from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Review, Comment, Tag, User, UploadImage


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

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    images = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.IntegerField(required=True)
    author_username = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field='name', allow_empty=True
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'group', 'images', 'rating', 'author_id',
                  'author_username', 'average_rating', 'likes', 'tags', 'comments', 'created_at')


class CommentSerializer(serializers.ModelSerializer):

    def get_likes(self, obj):
        return obj.get_likes()

    def get_author_username(self, obj):
        return obj.author.username

    def get_review_id(self, obj):
        return obj.review.pk

    likes = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.IntegerField(required=True)
    author_username = serializers.SerializerMethodField(read_only=True)
    review_id = serializers.IntegerField(required=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'likes', 'author_id', 'author_username',
                  'review_id', 'created_at')


class TagSerializer(serializers.ModelSerializer):
    reviews = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'reviews', 'created_at')


class UploadImageSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(required=False)
    review_id = serializers.IntegerField(required=False)
    image = serializers.ImageField(use_url=True, required=True)

    class Meta:
        model = UploadImage
        fields = ('id', 'user_id', 'review_id', 'image')

    def validate_user_id(self, value):
        print(value)
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')
