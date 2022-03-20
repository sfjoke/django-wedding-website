from django.contrib import admin
from .models import Guest, Party, Invitation


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'is_child', 'party')
    # readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'rsvp_before')
    list_filter = ()
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email', 'is_attending', 'is_child')
    list_filter = ('is_attending', 'is_child')


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('invitation_id', 'invitation_sent', 'invitation_accepted', 'invitation_text', 'invitation_rsvp_text')
    list_filter = ('invitation_sent', 'invitation_accepted')
    inlines = [GuestInline]

admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Invitation, InvitationAdmin)
