from __future__ import unicode_literals, print_function
from email.mime.image import MIMEImage
import os
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from guests.models import Party


SAVE_THE_DATE_TEMPLATE = 'guests/email_templates/save_the_date.html'


def send_all_save_the_dates(test_only=False, mark_as_sent=False):
    to_send_to = Party.in_default_order().filter(is_invited=True, save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()


def send_save_the_date_to_party(party, test_only=False):
    context = get_save_the_date_context(0)
    recipients = party.guest_emails
    if not recipients:
        print('===== WARNING: no valid email addresses found for {} ====='.format(party))
    else:
        send_save_the_date_email(
            context,
            recipients,
            test_only=test_only
        )


def get_save_the_date_context(template_id):
    context = dict()
    context['name'] = template_id
    context['rsvp_address'] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    context['location'] = settings.WEDDING_LOCATION
    context['date'] = settings.WEDDING_DATE
    context['page_title'] = (settings.BRIDE_AND_GROOM + ' - Save the Date!')
    context['preheader_text'] = (
        "The date that you've eagerly been waiting for is finally here. " + settings.BRIDE_AND_GROOM + " are getting married! Save the date!"
    )
    return context


def send_save_the_date_email(context, recipients, test_only=False):
    context['email_mode'] = True
    context['rsvp_address'] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = ("Save the date for " + settings.BRIDE_AND_GROOM + "'s wedding! " + settings.WEDDING_DATE + ". " + settings.WEDDING_LOCATION)
    subject = 'Save the Date!'
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, settings.DEFAULT_WEDDING_FROM_EMAIL, recipients, reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['header_filename'], context['main_image']):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print('sending {} to {}'.format(context['name'], ', '.join(recipients)))
    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    print('clear')
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        print("resetting {}".format(party))
        party.save()
