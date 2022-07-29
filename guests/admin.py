import csv
import codecs
from django.http import HttpResponse
from django.contrib import admin
from .models import Guest, Party, Invitation


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class GuestInline(admin.TabularInline):
    model = Guest


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'rsvp_before')
    list_filter = ()
    inlines = [
        GuestInline,
    ]


class GuestAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('first_name', 'last_name', 'is_attending', 'is_child', 'is_staying', 'vegetarian_option_selected')
    list_filter = ('is_attending', 'is_child', 'is_staying', 'vegetarian_option_selected')
    actions = ['export_as_csv']


class InvitationAdmin(admin.ModelAdmin):
    inlines = [
        GuestInline,
    ]
    list_display = ('guest_names', 'invit_url', 'invitation_opened', 'invitation_rsvp_text')
    def xstr(self, s):
        return '' if s is None else ' '+str(s)

    def guest_names(self, obj):
        guests = Guest.objects.filter(invitation=obj)
        names = ', '.join([g.first_name + self.xstr(g.last_name) for g in guests])
        return names
    
    def invit_url(self, obj):
        return 'https://karolinaandthibault.sfjoke.com/invite/' + obj.invitation_id

admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Invitation, InvitationAdmin)
