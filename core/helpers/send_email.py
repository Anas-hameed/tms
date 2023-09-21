"""This helper function send an email to user"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token


def send_email(subject, template_name, context, email):
    """
    Send an email template to the recipient email address

    Args:
        subject : subject of the email
        template_name : template to send back
        context : context for the template, if there is any
        email : recipient email address
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        from_email='TMS System',
        recipient_list=[email],
        html_message=html_message,
    )


def send_invite_email(training_id, training_name, email):
    """
    This util function send an email to user for training invite

    Args:
        training_id: training id in which user is to be enrolled
        training_name: name of the training plan
        email (_type_): recipient email address
    """
    subject = 'Invitation for a training'
    template = 'invite.html'
    context = {
        'email': f'http://localhost:3000/user/invite?email={email}&training={training_id}',
        'training_name': training_name,
    }
    send_email(subject, template, context, email)


def forget_password_email(user):
    """send a forget password link to the user"""
    key = Token.objects.get(user=user).key
    print(key)
    subject = 'Reset your password'
    template = 'forget_password.html'
    context = {
        'reset_link': f'http://localhost:3000/password_reset?token={key}&email={user.email}',
        'username': user.username,
    }
    send_email(subject, template, context, user.email)
