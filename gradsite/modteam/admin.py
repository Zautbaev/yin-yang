from django.contrib import admin
from django.utils.html import format_html
from .models import NewsPost, NewsImage, NewsLink, TeamMember, AboutPage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


class NewsLinkInline(admin.TabularInline):
    model = NewsLink
    extra = 1


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'cover_preview')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline, NewsLinkInline]
    list_editable = ('is_published',)

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px"/>', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Обложка'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_display_role', 'order', 'avatar_preview')
    list_editable = ('order',)
    search_fields = ('name',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:50%"/>', obj.avatar.url)
        return '—'
    avatar_preview.short_description = 'Аватар'


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'founded_year', 'mods_count', 'members_count')
