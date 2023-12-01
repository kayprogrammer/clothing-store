from django.contrib import admin

from apps.general.models import Message, SiteDetail, TeamMember


class SiteDetailAdmin(admin.ModelAdmin):
    pass


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    list_filter = list_display


class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")
    list_filter = list_display


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Message, MessageAdmin)
