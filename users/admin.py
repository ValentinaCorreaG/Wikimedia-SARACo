"""Admin configuration for users app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile, TeamArea, Position

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_wiki_handle')
    list_select_related = ('profile',)

    def get_wiki_handle(self, instance):
        return instance.profile.professional_wiki_handle
    get_wiki_handle.short_description = 'Wiki Handle'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(TeamArea)
class TeamAreaAdmin(admin.ModelAdmin):
    """Admin for TeamArea model."""
    list_display = ('text', 'code')
    search_fields = ('text', 'code')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin for Position model."""
    list_display = ('text', 'type', 'area_associated')
    list_filter = ('type', 'area_associated')
    search_fields = ('text',)
