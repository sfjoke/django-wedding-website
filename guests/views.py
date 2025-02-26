import base64
from collections import namedtuple
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from guests import csv_import
from guests.invitation import guess_party_by_invite_id_or_404
from guests.models import Guest, Invitation, Party


class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    wedding = Party.objects.filter().order_by('name').first()
    invitations = wedding.invitation_set.all()
    # print(invitations)
    
    return render(request, 'guests/dashboard.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'guests': Guest.objects.filter(is_attending=True).count(),
        'possible_guests': Guest.objects.filter().exclude(is_attending=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'pending_guests': Guest.objects.filter(is_attending=None).count(),
        'unopened_invite_count': Invitation.objects.filter(invitation_opened=None).count(),
        'total_invites': Guest.objects.filter().count(),
    })


def invitation(request, invite_id):
    invitation = guess_party_by_invite_id_or_404(invite_id)
    if invitation.invitation_opened is None:
        # update if this is the first time the invitation was opened
        invitation.invitation_opened = datetime.utcnow()
        invitation.save()
    if request.method == 'POST':
        for response in _parse_invite_params(request.POST):
            guest = Guest.objects.get(pk=response.guest_pk)
            assert guest.party == invitation.party
            guest.is_attending = response.is_attending
            guest.save()
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            invitation.invitation_rsvp_text = comments if not invitation.invitation_rsvp_text else '{}; {}'.format(invitation.invitation_rsvp_text, comments)
        invitation.save()
        return HttpResponseRedirect(reverse('rsvp-confirm', args=[invite_id]))
    return render(request, template_name='guests/invitation.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'invitation': invitation,
        'guests': Guest.objects.filter(invitation=invitation),
        # party
    })


InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'is_attending'])


def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith('attending'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['attending'] = True if value == 'yes' else False
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(pk, response['attending'])


def rsvp_confirm(request, invite_id=None):
    invitation = guess_party_by_invite_id_or_404(invite_id)
    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'invitation': invitation,
        'guests': Guest.objects.filter(invitation=invitation, is_attending=True),
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
