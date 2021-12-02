from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Review, Comment, Tag, User, UploadImage


class UserSerializer(serializers.ModelSerializer):

    def get_image(self, obj):
        return obj.image.image.url

    image = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    date_joined = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'image',
                  'is_staff', 'reviews', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        UploadImage.objects.create(
            user=user
        )
        return user


class ReviewSerializer(serializers.ModelSerializer):

    def get_author_username(self, obj):
        return obj.author.username

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    images = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.IntegerField(required=True)
    author_username = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    text_markdown = serializers.CharField(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field='name', allow_empty=True
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'text_markdown', 'group', 'images', 'rating', 'author_id',
                  'author_username', 'average_rating', 'likes', 'tags', 'comments', 'created_at')


class CommentSerializer(serializers.ModelSerializer):

    def get_author_username(self, obj):
        return obj.author.username

    def get_review_id(self, obj):
        return obj.review.pk

    likes = serializers.IntegerField(read_only=True)
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
    reviews_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'reviews', 'reviews_count', 'created_at')


class UploadImageSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(required=False)
    review_id = serializers.IntegerField(required=False)
    image = serializers.ImageField(use_url=True, required=True)

    class Meta:
        model = UploadImage
        fields = ('id', 'user_id', 'review_id', 'image')
