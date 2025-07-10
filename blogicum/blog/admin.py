from django.contrib import admin

from .models import Post, Location, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'created_at',
        'is_published',
        'slug'
    ]
    prepopulated_fields = {'slug': ('title',)}

    list_editable = (

        'is_published',
    )

    search_fields = ('title', 'description',)
    list_filter = ('title', 'created_at', 'is_published')
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'is_published',
    )

    list_editable = (
        'is_published',
    )

    search_fields = ('name',)
    list_filter = ('name', 'created_at', 'is_published',)
    list_display_links = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'category',
        'pub_date',
        'is_published',
        'location',

    )

    list_editable = (
        'is_published',
    )

    search_fields = ('title', 'text',)
    list_filter = (
        'author',
        'category',
        'pub_date',
        'is_published',
        'location',
    )
    list_display_links = ('author', 'title', 'category')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'post',
        'created_at',
        'is_published',
    )

    search_fields = ('author', 'text',)
    list_filter = (
        'author',
        'is_published',
        'created_at',
    )
    list_display_links = ('author', 'created_at', 'post')
