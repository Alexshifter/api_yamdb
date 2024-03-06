from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass



class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    review = 
