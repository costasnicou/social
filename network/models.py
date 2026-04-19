from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        User,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return f"Profile of: {self.user.username}"



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post: no {self.id} by {self.user.username}"

