from django.contrib import admin
from .models import Movie, Actor, Cast

class CastInline(admin.TabularInline):
    model = Cast
    extra = 1
    autocomplete_fields = ['actor']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_of_release', 'director')
    list_filter = ('year_of_release',)
    search_fields = ('title', 'director', 'script_writer')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'year_of_release', 'thumbnail')
        }),
        ('Production Details', {
            'fields': ('budget', 'box_office', 'director', 'script_writer', 'cinematographer'),
            'classes': ('collapse',)
        }),
    )
    inlines = [CastInline]

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)
    list_filter = ('date_of_birth',)

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('actor', 'movie', 'character_name')
    list_filter = ('movie',)
    search_fields = ('actor__name', 'movie__title', 'character_name')
    autocomplete_fields = ['actor', 'movie']