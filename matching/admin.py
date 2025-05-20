from django.contrib import admin
from .models import Match, LikeDislike

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user1__username', 'user2__username')


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_liked', 'timestamp')
    list_filter = ('is_liked', 'timestamp')
    search_fields = ('from_user__username', 'to_user__username')
