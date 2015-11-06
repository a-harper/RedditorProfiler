from django.contrib import admin

# Register your models here.
from .models import Redditor, Submission, Subreddit, Comment, RedditorStatus, Status, InterestingWord, WordCategory, \
    BadComment


class RedditorAdmin(admin.ModelAdmin):
    list_display = ('username', 'profile_url', 'last_updated')
    search_fields = ['username']


class SubredditAdmin(admin.ModelAdmin):
    list_display = ('name', 'over_18', 'flagged')
    search_fields = ['name']


class RedditorStatusAdmin(admin.ModelAdmin):
    list_display = ('redditor', 'status')
    search_fields = ['redditor__username']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subreddit', 'redditor', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('redditor', 'get_sreddit', 'body', 'controversiality', 'score', 'gilded')

    def get_sreddit(self, obj):
        return obj.submission.subreddit.name
    get_sreddit.short_description = 'Subreddit'


admin.site.register(Redditor, RedditorAdmin)
admin.site.register(RedditorStatus, RedditorStatusAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(Status)
admin.site.register(Comment, CommentAdmin)
admin.site.register(InterestingWord)
admin.site.register(WordCategory)
admin.site.register(BadComment)
