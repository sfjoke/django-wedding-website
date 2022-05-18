from __future__ import unicode_literals
import datetime
import uuid

from django.db import models


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, default=None)
    rsvp_before = models.DateTimeField(null=True, blank=True, default=None)
    

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest_set.values_list('email', flat=True)))


class Invitation(models.Model):
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_rsvp_text = models.TextField(null=True, blank=True)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey('Party', on_delete=models.CASCADE, related_name = "party")
    invitation = models.ForeignKey('Invitation', blank=True, null=True, on_delete=models.CASCADE, related_name = "invitation")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    is_attending = models.BooleanField(null=True, default=None)
    is_child = models.BooleanField(default=False)
    vegetarian_option_selected = models.BooleanField(default=False)

    @property
    def name(self):
        if self.last_name:
            return u'{} {}'.format(self.first_name, self.last_name)
        else:
            return self.first_name

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
