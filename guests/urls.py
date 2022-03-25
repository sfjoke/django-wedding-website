from django.conf.urls import url

from guests.views import GuestListView, export_guests, invitation, rsvp_confirm, dashboard

urlpatterns = [
    url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^guests/export$', export_guests, name='export-guest-list'),
    url(r'^invite/(?P<invite_id>[\w-]+)/$', invitation, name='invitation'),
    url(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
]
