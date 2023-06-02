from accounts.models import Activation, Subscription
from django.contrib import admin

from django_forum_app.forms import PostAdminForm
from django_forum_app.models import (Category, Comment, Forum, Post,
                                     ProfaneWord, Topic, Vote)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["order", "title"]


'''class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscription_type']'''


class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "category", "creator", "created"]
    prepopulated_fields = {"slug": ("title",)}


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created", "block_top"]
    list_filter = ["creator", ('forum__title', custom_titled_filter('Forum')),]
    # filter_horizontal = ('forums',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator", 'tag_list']
    list_display = ["title", "topic", "creator", "created", "tag_list"]
    raw_id_fields = ('creator', 'topic')
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    # form = PostAdminForm


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    search_fields = ["text"]
    list_display = ["id", "text", "creator", "created"]


class VoteAdmin(admin.ModelAdmin):
    pass


class ProfaneWordAdmin(admin.ModelAdmin):
    pass


class ActivationAdmin(admin.ModelAdmin):
    list_display = ("user", "is_paid")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Activation, ActivationAdmin)
admin.site.register(Subscription)
