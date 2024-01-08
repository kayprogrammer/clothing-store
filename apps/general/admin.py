from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.general.models import Message, SiteDetail, TeamMember


class SiteDetailAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        obj, created = self.model.objects.get_or_create()
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(obj.id,),
            )
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    list_filter = list_display


class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")
    list_filter = list_display


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Message, MessageAdmin)
