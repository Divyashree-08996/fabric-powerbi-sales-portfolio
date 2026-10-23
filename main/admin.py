from django.contrib import admin
from .models import UserProfile, VisitorLog, ContactMessage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'headline', 'education', 'email', 'is_public', 'updated_at')
    fieldsets = (
        ("Personal Information", {
            "fields": ("full_name", "headline", "bio", "is_public")
        }),
        ("Professional Background", {
            "fields": ("education", "experience_powerbi", "experience_sql")
        }),
        ("Contact & Social Connections", {
            "fields": ("email", "phone", "location", "linkedin_url", "github_url")
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 profile record to keep it clean
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'page_visited', 'ip_address', 'referrer')
    list_filter = ('page_visited', 'timestamp')
    search_fields = ('ip_address', 'page_visited', 'user_agent', 'referrer')
    readonly_fields = ('ip_address', 'page_visited', 'referrer', 'user_agent', 'timestamp')

    def has_add_permission(self, request):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'email', 'subject', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('timestamp', 'ip_address')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as Unread"
