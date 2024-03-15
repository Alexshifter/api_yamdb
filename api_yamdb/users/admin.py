from django.contrib import admin

from reviews.models import Category, Genre, Review, Title
from users.models import NewUser

admin.site.register(NewUser)
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
