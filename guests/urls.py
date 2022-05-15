from django.urls import re_path

from guests.views import GuestListView, export_guests, invitation, rsvp_confirm, dashboard

urlpatterns = [
    re_path(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    re_path(r'^dashboard/$', dashboard, name='dashboard'),
    re_path(r'^guests/export$', export_guests, name='export-guest-list'),
    re_path(r'^invite/(?P<invite_id>[\w-]+)/$', invitation, name='invitation'),
    re_path(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
]
