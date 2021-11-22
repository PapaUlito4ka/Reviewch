# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    title = models.CharField(max_length=128, null=False)
    text = models.TextField(null=False)
    group = models.CharField(max_length=10, null=False)
    images = ArrayField(models.CharField(max_length=512, default=''), default=list)
    rating = models.IntegerField(null=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    user_ratings = models.ManyToManyField(
        User,
        through='UserReviewRating',
        through_fields=('review', 'user'),
        related_name='rated_reviews'
    )
    user_likes = models.ManyToManyField(User, related_name='liked_reviews')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_average_rating(self):
        return self.user_ratings.aggregate(models.Avg('userreviewrating__rating'))['userreviewrating__rating__avg']

    def get_likes(self):
        return self.user_likes.count()


class Comment(models.Model):
    text = models.TextField(null=False)

    user_likes = models.ManyToManyField(User, related_name='liked_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_likes(self):
        return self.user_likes.count()


class UserReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)


class Tag(models.Model):
    name = models.CharField(max_length=32, null=False)

    reviews = models.ManyToManyField(Review, related_name='tags')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
