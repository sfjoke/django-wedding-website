from django.contrib import admin
from .models import Guest, Party, Invitation


class GuestInline(admin.TabularInline):
    model = Guest


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'rsvp_before')
    list_filter = ()
    inlines = [
        GuestInline,
    ]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending', 'is_child')
    list_filter = ('is_attending', 'is_child')


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
