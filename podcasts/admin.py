from django.contrib import admin
from podcasts.models import Podcast, Episode, Category

class PodcastAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ["pk","name"]
    list_filter = ["inReview"]
    readonly_fields=["pk", "rss_feed"]

class CategoryAdmin(admin.ModelAdmin):
    pass


class EpisodeAdmin(admin.ModelAdmin):
    list_per_page = 100

# Register your models here.
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Category, CategoryAdmin)