import logging
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Interest, Presentation

logger = logging.getLogger('ws')


@channel_session_user_from_http
def ws_connect(message):
    pass


@channel_session_user
def ws_message(message):
    msg = message.content.get('text')
    action, presentation_id = msg.split(':')

    if action == 'disinterested':

        interest = Interest.objects.get(
            user=message.user,
            presentation__presentation_id=int(presentation_id))
        interest.delete()

        resp = {'text': 'success'}

    elif action == 'interested':

        presentation = Presentation.objects.get(
            presentation_id=int(presentation_id))
        Interest.objects.create(
            user=message.user, presentation=presentation)

        resp = {'text': 'success'}

    else:
        resp = {'text': 'failure'}
    message.reply_channel.send(resp)
