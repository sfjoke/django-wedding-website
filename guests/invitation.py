from django.conf import settings
from django.http import Http404
from guests.models import Invitation

INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'


def guess_party_by_invite_id_or_404(invite_id):
    try:
        return Invitation.objects.get(invitation_id=invite_id)
    except Invitation.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Invitation.objects.get(id=int(invite_id))
        else:
            raise Http404()


def get_invitation_context(party):
    return {
        'title': "Lion's Head",
        'main_image': 'bride-groom.png',
        'main_color': '#fff3e8',
        'font_color': '#666666',
        'page_title': "Karolina and Thibault- You're Invited!",
        'preheader_text': "You are invited!",
        'invitation_id': party.invitation_id,
        'party': party,
    }

