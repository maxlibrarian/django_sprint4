from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'pub_date', 'is_published')
    list_editable = ('category', 'is_published')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'author__username')
    date_hierarchy = ('pub_date')
    readonly_fields = ('pub_date',)
    list_display_links = ('title',)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
