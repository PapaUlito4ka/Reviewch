# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models
from markdown import markdown


class Review(models.Model):
    title = models.CharField(max_length=128, null=False)
    text = models.TextField(null=False)
    text_markdown = models.TextField(default='')
    group = models.CharField(max_length=10, null=False)
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.text_markdown = markdown(self.text)
        super(Review, self).save()

    def delete(self, using=None, keep_parents=False):
        tags_to_remove = []
        for tag in self.tags.all():
            if tag.reviews.count() == 1:
                tags_to_remove.append(tag)
        for tag in tags_to_remove:
            tag.delete()
        super(Review, self).delete()

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
    name = models.CharField(max_length=32, null=False, unique=True)

    reviews = models.ManyToManyField(Review, related_name='tags')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UploadImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='image', null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images', null=True)
    image = models.ImageField(upload_to='images/', default='user_profile.png')

