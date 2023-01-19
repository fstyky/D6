from django.contrib import admin

# Register your models here.
from .models import Category, Product, CategoryN, Post,Author,PostCategory,Comment


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CategoryN)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
